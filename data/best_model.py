from typing import Dict, Tuple
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import models, transforms
from torchvision.utils import save_image, make_grid
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
from IPython.display import HTML
#from diffusion_utilities import *
import os
import torchvision.transforms as transforms
from torch.utils.data import Dataset
from PIL import Image

#from diffusion_utilities import *


import random
import numpy as np
import torch

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if using multi-GPU
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)

import torch

torch.cuda.empty_cache()
torch.cuda.ipc_collect()




class ResidualConvBlock(nn.Module):
    def __init__(
        self, in_channels: int, out_channels: int, is_res: bool = False) -> None:
        super().__init__()

        # Check if input and output channels are the same for the residual connection
        self.same_channels = in_channels == out_channels

        # Flag for whether or not to use residual connection
        self.is_res = is_res

        # First convolutional layer
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, 1, 1),   # 3x3 kernel with stride 1 and padding 1
            nn.BatchNorm2d(out_channels),   # Batch normalization
            nn.ReLU(),   # GELU activation function
        )

        # Second convolutional layer
        self.conv2 = nn.Sequential(
            nn.Conv2d(out_channels, out_channels, 3, 1, 1),   # 3x3 kernel with stride 1 and padding 1
            nn.BatchNorm2d(out_channels),   # Batch normalization
            nn.ReLU(),   # GELU activation function
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:

        # If using residual connection
        if self.is_res:
            # Apply first convolutional layer
            x1 = self.conv1(x)

            # Apply second convolutional layer
            x2 = self.conv2(x1)

            # If input and output channels are the same, add residual connection directly
            if self.same_channels:
                out = x + x2
            else:
                # If not, apply a 1x1 convolutional layer to match dimensions before adding residual connection
                shortcut = nn.Conv2d(x.shape[1], x2.shape[1], kernel_size=1, stride=1, padding=0).to(x.device)
                out = shortcut(x) + x2
            #print(f"resconv forward: x {x.shape}, x1 {x1.shape}, x2 {x2.shape}, out {out.shape}")

            # Normalize output tensor
            return out / 1.414

        # If not using residual connection, return output of second convolutional layer
        else:
            x1 = self.conv1(x)
            x2 = self.conv2(x1)
            return x2

    # Method to get the number of output channels for this block
    def get_out_channels(self):
        return self.conv2[0].out_channels

    # Method to set the number of output channels for this block
    def set_out_channels(self, out_channels):
        self.conv1[0].out_channels = out_channels
        self.conv2[0].in_channels = out_channels
        self.conv2[0].out_channels = out_channels



class UnetUp(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(UnetUp, self).__init__()

        # Create a list of layers for the upsampling block
        # The block consists of a ConvTranspose2d layer for upsampling, followed by two ResidualConvBlock layers
        layers = [
            nn.ConvTranspose2d(in_channels, out_channels, 2, 2),
            ResidualConvBlock(out_channels, out_channels),
            ResidualConvBlock(out_channels, out_channels),
        ]

        # Use the layers to create a sequential model
        self.model = nn.Sequential(*layers)

    def forward(self, x, skip):
        # Concatenate the input tensor x with the skip connection tensor along the channel dimension
        x = torch.cat((x, skip), 1)
        x = self.model(x)
        return x

class UnetDown(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(UnetDown, self).__init__()

        # Create a list of layers for the downsampling block
        # Each block consists of two ResidualConvBlock layers, followed by a MaxPool2d layer for downsampling
        layers = [ResidualConvBlock(in_channels, out_channels), ResidualConvBlock(out_channels, out_channels), nn.MaxPool2d(2)]

        # Use the layers to create a sequential model
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        # Pass the input through the sequential model and return the output
        return self.model(x)

class EmbedFC(nn.Module):
    def __init__(self, input_dim, emb_dim):
        super(EmbedFC, self).__init__()
        '''
        This class defines a generic one layer feed-forward neural network for embedding input data of
        dimensionality input_dim to an embedding space of dimensionality emb_dim.
        '''
        self.input_dim = input_dim

        # define the layers for the network
        layers = [
            nn.Linear(input_dim, emb_dim),
            nn.GELU(),
            nn.Linear(emb_dim, emb_dim),
        ]

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        # flatten the input tensor
        x = x.view(-1, self.input_dim)
        # apply the model layers to the flattened tensor
        return self.model(x)
    


class CustomDataset(Dataset):
    def __init__(self, sfilename, lfilename, transform, null_context=False):
        self.hi_maps = np.load(sfilename)
        self.slabels = np.load(lfilename)
        print(f"hi_maps shape: {self.hi_maps.shape}")
        print(f"labels shape: {self.slabels.shape}")
        self.transform = transform
        self.null_context = null_context
        self.hi_maps_shape = self.hi_maps.shape
        self.slabel_shape = self.slabels.shape
                
    # Return the number of images in the dataset
    def __len__(self):
        return len(self.hi_maps)

    def __getitem__(self, idx):
      image = torch.from_numpy(self.hi_maps[idx].transpose(2, 0, 1)).float()
      label = torch.tensor(self.slabels[idx]).float()
      return (image, label)

   

    def getshapes(self):
        # return shapes of data and labels
        return self.hi_maps_shape, self.slabel_shape
#transform = transforms.Compose([
#   transforms.ToTensor()])

transform = transforms.Lambda(lambda x: torch.from_numpy(x.transpose(2, 0 , 1 )).float())




class ContextUnet(nn.Module):
    def __init__(self, in_channels, n_feat=64, n_cfeat=6, height=64):  # cfeat - context features
        super(ContextUnet, self).__init__()

        # number of input channels, number of intermediate feature maps and number of classes
        self.in_channels = in_channels
        self.n_feat = n_feat
        self.n_cfeat = n_cfeat
        self.h = height  #assume h == w. must be divisible by 4, so 28,24,20,16...

        # Initialize the initial convolutional layer
        self.init_conv = ResidualConvBlock(in_channels, n_feat, is_res=True)

        # Initialize the down-sampling path of the U-Net with two levels
        self.down1 = UnetDown(n_feat, n_feat)        # down1 #[10, 256, 8, 8]
        self.down2 = UnetDown(n_feat, 2 * n_feat)    # down2 #[10, 256, 4,  4]
        self.down3 = UnetDown(2 * n_feat, 4 * n_feat) # down3 #[10, 256, 2,  2]
        self.down4 = UnetDown(4 * n_feat, 8 * n_feat) # down4 #[10, 256, 1,  1]

         # original: self.to_vec = nn.Sequential(nn.AvgPool2d(7), nn.GELU())
        self.to_vec = nn.Sequential(nn.AvgPool2d((2)), nn.GELU())

        # Embed the timestep and context labels with a one-layer fully connected neural network
        self.timeembed1 = EmbedFC(1, 8*n_feat)
        self.timeembed2 = EmbedFC(1, 4*n_feat)
        self.contextembed1 = EmbedFC(n_cfeat, 8*n_feat)
        self.contextembed2 = EmbedFC(n_cfeat, 4*n_feat)

        # Initialize the up-sampling path of the U-Net with three levels
        self.up0 = nn.Sequential(
            nn.ConvTranspose2d(8 * n_feat, 8 * n_feat, 2, 2), # up-sample
            nn.GroupNorm(8, 8 * n_feat), # normalize
            nn.ReLU(),
        )
        self.up1 = UnetUp(16 * n_feat, 4 * n_feat)
        self.up2 = UnetUp(8 * n_feat, 2 * n_feat)
        self.up3 = UnetUp(4 * n_feat, n_feat)
        self.up4 = UnetUp(2 * n_feat, n_feat)

        # Initialize the final convolutional layers to map to the same number of channels as the input image
        self.out = nn.Sequential(
            nn.Conv2d(2 * n_feat, n_feat, 3, 1, 1), # reduce number of feature maps   #in_channels, out_channels, kernel_size, stride=1, padding=0
            nn.GroupNorm(8, n_feat), # normalize
            nn.ReLU(),
            nn.Conv2d(n_feat, self.in_channels, 3, 1, 1), # map to same number of channels as input
        )

    def forward(self, x, t, c=None):
        """
        x : (batch, n_feat, h, w) : input image
        t : (batch, n_cfeat)      : time step
        c : (batch, n_classes)    : context label
        """
        # x is the input image, c is the context label, t is the timestep, context_mask says which samples to block the context on

        # pass the input image through the initial convolutional layer
        x = self.init_conv(x)
        # pass the result through the down-sampling path
        down1 = self.down1(x)       #[10, 256, 8, 8]
        down2 = self.down2(down1)   #[10, 256, 4, 4]
        down3 = self.down3(down2)   #[10, 256, 2, 2]
        down4 = self.down4(down3)   #[10, 256, 1, 1]

        # convert the feature maps to a vector and apply an activation
        hiddenvec = self.to_vec(down4)

        # mask out context if context_mask == 1
        if c is None:
            c = torch.zeros(x.shape[0], self.n_cfeat).to(x)

        # embed context and timestep
        cemb1 = self.contextembed1(c).view(-1, self.n_feat * 8, 1, 1)     # (batch, 2*n_feat, 1,1)
        temb1 = self.timeembed1(t).view(-1, self.n_feat * 8, 1, 1)
        cemb2 = self.contextembed2(c).view(-1, self.n_feat * 4, 1, 1)
        temb2 = self.timeembed2(t).view(-1, self.n_feat * 4, 1, 1)
        #print(f"uunet forward: cemb1 {cemb1.shape}. temb1 {temb1.shape}, cemb2 {cemb2.shape}. temb2 {temb2.shape}")


        up1 = self.up0(hiddenvec)
        up2 = self.up1(cemb1*up1 + temb1, down4)  # add and multiply embeddings
        up3 = self.up2(cemb2*up2 + temb2, down3)
        up4 = self.up3(up3, down2)
        up5 = self.up4(up4, down1)
        out = self.out(torch.cat((up5, x), 1))
        return out


# hyperparameters

# diffusion hyperparameters
timesteps = 1500
beta1 = 1e-4
beta2 = 0.02

# network hyperparameters
device = torch.device("cuda:0" if torch.cuda.is_available() else torch.device('cpu'))
n_feat = 64 # 64 hidden dimension feature
n_cfeat = 6 
height = 64 
save_dir = './weights_64/'

# training hyperparameters
batch_size = 128
n_epoch = 200
lrate = 1e-3

# construct DDPM noise schedule
b_t = (beta2 - beta1) * torch.linspace(0, 1, timesteps + 1, device=device) + beta1
a_t = 1 - b_t
ab_t = torch.cumsum(a_t.log(), dim=0).exp()    
ab_t[0] = 1


# construct model
nn_model = ContextUnet(in_channels=1, n_feat=n_feat, n_cfeat=n_cfeat, height=height).to(device)

dataset = CustomDataset("/scratch/mrpcol001/Diffusion_job/data/Train64x64.npy",
 "/scratch/mrpcol001/Diffusion_job/data/Labels.npy", transform, null_context=False)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=1)

# load dataset and construct optimizer
#dataset = CustomDataset("Train64x64.npy", "Labels.npy", transform, null_context=False)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=1)
optim = torch.optim.Adam(nn_model.parameters(), lr=lrate)

# helper function: perturbs an image to a specified noise level
def perturb_input(x, t, noise):
    return ab_t.sqrt()[t, None, None, None] * x + (1 - ab_t[t, None, None, None]) * noise

# training without context code

# set into train mode
nn_model.train()

# Initialize lists to store loss values
train_losses = []
epoch_numbers = []

for ep in range(n_epoch):
    print(f'epoch {ep}')
    
    # linearly decay learning rate
    optim.param_groups[0]['lr'] = lrate*(1-ep/n_epoch)
    
    pbar = tqdm(dataloader, mininterval=2)
    epoch_loss = 0.0
    num_batches = 0
    
    for x, _ in pbar:   # x: images
        optim.zero_grad()
        x = x.to(device)
        
        # perturb data
        noise = torch.randn_like(x)
        t = torch.randint(1, timesteps + 1, (x.shape[0],)).to(device) 
        x_pert = perturb_input(x, t, noise)
        
        # use network to recover noise
        pred_noise = nn_model(x_pert, t / timesteps)
        
        # loss is mean squared error between the predicted and true noise
        loss = F.mse_loss(pred_noise, noise)
        loss.backward()
        
        optim.step()
        
        epoch_loss += loss.item()
        num_batches += 1
    
    # Calculate average loss for the epoch
    avg_epoch_loss = epoch_loss / num_batches
    train_losses.append(avg_epoch_loss)
    epoch_numbers.append(ep)
    
    # Print epoch statistics
    print(f'Epoch {ep}: Loss = {avg_epoch_loss:.4f}')
    
    # save model periodically
    if ep% 25==0 or ep == int(n_epoch-1):
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        torch.save(nn_model.state_dict(), save_dir + f"model_{ep}.pth")
        print('saved model at ' + save_dir + f"model_{ep}.pth")

# Plotting the training loss
plt.figure(figsize=(10, 6))
plt.plot(epoch_numbers, train_losses, label='Training Loss')
plt.title('Training Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.legend()
plt.grid(True)

# Save the plot
plot_path = os.path.join(save_dir, 'training_loss_relu_256.png')
plt.savefig(plot_path)
print(f'Saved training loss plot at {plot_path}')
plt.show()

# helper function; removes the predicted noise (but adds some noise back in to avoid collapse)
def denoise_add_noise(x, t, pred_noise, z=None):
    if z is None:
        z = torch.randn_like(x)
    noise = b_t.sqrt()[t] * z
    mean = (x - pred_noise * ((1 - a_t[t]) / (1 - ab_t[t]).sqrt())) / a_t[t].sqrt()
    return mean + noise


# sample using standard algorithm
@torch.no_grad()
def sample_ddpm(n_sample, save_rate=20):
    # x_T ~ N(0, 1), sample initial noise
    samples = torch.randn(n_sample, 1, height, height).to(device)  

    # array to keep track of generated steps for plotting
    intermediate = [] 
    for i in range(timesteps, 0, -1):
        print(f'sampling timestep {i:3d}', end='\r')

        # reshape time tensor
        t = torch.tensor([i / timesteps])[:, None, None, None].to(device)

        # sample some random noise to inject back in. For i = 1, don't add back in noise
        z = torch.randn_like(samples) if i > 1 else 0

        eps = nn_model(samples, t)    # predict noise e_(x_t,t)
        samples = denoise_add_noise(samples, i, eps, z)
        if i % save_rate ==0 or i==timesteps or i<8:
            intermediate.append(samples.detach().cpu().numpy())

    intermediate = np.stack(intermediate)
    return samples, intermediate


# Define model paths
model_paths = {
    50: "./scratch/mrpcol001/Diffusion_job/01aug/model_50.pth",
    100: "./scratch/mrpcol001/Diffusion_job/01aug/model_100.pth",
    150: "./scratch/mrpcol001/Diffusion_job/01aug/model_150.pth",
    199: "./scratch/mrpcol001/Diffusion_job/01aug/model_199.pth"
   # 399: "./weights_relu_192/model_399.pth"
}

generated_samples_dict = {}  # Global dictionary to store generated samples

# Load real samples
real_samples = []
for x, _ in dataloader:  # one batch is enough
    real_samples.extend(x)
    break
real_samples = torch.stack(real_samples)[:100].to(device)

def get_generated_samples(model_path):
    nn_model.load_state_dict(torch.load(model_path, map_location=device))
    nn_model.eval()
    samples, _ = sample_ddpm(100)  # adjust number of samples if needed
    return samples

generated_samples_dict[50] = get_generated_samples(model_paths[50])
generated_samples_dict[100] = get_generated_samples(model_paths[100])
generated_samples_dict[150] = get_generated_samples(model_paths[150])
generated_samples_dict[199] = get_generated_samples(model_paths[199])
#generated_samples_dict[399] = get_generated_samples(model_paths[399])

plt.figure(figsize=(10, 6))

# Plot real data
real_pixels = real_samples.cpu().numpy().flatten()
plt.hist(real_pixels, bins=50, label='Real Images', density=True, histtype='step')

# Plot each model's generated data
for epoch, samples in generated_samples_dict.items():
    pixels = samples.cpu().numpy().flatten()
    plt.hist(pixels, bins=50, label=f'Generated (Model {epoch})', density=True, histtype='step')

plt.xlabel('Pixel Intensity')
plt.ylabel('Normalized Frequency')
plt.title('Pixel Intensity Histograms (Real vs. Generated Images)')
plt.legend(loc='upper right')
plt.grid(True)
#plt.xlim(0.5, 2.5)  # Set x-axis limits
plt.xlim(-1, 1)  # Set x-axis limits
#plt.savefig('pixel_intensity_histograms_relu_256.png')
pixel_128 = os.path.join(save_dir, 'pixel_relu_192.png')
plt.savefig(pixel_128)

#plt.savefig('pixel_intensity_histograms_relu_192.png')
plt.show()


import numpy as np

def PowerSpectrum(box, N, dl):
    FT_box  = np.fft.fftn(box, norm="ortho")
    k       = 2 * np.pi * np.fft.fftfreq(N, dl)
    pk      = np.zeros(N)
    count   = np.zeros(N)
    dk_val  = 2 * np.pi / (N * dl)

    for i in range(N):
        for j in range(N):
            kbar = np.sqrt(k[i]**2 + k[j]**2)
            t = int(round(kbar / dk_val))
            if t < N:
                count[t] += 1.0
                pk[t] += FT_box[i, j] * np.conj(FT_box[i, j])

    pk /= np.where(count == 0, 1, count)  # Avoid division by zero
    pk *= dl**2
    dk = np.arange(N) * dk_val
    return dk, pk.real  # return only real part

# Parameters for images
N = 32
box_size = 25  # Mpc/h
dl = box_size / N


plt.figure(figsize=(10, 6))

# Real images power spectrum
real_imgs = real_samples.squeeze(1).cpu().numpy()
real_power = np.zeros(N)
for img in real_imgs:
    _, pk = PowerSpectrum(img, N, dl)
    real_power += pk
real_power /= len(real_imgs)
k_vals, _ = PowerSpectrum(real_imgs[0], N, dl)
plt.plot(k_vals, real_power, label='Real Images', linestyle='--')

# Generated images power spectrum
for epoch, samples in generated_samples_dict.items():
    gen_imgs = samples.squeeze(1).cpu().numpy()
    avg_pk = np.zeros(N)
    for img in gen_imgs:
        _, pk = PowerSpectrum(img, N, dl)
        avg_pk += pk
    avg_pk /= len(gen_imgs)
    plt.plot(k_vals, avg_pk, label=f'Model {epoch}')
plt.xlabel(r'$k$ [$h/\mathrm{Mpc}$]')
plt.ylabel(r'$P(k)$')
plt.title('Power Spectrum (Real vs. Generated Images)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
#plt.xlim(0.1, 1.0)  # Set x-axis limits
#plt.ylim(1e-4, 1e-1)  # Set y-axis limits
#plt.savefig('power_relu_192.png')
plt.xlim(0.0, 5.0)  # Set x-axis limits
plt.ylim(1e0, 1e-4)  # Set y-axis limits
power = os.path.join(save_dir, 'power.png')
plt.savefig(power)

plt.show()


nn_model.load_state_dict(torch.load(f"./scratch/mrpcol001/Diffusion_job/01aug/model_100.pth", map_location=device))
nn_model.eval()
print("Loaded in Model")
"""
plt.clf()
samples, intermediate_ddpm = sample_ddpm(32)
animation_ddpm = plot_sample(intermediate_ddpm,32,4,save_dir, "ani_run", None, save=False)
HTML(animation_ddpm.to_jshtml())
animation_ddpm.save('gelu_model199.gif', writer=PillowWriter(fps=10))
"""
real_data, _ = next(iter(dataloader))
real_data = real_data.to(device)
real_data.shape

fake_data = sample_ddpm(100)


real_samples = []
for x, _ in dataloader: # Assuming your dataloader yields (image, label) tuples
    real_samples.extend(x) # Collect a batch of samples
    break  # We only need one batch for demonstration

real_samples = torch.stack(real_samples)  # To make them tensor
real_samples = real_samples[:100] # Take the same number of samples for comparison

fig, axes = plt.subplots(2, 8, figsize=(15, 5))
for i in range(8):
    axes[0, i].imshow(real_samples[i, 0].cpu().numpy()) # Assuming grayscale im>
    axes[0,i].axis('off')

# Plot 8 random images from 'samples'
for i in range(8):
    axes[1, i].imshow(samples[i, 0].cpu().numpy())  # Assuming grayscale images>
    axes[1,i].axis('off')
#plt.savefig('real_vs_generated_relu_150.png')
real_100 = os.path.join(save_dir, 'real_vs_gene_200.png')
plt.savefig(real_100)
plt.show()


real_pixels = real_samples.cpu().numpy().flatten()
sampled_pixels = samples.cpu().numpy().flatten()

# Plot the histograms on the same axes
plt.figure(figsize=(10, 6))
plt.hist(real_pixels, bins=50, alpha=0.5, label='Real Images', density=True)
plt.hist(sampled_pixels, bins=50, alpha=0.5, label='Generated Images', density=True)
plt.xlabel('Pixel Intensity')
plt.ylabel('Normalized Frequency')
plt.title('Pixel Intensity Histograms (Real vs. Generated Images)')
plt.legend(loc='upper right')
#plt.xlim(0, 1)
plt.grid(True)
#plt.savefig('pixel_intensity_relu_150.png')
pixel_100 = os.path.join(save_dir, 'pixel_relu_100.png')
plt.savefig(pixel_100)


train = real_data.cpu()
reco = fake_data[0].cpu()


bin_max = np.max([train.max(), reco.max()])
bin_min = np.min([train.min(), reco.min()])
#bin_max, bin_min

bin_delta = 0.025
bins = np.arange(bin_min, bin_max + bin_delta, bin_delta)
#bins.shape

# compute all PDFs
train_pdf = []
reco_pdf = []
# Change len(train) to min(len(train), len(reco)) to iterate over the common length
for i in range(min(len(train), len(reco))):
    h= np.histogram(train[i].ravel(), bins, density=True)[0]
    train_pdf.append(h)
    h= np.histogram(reco[i].ravel(), bins,  density=True)[0]
    reco_pdf.append(h)
train_pdf = np.array(train_pdf)
reco_pdf  = np.array(reco_pdf)

#train_pdf.shape, reco_pdf.shape

# compute the mean and std PDFs
train_pdf_mean = np.mean(train_pdf, axis=0)
train_pdf_std = np.std(train_pdf, axis=0)
reco_pdf_mean = np.mean(reco_pdf, axis=0)
reco_pdf_std = np.std(reco_pdf, axis=0)


fig, ax  = plt.subplots(1,2, figsize=(14,4))
# average bin
bin_mid = (bins[1:]+ bins[:-1])/2.0
ax[0].plot(bin_mid, train_pdf_mean, 'k-', label= 'training')
ax[0].plot(bin_mid, reco_pdf_mean, 'b--', label='recontructed')
ax[0].set_ylabel(r"$\mu(\rm PDF)$", fontsize=14)
ax[1].plot(bin_mid, train_pdf_std, 'k-')
ax[1].plot(bin_mid, reco_pdf_std, 'b--')
ax[1].set_ylabel(r"$\sigma(rm PDF)$", fontsize=14)
for i in range(2):
    ax[i].set_xlabel(r'$N_{\rm HI}$', fontsize=14)
ax[0].legend(fontsize=16)
#ax[0].legend(fontsize=16)
plt.tight_layout()
#plt.savefig('mean_std_pdf_relu_150.png')
mean_100 = os.path.join(save_dir, 'mean_std_relu_100.png')
plt.savefig(mean_100)

plt.show()


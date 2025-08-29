# Design & Layout Customization Guide

## 🎨 **Overview**

Your Collins Personal Agent has two web interfaces with different design approaches:

1. **Streamlit App** (`streamlit_app.py`) - Python-based UI with embedded CSS
2. **Flask App** (`templates/index.html`) - Traditional HTML/CSS/JavaScript

## 📁 **File Structure**

```
collins_personal_agent/
├── streamlit_app.py          # Streamlit interface with embedded CSS
├── flask_app.py              # Flask backend
├── templates/
│   └── index.html            # Flask frontend (HTML/CSS/JS)
└── static/                   # (Optional) Static assets for Flask
    ├── css/
    ├── js/
    └── images/
```

## 🚀 **Streamlit App Customization**

### **1. Page Configuration**
```python
# In streamlit_app.py - Lines 10-15
st.set_page_config(
    page_title="Collins Personal Agent",
    page_icon="🤖",
    layout="wide",                    # "centered" or "wide"
    initial_sidebar_state="expanded"  # "collapsed" or "expanded"
)
```

**Customization Options:**
- `page_title`: Browser tab title
- `page_icon`: Emoji or file path to icon
- `layout`: "centered" (narrow) or "wide" (full width)
- `initial_sidebar_state`: "expanded" or "collapsed"

### **2. Custom CSS Styling**
```python
# In streamlit_app.py - Lines 18-65
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    /* ... more styles ... */
</style>
""", unsafe_allow_html=True)
```

**Key CSS Classes to Customize:**

#### **Header Styling**
```css
.main-header {
    font-size: 2.5rem;           /* Font size */
    font-weight: bold;           /* Font weight */
    color: #1f77b4;             /* Text color */
    text-align: center;          /* Alignment */
    margin-bottom: 2rem;         /* Spacing */
}
```

#### **Chat Message Styling**
```css
.chat-message {
    padding: 1rem;               /* Internal spacing */
    border-radius: 0.5rem;       /* Rounded corners */
    margin-bottom: 1rem;         /* Bottom spacing */
    border-left: 4px solid #1f77b4; /* Left border */
}

.user-message {
    background-color: #e3f2fd;   /* User message background */
    border-left-color: #2196f3;  /* User message border */
}

.assistant-message {
    background-color: #f3e5f5;   /* Assistant message background */
    border-left-color: #9c27b0;  /* Assistant message border */
}
```

#### **Panel Styling**
```css
.left-panel {
    background-color: #f8f9fa;   /* Panel background */
    padding: 1.5rem;             /* Internal spacing */
    border-radius: 10px;         /* Rounded corners */
    border: 1px solid #dee2e6;   /* Border */
    margin-bottom: 1rem;         /* Bottom spacing */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Shadow */
}
```

#### **Button Styling**
```css
.stButton > button {
    border-radius: 8px;          /* Rounded corners */
    font-weight: 500;            /* Font weight */
}

.quick-question-btn {
    background-color: #e3f2fd;   /* Background color */
    border: 1px solid #2196f3;   /* Border */
    color: #1976d2;              /* Text color */
}
```

### **3. Layout Structure**
```python
# Main layout structure in streamlit_app.py
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Collins Personal Agent</h1>', unsafe_allow_html=True)
    
    # Two-column layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Left panel - Controls and info
        st.markdown('<div class="left-panel">', unsafe_allow_html=True)
        # ... controls ...
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Right panel - Chat interface
        # ... chat area ...
```

## 🌐 **Flask App Customization**

### **1. HTML Structure**
```html
<!-- In templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Collins Personal Agent - Web Interface</title>
    <style>
        /* CSS styles here */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Collins Personal Agent</h1>
            <p>Hi, I'm Collins! Ask me anything about my background, skills, and research.</p>
        </div>
        
        <div class="info-panel" id="info-panel">
            <h3>📊 System Status</h3>
            <div id="kb-info">Loading...</div>
        </div>
        
        <div class="chat-area" id="chat-area">
            <!-- Chat messages appear here -->
        </div>
        
        <div class="input-area">
            <input type="text" id="question" placeholder="Ask me anything...">
            <button onclick="askQuestion()">Send</button>
        </div>
    </div>
    
    <script>
        // JavaScript functionality here
    </script>
</body>
</html>
```

### **2. CSS Customization**

#### **Body and Container**
```css
body {
    font-family: Arial, sans-serif;    /* Font family */
    max-width: 800px;                  /* Maximum width */
    margin: 0 auto;                    /* Center horizontally */
    padding: 20px;                     /* External spacing */
    background-color: #f5f5f5;         /* Background color */
}

.container {
    background: white;                 /* Container background */
    padding: 30px;                     /* Internal spacing */
    border-radius: 10px;               /* Rounded corners */
    box-shadow: 0 2px 10px rgba(0,0,0,0.1); /* Shadow */
}
```

#### **Header Styling**
```css
.header {
    text-align: center;                /* Center alignment */
    color: #1f77b4;                   /* Text color */
    margin-bottom: 30px;              /* Bottom spacing */
}
```

#### **Chat Area**
```css
.chat-area {
    border: 1px solid #ddd;           /* Border */
    border-radius: 5px;               /* Rounded corners */
    padding: 20px;                    /* Internal spacing */
    min-height: 300px;                /* Minimum height */
    margin-bottom: 20px;              /* Bottom spacing */
    background-color: #fafafa;        /* Background color */
}
```

#### **Input Area**
```css
.input-area {
    display: flex;                     /* Flexbox layout */
    gap: 10px;                        /* Gap between elements */
    margin-bottom: 20px;              /* Bottom spacing */
}

#question {
    flex: 1;                          /* Take remaining space */
    padding: 10px;                    /* Internal spacing */
    border: 1px solid #ddd;           /* Border */
    border-radius: 5px;               /* Rounded corners */
}

button {
    padding: 10px 20px;               /* Internal spacing */
    background-color: #1f77b4;        /* Background color */
    color: white;                     /* Text color */
    border: none;                     /* No border */
    border-radius: 5px;               /* Rounded corners */
    cursor: pointer;                  /* Pointer cursor */
}

button:hover {
    background-color: #1565c0;        /* Hover color */
}
```

#### **Message Styling**
```css
.response {
    background-color: #e3f2fd;        /* Assistant message background */
    padding: 15px;                    /* Internal spacing */
    border-radius: 5px;               /* Rounded corners */
    margin: 10px 0;                   /* Vertical spacing */
    border-left: 4px solid #2196f3;   /* Left border */
}

.user-question {
    background-color: #f3e5f5;        /* User message background */
    padding: 15px;                    /* Internal spacing */
    border-radius: 5px;               /* Rounded corners */
    margin: 10px 0;                   /* Vertical spacing */
    border-left: 4px solid #9c27b0;   /* Left border */
}
```

### **3. JavaScript Customization**
```javascript
// In templates/index.html - JavaScript section
function askQuestion() {
    const question = document.getElementById('question').value;
    if (!question.trim()) return;
    
    // Add user question to chat
    addMessage(question, 'user');
    
    // Show loading
    addMessage('Thinking...', 'assistant', 'loading');
    
    // Send to backend
    fetch('/api/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({question: question})
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message and add response
        removeLoadingMessage();
        addMessage(data.response, 'assistant');
    })
    .catch(error => {
        removeLoadingMessage();
        addMessage('Sorry, I encountered an error.', 'assistant');
    });
    
    document.getElementById('question').value = '';
}
```

## 🎨 **Color Schemes**

### **Default Blue Theme**
```css
/* Primary Colors */
--primary-color: #1f77b4;
--primary-light: #e3f2fd;
--primary-dark: #1565c0;

/* Secondary Colors */
--secondary-color: #9c27b0;
--secondary-light: #f3e5f5;
--secondary-dark: #7b1fa2;

/* Neutral Colors */
--background: #f5f5f5;
--surface: #ffffff;
--text-primary: #333333;
--text-secondary: #666666;
```

### **Alternative Themes**

#### **Green Theme**
```css
--primary-color: #4caf50;
--primary-light: #e8f5e8;
--primary-dark: #388e3c;
--secondary-color: #8bc34a;
--secondary-light: #f1f8e9;
--secondary-dark: #689f38;
```

#### **Purple Theme**
```css
--primary-color: #9c27b0;
--primary-light: #f3e5f5;
--primary-dark: #7b1fa2;
--secondary-color: #e91e63;
--secondary-light: #fce4ec;
--secondary-dark: #c2185b;
```

#### **Dark Theme**
```css
--primary-color: #bb86fc;
--primary-light: #2d2d2d;
--primary-dark: #3700b3;
--secondary-color: #03dac6;
--secondary-light: #1e1e1e;
--secondary-dark: #018786;
--background: #121212;
--surface: #1e1e1e;
--text-primary: #ffffff;
--text-secondary: #b3b3b3;
```

## 🔧 **Quick Customization Examples**

### **1. Change Color Scheme**
```python
# In streamlit_app.py - Update CSS colors
st.markdown("""
<style>
    .main-header {
        color: #4caf50;  /* Change from blue to green */
    }
    .chat-message {
        border-left-color: #4caf50;
    }
    .user-message {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
    }
</style>
""", unsafe_allow_html=True)
```

### **2. Change Font**
```python
# In streamlit_app.py
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)
```

### **3. Add Background Image**
```css
/* In templates/index.html */
body {
    background-image: url('path/to/background.jpg');
    background-size: cover;
    background-attachment: fixed;
}
```

### **4. Add Animations**
```css
/* In templates/index.html */
.chat-message {
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

## 📱 **Responsive Design**

### **Mobile-Friendly CSS**
```css
/* In templates/index.html */
@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    .container {
        padding: 15px;
    }
    
    .input-area {
        flex-direction: column;
    }
    
    button {
        width: 100%;
        margin-top: 10px;
    }
}
```

## 🎯 **Best Practices**

1. **Consistency**: Use the same color scheme throughout
2. **Accessibility**: Ensure good contrast ratios
3. **Responsive**: Test on different screen sizes
4. **Performance**: Optimize images and CSS
5. **User Experience**: Keep interfaces clean and intuitive

## 🚀 **Next Steps**

1. **Choose your interface**: Streamlit (easier) or Flask (more control)
2. **Pick a color scheme**: Use the provided themes or create your own
3. **Customize fonts**: Choose readable, professional fonts
4. **Add branding**: Include logos, custom icons, or personal touches
5. **Test responsiveness**: Ensure it works on mobile devices

The design is now fully customizable! Choose your preferred interface and start personalizing! 🎨

from flask import Flask, render_template, request, jsonify
import os
from colligent_config import Config
from colligent_core import ContextAwareChatbot

app = Flask(__name__)

# Initialize chatbot globally
config = Config()
chatbot = ContextAwareChatbot(config)

@app.route('/')
def home():
    """Main page"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to ask questions"""
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        response = chatbot.ask_question(question)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/info')
def get_info():
    """Get knowledge base info"""
    try:
        info = chatbot.get_knowledge_base_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modes')
def get_modes():
    """Get available modes"""
    try:
        modes = chatbot.get_available_modes()
        return jsonify(modes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mode/<mode_name>', methods=['POST'])
def set_mode(mode_name):
    """Set response mode"""
    try:
        result = chatbot.set_mode(mode_name)
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize knowledge base
    print("Initializing knowledge base...")
    success = chatbot.initialize_knowledge_base()
    if success:
        print("✅ Knowledge base initialized!")
    else:
        print("❌ Failed to initialize knowledge base")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

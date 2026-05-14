import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from src.vector_store import create_vector_store
from src.generator import generate_answer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Renders the main Chat Interface"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles PDF uploads and triggers vector store creation"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process the PDF and add to vector store
            create_vector_store(filepath)
            return jsonify({'success': True, 'message': f'Successfully ingested {filename}!'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handles the chat interaction"""
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
        
    question = data['question']
    
    try:
        # Generate answer using our pipeline
        answer = generate_answer(question)
        return jsonify({'success': True, 'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

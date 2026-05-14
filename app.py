# 1. SQLite Patch (Required for ChromaDB on Vercel)
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from src.vector_store import create_vector_store
from src.generator import generate_answer

app = Flask(__name__)

# 2. Use /tmp for uploads (Vercel's only writable directory)
app.config['UPLOAD_FOLDER'] = '/tmp/data'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Renders the main Chat Interface"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles multiple PDF uploads and triggers vector store creation"""
    if 'file' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
        
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No selected files'}), 400
        
    saved_paths = []
    filenames = []
    
    for file in files:
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            saved_paths.append(filepath)
            filenames.append(filename)
            
    if not saved_paths:
        return jsonify({'error': 'Invalid file types. Please upload PDFs only.'}), 400
        
    try:
        # Process all PDFs and add to vector store
        create_vector_store(saved_paths)
        msg = f'Successfully ingested {len(filenames)} file(s)!' if len(filenames) > 1 else f'Successfully ingested {filenames[0]}!'
        return jsonify({'success': True, 'message': msg})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

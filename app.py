from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
import docx
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    logger.warning("Downloading spacy model...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Predefined skill database
SKILL_DATABASE = {
    'programming_languages': [
        'python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'kotlin',
        'typescript', 'php', 'ruby', 'swift', 'objective-c', 'scala', 'r'
    ],
    'web_frameworks': [
        'django', 'flask', 'fastapi', 'spring', 'react', 'angular', 'vue',
        'express', 'rails', 'laravel', 'asp.net', 'nodejs'
    ],
    'databases': [
        'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
        'dynamodb', 'cassandra', 'oracle', 'sql server'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'docker', 'kubernetes'
    ],
    'devops_tools': [
        'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
        'terraform', 'ansible', 'prometheus', 'grafana'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'tensorflow', 'pytorch',
        'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
        'nlp', 'computer vision'
    ],
    'soft_skills': [
        'communication', 'teamwork', 'leadership', 'problem solving',
        'project management', 'analytical'
    ]
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(filepath, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(filepath):
    """Extract text from DOCX file"""
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        logger.error(f"Error reading DOCX: {e}")
    return text

def extract_text_from_txt(filepath):
    """Extract text from TXT file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading TXT: {e}")
    return ""

def extract_text(filepath):
    """Extract text based on file type"""
    file_ext = filepath.rsplit('.', 1)[1].lower()
    
    if file_ext == 'pdf':
        return extract_text_from_pdf(filepath)
    elif file_ext == 'docx':
        return extract_text_from_docx(filepath)
    elif file_ext == 'txt':
        return extract_text_from_txt(filepath)
    
    return ""

def extract_skills(text):
    """Extract skills from resume text"""
    text_lower = text.lower()
    found_skills = {
        'programming_languages': [],
        'web_frameworks': [],
        'databases': [],
        'cloud_platforms': [],
        'devops_tools': [],
        'data_science': [],
        'soft_skills': []
    }
    
    for category, skills in SKILL_DATABASE.items():
        for skill in skills:
            if skill in text_lower:
                found_skills[category].append(skill)
    
    return found_skills

def extract_entities(text):
    """Extract named entities from resume"""
    doc = nlp(text[:1000000])  # Limit text for processing
    
    entities = {
        'person': [],
        'org': [],
        'gpe': []
    }
    
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            entities['person'].append(ent.text)
        elif ent.label_ == 'ORG':
            entities['org'].append(ent.text)
        elif ent.label_ == 'GPE':
            entities['gpe'].append(ent.text)
    
    return {k: list(set(v)) for k, v in entities.items()}

def calculate_match_score(resume_skills, job_description):
    """Calculate match score between resume and job description"""
    job_skills = extract_skills(job_description)
    
    resume_flat = []
    for category, skills in resume_skills.items():
        resume_flat.extend(skills)
    
    job_flat = []
    for category, skills in job_skills.items():
        job_flat.extend(skills)
    
    if not job_flat:
        return 0
    
    matched = len(set(resume_flat) & set(job_flat))
    score = (matched / len(set(job_flat))) * 100
    
    return min(score, 100)

def calculate_similarity_score(resume_text, job_description):
    """Calculate text similarity using TF-IDF"""
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        documents = [resume_text, job_description]
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        return similarity * 100
    except:
        return 0

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], timestamp + filename)
        file.save(filepath)
        
        # Extract text
        resume_text = extract_text(filepath)
        
        if not resume_text:
            return jsonify({'error': 'Could not extract text from file'}), 400
        
        # Extract skills
        skills = extract_skills(resume_text)
        entities = extract_entities(resume_text)
        
        # Calculate scores
        skill_match_score = 0
        similarity_score = 0
        matched_skills = {}
        
        if job_description:
            skill_match_score = calculate_match_score(skills, job_description)
            similarity_score = calculate_similarity_score(resume_text, job_description)
            
            job_skills = extract_skills(job_description)
            matched_skills = {
                category: list(set(skills[category]) & set(job_skills[category]))
                for category in skills.keys()
            }
        
        # Calculate overall score
        overall_score = (skill_match_score * 0.7 + similarity_score * 0.3) if job_description else 0
        
        # Prepare response
        result = {
            'resume_filename': filename,
            'skills': skills,
            'entities': entities,
            'skill_match_score': round(skill_match_score, 2),
            'similarity_score': round(similarity_score, 2),
            'overall_score': round(overall_score, 2),
            'matched_skills': matched_skills,
            'resume_preview': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text
        }
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error processing upload: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

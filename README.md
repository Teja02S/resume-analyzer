# 📄 Resume Analyzer - AI-Powered Resume Analysis Tool

A production-ready Resume Analyzer built with Flask, Python NLP, Docker, and Kubernetes. This tool extracts skills from resumes, matches them against job descriptions, and generates comprehensive analysis scores.

## ✨ Features

- **📤 Resume Upload**: Support for PDF, DOCX, and TXT formats
- **🔍 Skill Extraction**: Automatic extraction of 100+ technical and soft skills
- **🎯 Job Matching**: Match resume skills against job descriptions
- **📊 Scoring System**:
  - Skill Match Score (70% weight)
  - Text Similarity Score (30% weight)
  - Overall Match Score
- **🏷️ Entity Recognition**: Extract names, organizations, and locations from resumes
- **🎨 Modern UI**: Beautiful, responsive web interface
- **📦 Production-Ready**: Docker & Kubernetes deployment configurations
- **🏥 Health Checks**: Built-in health monitoring endpoints

## 🛠️ Tech Stack

- **Backend**: Flask 2.3.3
- **NLP**: spaCy 3.6.1
- **ML**: scikit-learn, TF-IDF vectorization
- **File Processing**: PyPDF2, python-docx
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Server**: Gunicorn

## 📋 Project Structure

```
resume-analyzer/
├── app.py                          # Main Flask application
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker image configuration
├── docker-compose.yml              # Local development setup
├── .env                           # Environment variables
├── .gitignore                     # Git ignore rules
├── kubernetes/
│   ├── deployment.yaml            # K8s deployment
│   ├── service.yaml               # K8s service
│   └── configmap.yaml             # K8s configuration
├── templates/
│   ├── base.html                  # Base template
│   ├── upload.html                # Upload page
│   └── results.html               # Results page
└── static/
    ├── css/
    │   └── style.css              # Styling
    └── js/
        └── script.js              # Frontend logic
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Teja02S/resume-analyzer.git
   cd resume-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open http://localhost:5000 in your browser

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t resume-analyzer .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up
   ```

3. **Access the application**
   - Open http://localhost:5000 in your browser

### Kubernetes Deployment

1. **Build and push Docker image**
   ```bash
   docker build -t your-registry/resume-analyzer:latest .
   docker push your-registry/resume-analyzer:latest
   ```

2. **Update image in deployment.yaml**
   ```yaml
   image: your-registry/resume-analyzer:latest
   ```

3. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f kubernetes/
   ```

4. **Check deployment status**
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get svc
   ```

5. **Access the application**
   - Get the LoadBalancer IP: `kubectl get svc resume-analyzer-service`
   - Access via IP in browser

## 📊 Supported Skills Database

The application recognizes skills across multiple categories:

- **Programming Languages**: Python, Java, JavaScript, C++, Go, Rust, etc.
- **Web Frameworks**: Django, Flask, FastAPI, React, Angular, Vue, etc.
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch, etc.
- **Cloud Platforms**: AWS, Azure, GCP, Docker, Kubernetes, etc.
- **DevOps Tools**: Jenkins, GitLab CI, GitHub Actions, Terraform, Ansible, etc.
- **Data Science**: TensorFlow, PyTorch, scikit-learn, Pandas, NumPy, etc.
- **Soft Skills**: Communication, Leadership, Problem Solving, etc.

## 🔌 API Endpoints

### Upload and Analyze
- **POST** `/upload`
  - **Parameters**:
    - `file` (multipart/form-data): Resume file (PDF, DOCX, TXT)
    - `job_description` (optional): Job description text
  - **Response**: JSON with skills, scores, and entities

### Health Check
- **GET** `/health`
  - **Response**: `{"status": "healthy"}`

## 📈 Analysis Scoring

### Skill Match Score
- Compares skills found in resume against job description
- Range: 0-100%
- Formula: (Matched Skills / Total Required Skills) × 100

### Text Similarity Score
- Uses TF-IDF vectorization for semantic matching
- Range: 0-100%
- Compares resume content with job description

### Overall Score
- Weighted combination of scores
- Formula: (Skill Match × 0.7) + (Text Similarity × 0.3)
- Range: 0-100%

## 🔧 Configuration

### Environment Variables

```env
FLASK_ENV=development          # development or production
DEBUG=False                    # Debug mode
SECRET_KEY=your-secret-key    # Flask secret key
```

### File Upload Settings

- **Maximum File Size**: 10MB
- **Allowed Formats**: PDF, DOCX, TXT
- **Upload Directory**: `./uploads`

## 📦 Dependencies

- Flask 2.3.3
- PyPDF2 3.0.1
- python-docx 0.8.11
- spacy 3.6.1
- scikit-learn 1.3.0
- numpy 1.24.3
- pandas 2.0.3
- gunicorn 21.2.0
- python-dotenv 1.0.0

## 🏗️ Kubernetes Features

- **Replicas**: 3 pods for high availability
- **Resource Management**: CPU & memory requests/limits
- **Health Checks**: Liveness and readiness probes
- **Service Type**: LoadBalancer for external access
- **Configuration**: ConfigMap for environment management

## 📝 Logging

Application logs are configured at INFO level. Check logs using:

```bash
# Docker
docker logs resume-analyzer

# Kubernetes
kubectl logs -f deployment/resume-analyzer
```

## 🔐 Security Considerations

1. **File Upload Validation**: Strict file type and size validation
2. **Filename Sanitization**: Uses `secure_filename()` to prevent path traversal
3. **Environment Variables**: Sensitive data stored in .env (not committed)
4. **CORS**: Configure CORS headers if needed for API access
5. **Secret Key**: Change `SECRET_KEY` in production

## 🎯 Interview Highlights

This project demonstrates:

✅ **Full-stack Development**: Flask backend, responsive frontend
✅ **NLP & ML Skills**: spaCy, scikit-learn, TF-IDF vectorization
✅ **Cloud Architecture**: Docker containerization, Kubernetes orchestration
✅ **DevOps**: Health checks, resource management, scalability
✅ **Best Practices**: Configuration management, error handling, logging
✅ **Production-Ready**: Gunicorn, health endpoints, resource optimization

## 🚀 Future Enhancements

- [ ] Advanced resume parsing with more entity types
- [ ] Database integration for resume history
- [ ] Enhanced NLP with transformer models (BERT, GPT)
- [ ] Resume ranking against multiple job descriptions
- [ ] Email notifications for score updates
- [ ] Admin dashboard for analytics
- [ ] API authentication (JWT)
- [ ] Rate limiting

## 📄 License

MIT License - feel free to use this project for learning and commercial purposes.

## 👤 Author

Created by Teja02S for demonstration and interview preparation purposes.

## 💬 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for interview success in 2026!**

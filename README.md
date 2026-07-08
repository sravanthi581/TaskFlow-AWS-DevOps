# 🚀 TaskFlow: Automated CI/CD Pipeline for Flask Task Management System

# 🚀 TaskFlow

![Python](https://img.shields.io/badge/Python-3.11-blue)

![Flask](https://img.shields.io/badge/Flask-3.1-green)

![AWS](https://img.shields.io/badge/AWS-DevOps-orange)

![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

![CI/CD](https://img.shields.io/badge/CI/CD-CodePipeline-success)

## 📌 Project Overview

TaskFlow is a cloud-based Task Management System developed using **Flask** and deployed on **Amazon EC2** using a complete **CI/CD pipeline** built with AWS DevOps services.

Whenever code is pushed to GitHub, AWS automatically builds, tests, and deploys the latest version to the EC2 instance.

---

# ✨ Features

- ✅ Create Tasks
- ✅ Delete Tasks
- ✅ Complete Tasks
- ✅ Search Tasks
- ✅ Task Statistics
- ✅ Responsive Dashboard
- ✅ Priority Management
- ✅ Category Management
- ✅ Due Date Management
- ✅ Modern Bootstrap UI
- ✅ Automated CI/CD Pipeline

---

# 🛠 Tech Stack

### Backend
- Python
- Flask

### Database
- SQLite

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### DevOps
- AWS EC2
- AWS CodePipeline
- AWS CodeBuild
- AWS CodeDeploy
- Gunicorn
- Nginx
- GitHub

---

# 📂 Project Structure

```
TaskFlow-AWS-DevOps/
│
├── app.py
├── database.py
├── requirements.txt
├── buildspec.yml
├── appspec.yml
├── README.md
├── taskflow.db
│
├── templates/
│   ├── base.html
│   ├── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── scripts/
    ├── install_dependencies.sh
    ├── start_server.sh
    └── stop_server.sh
```

---

# ⚙️ CI/CD Workflow

```
Developer
     │
     ▼
GitHub Repository
     │
     ▼
AWS CodePipeline
     │
     ▼
AWS CodeBuild
     │
     ▼
AWS CodeDeploy
     │
     ▼
Amazon EC2
     │
     ▼
Gunicorn
     │
     ▼
Nginx
     │
     ▼
Browser
```

---

# 🚀 Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd TaskFlow-AWS-DevOps
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open

```
http://localhost:5000
```

---

# ☁️ Deployment

The application is deployed using

- AWS EC2
- Gunicorn
- Nginx
- AWS CodeDeploy
- AWS CodeBuild
- AWS CodePipeline

---

# 📷 Screenshots

### Dashboard

(Add Screenshot)

### Create Task

(Add Screenshot)

### AWS Pipeline

(Add Screenshot)

### EC2 Deployment

(Add Screenshot)

---

# 👩‍💻 Developed By

Sravanthi Duggineni

B.Tech – Artificial Intelligence & Machine Learning

VVIT

---

# ⭐ Future Enhancements

- User Authentication
- Email Notifications
- Task Categories
- Task Priority Levels
- Dark Mode
- REST API
- Docker Support
- PostgreSQL Support
- Unit Testing
- Monitoring with CloudWatch

---

# 📄 License

This project is developed for educational and internship purposes.

# 🛒 Ecommerce App with CI/CD on Azure

This project is a simple **Flask-based Ecommerce Application** deployed using a **Jenkins CI/CD pipeline**.  
The pipeline builds, tests, containers, pushes to Docker Hub, and deploys to an **Azure VM** automatically.

---

## 🚀 Tech Stack
- **Backend**: Flask + Gunicorn
- **Testing**: Pytest
- **Containerization**: Docker
- **CI/CD**: Jenkins (Pipeline as Code)
- **Hosting**: Azure VM
- **Registry**: Docker Hub

---

## 📂 Project Structure
```
ecommerce-app-demo/
│── app.py              # Flask application
│── requirements.txt    # Dependencies
│── Dockerfile          # Docker image build instructions
│── Jenkinsfile         # CI/CD pipeline
│── tests/              # Unit tests
```

---

## 🔧 CI/CD Pipeline Stages
1. **Checkout** → Clone repo from GitHub  
2. **Install & Test** → Install dependencies & run `pytest`  
3. **Build & Push Docker Image** → Build amd64 image & push to Docker Hub  
4. **Deploy to Azure VM** →  
   - Remove old container  
   - Pull latest image from Docker Hub  
   - Run container with port mapping `5000:5000`  

---

## 📦 Build & Run Locally
```bash
# Clone repo
git clone https://github.com/rahman5828/ecommerce-app-demo.git
cd ecommerce-app-demo

# Build Docker image
docker build -t ecommerce-app .

# Run container
docker run -d -p 5000:5000 ecommerce-app

# Open in browser
http://localhost:5000
```

---

## ☁️ Deployment on Azure VM
The Jenkins pipeline deploys automatically to the Azure VM.  
Check running containers:
```bash
ssh -i ~/.ssh/jenkins_id_rsa azureuser@<VM_IP>
docker ps
```

---

## 🔗 Important Links
- **GitHub Repo**: [ecommerce-app-demo](https://github.com/rahman5828/ecommerce-app-demo)  
- **Docker Hub Image**: [rahman5828/ecommerce-app](https://hub.docker.com/r/rahman5828/ecommerce-app)  
- **Live App (Azure VM)**: `http://<VM_IP>:5000`

---

## ✅ Status
- CI/CD pipeline **working successfully** 🎉  
- Any push to `main` → triggers Jenkins → builds & deploys app to Azure VM automatically.

---

# 🚀 Deploying Nginx on Kubernetes (GKE & Minikube)  

This project demonstrates how to **deploy an Nginx web server on Kubernetes**, using either **Google Kubernetes Engine (GKE)** or **Minikube**.  
---

## **🎯 Project Overview**  
This project follows these key steps:  
1️⃣ **Set up a Kubernetes cluster** (GKE or Minikube)  
2️⃣ **Deploy a simple Nginx web app**  
3️⃣ **Expose the app to the internet**  
4️⃣ **Push the Kubernetes configuration to GitHub**  

---

## **⚡ Prerequisites**  
Before starting, install the following:  
- [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install)  
- [Kubectl (Kubernetes CLI)](https://kubernetes.io/docs/tasks/tools/)  
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) (for local testing)  
- [Git](https://git-scm.com/downloads) (for version control)  

---

## **🚀 Implementation Steps**  

### **🔹 1️⃣ Set Up Kubernetes Cluster**  

#### **Option 1: Using GKE (Google Kubernetes Engine)**  
```bash
# Authenticate with GCP  
gcloud auth login  
gcloud config set project YOUR_PROJECT_ID  

# Enable Kubernetes API  
gcloud services enable container.googleapis.com  

# Create a Kubernetes Cluster  
gcloud container clusters create my-gke-cluster --num-nodes=2 --region=us-central1  

# Connect to the Cluster  
gcloud container clusters get-credentials my-gke-cluster --region=us-central1  



# 🚀 Deploying Nginx on Kubernetes (GKE) with GitHub Actions  

---

## **📌 Project Overview**  
This project follows these key steps:  
1️⃣ **Set up a Kubernetes cluster on GKE**  
2️⃣ **Deploy a simple Nginx web app**  
3️⃣ **Expose the app to the internet**  
4️⃣ **Automate deployments using GitHub Actions**  

---

## **🚀 Deployment Steps**  

### **🔹 1️⃣ Set Up Kubernetes Cluster**  

#### **Using an Existing GKE Cluster**  
If you already have a GKE cluster, connect to it:  
```bash
gcloud container clusters get-credentials YOUR_EXISTING_CLUSTER_NAME --region=YOUR_CLUSTER_REGION
kubectl get nodes


🔹 2️⃣ Deploy Nginx to Kubernetes
Create Deployment (k8s/nginx-deployment.yaml)

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80

Apply the service:

kubectl apply -f k8s/nginx-service.yaml
kubectl get svc nginx-service


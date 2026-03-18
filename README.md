# 📸 Intelligent Event Photo Retrieval System

## 🚀 Overview
An AI-powered system that allows users to find themselves in event photos using just one selfie. Perfect for weddings, corporate events, and parties.

## ✨ Features
- 🔍 **Multi-face detection** in group photos
- 🎯 **Accurate face matching** with FaceNet embeddings
- ⚡ **Fast search** using FAISS vector database
- 🌐 **Simple web interface** with Streamlit
- 🔒 **Local processing** for privacy
- ⚙️ **Adjustable similarity threshold**

## 🛠️ Technology Stack
- **Face Detection:** MTCNN (Multi-task Cascaded CNN)
- **Face Recognition:** FaceNet (512D embeddings)
- **Similarity Search:** FAISS (Facebook AI Similarity Search)
- **Web Framework:** Streamlit
- **Programming Language:** Python 3.8+

## 📋 Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum
- 500MB free disk space

## 🚀 Installation & Setup

### 1. Clone/Setup Project
```bash
# Create project directory
mkdir event_photo_retrieval
cd event_photo_retrieval

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
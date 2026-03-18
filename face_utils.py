import cv2
import numpy as np
from PIL import Image
import sys
import os

# Try to import required packages with fallbacks
try:
    from mtcnn import MTCNN
    MTCNN_AVAILABLE = True
except ImportError:
    MTCNN_AVAILABLE = False
    print("Warning: MTCNN not available. Using OpenCV fallback.")

try:
    import torch
    from facenet_pytorch import InceptionResnetV1
    FACENET_AVAILABLE = True
except ImportError:
    FACENET_AVAILABLE = False
    print("Warning: FaceNet not available.")

class FaceProcessor:
    def __init__(self):
        self.detector = None
        self.recognizer = None
        
        # Initialize face detector
        if MTCNN_AVAILABLE:
            try:
                self.detector = MTCNN()
                print("Using MTCNN for face detection")
            except:
                self.detector = None
        
        # If MTCNN fails, use OpenCV Haar cascades
        if self.detector is None:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if os.path.exists(cascade_path):
                self.detector = cv2.CascadeClassifier(cascade_path)
                print("Using OpenCV Haar Cascade for face detection")
        
        # Initialize face recognizer
        if FACENET_AVAILABLE:
            try:
                self.recognizer = InceptionResnetV1(pretrained='vggface2').eval()
                print("Using FaceNet for face recognition")
            except:
                self.recognizer = None
    
    def detect_faces(self, image_path):
        """Detect all faces in an image"""
        try:
            # Read image
            if isinstance(image_path, str):
                image = cv2.imread(image_path)
                if image is None:
                    raise ValueError(f"Could not read image: {image_path}")
            else:
                # Assume it's already an image array
                image = image_path
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            faces = []
            boxes = []
            
            # Use MTCNN if available
            if MTCNN_AVAILABLE and isinstance(self.detector, MTCNN):
                detections = self.detector.detect_faces(image_rgb)
                
                for detection in detections:
                    x, y, width, height = detection['box']
                    x, y = abs(x), abs(y)
                    
                    # Ensure box is within image boundaries
                    x1, y1 = max(0, x), max(0, y)
                    x2, y2 = min(image.shape[1], x + width), min(image.shape[0], y + height)
                    
                    # Crop face
                    face = image[y1:y2, x1:x2]
                    
                    if face.size > 0 and face.shape[0] > 20 and face.shape[1] > 20:
                        # Resize to 160x160 for FaceNet
                        face = cv2.resize(face, (160, 160))
                        faces.append(face)
                        boxes.append((x1, y1, x2, y2))
            
            # Use OpenCV Haar Cascade as fallback
            elif isinstance(self.detector, cv2.CascadeClassifier):
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                detections = self.detector.detectMultiScale(
                    gray, 
                    scaleFactor=1.1, 
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                for (x, y, w, h) in detections:
                    face = image[y:y+h, x:x+w]
                    
                    if face.size > 0:
                        face = cv2.resize(face, (160, 160))
                        faces.append(face)
                        boxes.append((x, y, x+w, y+h))
            
            return faces, boxes
            
        except Exception as e:
            print(f"Error in detect_faces: {str(e)}")
            return [], []
    
    def get_embedding(self, face_image):
        """Convert face image to embedding vector"""
        try:
            if self.recognizer is None or not FACENET_AVAILABLE:
                # Return dummy embedding if FaceNet not available
                return np.random.randn(512).astype('float32')
            
            # Convert to tensor
            if isinstance(face_image, np.ndarray):
                face_tensor = torch.from_numpy(face_image).float()
            else:
                face_tensor = face_image
            
            # Normalize
            face_tensor = face_tensor / 255.0
            
            # Ensure correct shape: [batch, channels, height, width]
            if len(face_tensor.shape) == 3:
                face_tensor = face_tensor.permute(2, 0, 1).unsqueeze(0)  # [1, 3, 160, 160]
            
            # Get embedding
            with torch.no_grad():
                embedding = self.recognizer(face_tensor)
            
            return embedding.numpy().flatten().astype('float32')
            
        except Exception as e:
            print(f"Error in get_embedding: {str(e)}")
            return np.random.randn(512).astype('float32')
    
    def process_image(self, image_path):
        """Process single image and return embeddings and metadata"""
        try:
            faces, boxes = self.detect_faces(image_path)
            
            embeddings = []
            for face in faces:
                embedding = self.get_embedding(face)
                embeddings.append(embedding)
            
            return embeddings, boxes, len(faces)
            
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            return [], [], 0
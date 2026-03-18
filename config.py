import os

class Config:
    # Project paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Data paths
    DATA_DIR = os.path.join(BASE_DIR, "data")
    INPUT_IMAGE_DIR = os.path.join(DATA_DIR, "input")
    REFERENCE_IMAGE_DIR = os.path.join(DATA_DIR, "reference")
    OUTPUT_DIR = os.path.join(DATA_DIR, "output")
    
    # Database paths
    FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index.bin")
    METADATA_PATH = os.path.join(BASE_DIR, "metadata.pkl")
    
    # Face detection settings
    MIN_FACE_SIZE = 20
    FACE_DETECTION_CONFIDENCE = 0.9
    
    # Similarity threshold (0.0 to 1.0)
    SIMILARITY_THRESHOLD = 0.6
    
    # Performance settings
    BATCH_SIZE = 32
    
    # Create directories if they don't exist
    @staticmethod
    def setup_directories():
        os.makedirs(Config.INPUT_IMAGE_DIR, exist_ok=True)
        os.makedirs(Config.REFERENCE_IMAGE_DIR, exist_ok=True)
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        print(f"Directories created:")
        print(f"  - Event photos: {Config.INPUT_IMAGE_DIR}")
        print(f"  - Reference photos: {Config.REFERENCE_IMAGE_DIR}")
        print(f"  - Output: {Config.OUTPUT_DIR}")

# Create directories on import
Config.setup_directories()
import subprocess
import sys
import os

def install_requirements():
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Requirements installed successfully!")

def create_sample_data():
    print("Creating sample directory structure...")
    os.makedirs("data/input", exist_ok=True)
    os.makedirs("data/reference", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)
    
    # Create a README in each folder
    with open("data/input/README.txt", "w") as f:
        f.write("Put your event photos here (jpg, png, etc.)")
    
    with open("data/reference/README.txt", "w") as f:
        f.write("Put your reference selfies here")
    
    print("Directory structure created!")
    print("Please add photos to:")
    print("  - data/input/ for event photos")
    print("  - data/reference/ for selfies")

if __name__ == "__main__":
    print("Setting up Intelligent Event Photo Retrieval System...")
    install_requirements()
    create_sample_data()
    print("\nSetup complete! Run the app with:")
    print("  streamlit run app.py")
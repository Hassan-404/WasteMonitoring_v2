from pathlib import Path
import sys

file_path = Path(__file__).resolve()

root_path = file_path.parent

if root_path not in sys.path:
    sys.path.append(str(root_path))

ROOT = root_path.relative_to(Path.cwd())

IMAGE = 'Image'
WEBCAM = 'Webcam'
SOURCES_LIST = [IMAGE, WEBCAM]

MODEL_DIR =  './weights/'
DETECTION_MODEL = MODEL_DIR+'yolov8.pt'

# Webcam
WEBCAM_PATH = 0

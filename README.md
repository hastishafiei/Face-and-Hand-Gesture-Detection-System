# Face and Hand Gesture Detection System

A real-time computer vision system that detects faces and hand gestures using Python, OpenCV, and MediaPipe. The system triggers an alert when a left hand fist gesture is detected.

## Features

- **Face Detection**: Detects and tracks faces in real-time
- **Hand Tracking**: Identifies and tracks up to 2 hands simultaneously
- **Gesture Recognition**: Detects fist gestures with high accuracy
- **Left/Right Hand Differentiation**: Distinguishes between left and right hands
- **Alert System**: Visual and console alerts when left hand fist is detected
- **Real-time Processing**: Smooth video processing at 30 FPS
- **Info Panel**: Live statistics showing detected faces, hands, and status

## Requirements

- Python 3.8 or higher
- Webcam (built-in or USB)
- Windows, Linux, or macOS

## Installation

### Windows

1. **Easy Setup** (Recommended):
   - Double-click `setup_windows.bat`
   - Wait for installation to complete

2. **Run the application**:
   - Double-click `run_windows.bat`

3. **Manual Setup** (Alternative):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

### Linux/macOS

1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Windows
Double-click `run_windows.bat` or run manually:
```cmd
venv\Scripts\activate
python main.py
```

### Linux/macOS
```bash
source venv/bin/activate
python main.py
```

### Controls

- **q**: Quit the application
- **s**: Take a screenshot

### How It Works

1. The system captures video from your webcam
2. Each frame is processed to detect:
   - Faces using MediaPipe Face Detection
   - Hands and finger positions using MediaPipe Hands
3. When a fist gesture is detected on the left hand:
   - A red border appears around the screen
   - An alert message is displayed
   - A console message is printed
4. The alert remains active for 2 seconds

## Technical Details

### Fist Detection Algorithm

A fist is detected when:
- All four fingers (index, middle, ring, pinky) are curled (fingertips below PIP joints)
- The thumb is curled close to the palm
- At least 3 out of 4 fingers meet the curl criteria

### Hand Classification

The system uses MediaPipe's built-in hand classification to distinguish between left and right hands.

## Project Structure

```
.
├── main.py              # Main application entry point
├── gesture_detector.py  # Core detection and processing logic
├── requirements.txt     # Python dependencies
├── setup_windows.bat    # Windows setup script
├── run_windows.bat      # Windows run script
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Deploying to Another Machine

**Files to copy:**
- `main.py`
- `gesture_detector.py`
- `requirements.txt`
- `setup_windows.bat` (for Windows)
- `run_windows.bat` (for Windows)
- `README.md` (optional)

**Do NOT copy:**
- `venv/` folder (machine-specific)
- `__pycache__/` folder (will be auto-generated)

On the new machine, run the setup script or follow the installation instructions above.

## Troubleshooting

**Camera not opening (Windows):**
- The application now automatically tries multiple camera indices and DirectShow backend
- Check if another application is using the camera (Skype, Teams, Zoom, etc.)
- Ensure camera drivers are installed
- Check Windows Privacy Settings → Camera permissions

**Camera not opening (Linux):**
- Check if another application is using the camera
- Verify camera permissions: `ls -l /dev/video*`
- Install v4l-utils: `sudo apt install v4l-utils`

**Low FPS:**
- Reduce camera resolution in `main.py`
- Close other resource-intensive applications

**False detections:**
- Ensure good lighting conditions
- Adjust `min_detection_confidence` in `gesture_detector.py`

## License

MIT License


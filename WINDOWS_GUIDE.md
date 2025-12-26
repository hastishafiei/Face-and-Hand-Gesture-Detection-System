===============================================================================
   FACE AND HAND GESTURE DETECTION - WINDOWS QUICK START GUIDE
===============================================================================

PREREQUISITES:
--------------
1. Python 3.8 or higher installed
   Download from: https://www.python.org/downloads/
   IMPORTANT: Check "Add Python to PATH" during installation!

2. Webcam connected (built-in laptop camera or USB webcam)

3. Camera permissions enabled in Windows Settings

MANUAL INSTALLATION :
----------------------------------
If setup_windows.bat doesn't work:

1. Open Command Prompt in project folder
2. Run these commands:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python main.py

HOW TO TEST:
-----------
1. Position yourself in front of the camera
2. Make sure your face and hands are visible
3. Make a FIST with your LEFT hand
4. You should see:
   - Red border around the screen
   - "ALERT: FIST DETECTED!" message
   - Console message printed

TROUBLESHOOTING:
---------------

Problem: "Python is not installed or not in PATH"
Solution: Install Python from python.org and check "Add to PATH"

Problem: "Could not open camera"
Solution:
  - Close other apps using camera (Skype, Teams, Zoom)
  - Check Windows Settings → Privacy → Camera
  - Make sure camera is enabled for desktop apps
  - Try unplugging and reconnecting USB camera

Problem: Camera opens but no detection
Solution:
  - Ensure good lighting
  - Move closer to camera
  - Make sure hands are visible in frame

Problem: Detection is slow/laggy
Solution:
  - Close other programs
  - Reduce camera resolution (edit main.py line 61-62)

===============================================================================
                           ENJOY DETECTING GESTURES!
===============================================================================

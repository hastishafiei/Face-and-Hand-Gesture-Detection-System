
"""
Face and Hand Gesture Detection System
Detects faces and hand gestures in real-time video feed.
Triggers an alert when a left hand fist is detected.

Cross-platform compatible: Windows, Linux, macOS
"""
import cv2
import sys
from gesture_detector import GestureDetector


def main():
    """Main function to run the gesture detection system."""
    print("="*60)
    print("Face and Hand Gesture Detection System")
    print("="*60)
    print("\nInstructions:")
    print("- The system will detect your face and hands")
    print("- Make a fist with your LEFT hand to trigger an alert")
    print("- Press 'q' to quit")
    print("- Press 's' to take a screenshot")
    print("\nStarting camera...")
    print("="*60 + "\n")

    # Initialize the gesture detector
    detector = GestureDetector()

    # Initialize webcam
    # Try different camera indices (Windows may use DirectShow backend)
    cap = None
    for camera_index in [0, 1, 2]:
        print(f"Trying camera index {camera_index}...")
        test_cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # DirectShow for Windows
        if test_cap.isOpened():
            cap = test_cap
            print(f"Successfully opened camera at index {camera_index}")
            break
        test_cap.release()

    # If DirectShow fails, try default backend
    if cap is None:
        print("DirectShow failed, trying default backend...")
        for camera_index in [0, 1, 2]:
            test_cap = cv2.VideoCapture(camera_index)
            if test_cap.isOpened():
                cap = test_cap
                print(f"Successfully opened camera at index {camera_index}")
                break
            test_cap.release()

    if cap is None or not cap.isOpened():
        print("Error: Could not open camera")
        print("Please ensure:")
        print("- Camera is connected and powered on")
        print("- No other application is using the camera")
        print("- Camera drivers are installed (Windows)")
        sys.exit(1)

    # Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    frame_count = 0
    screenshot_count = 0

    try:
        while True:
            # Read frame from camera
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame")
                break

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)

            # Process the frame
            processed_frame, detection_info = detector.process_frame(frame)

            # Display frame count
            frame_count += 1
            cv2.putText(
                processed_frame,
                f"Frame: {frame_count}",
                (processed_frame.shape[1] - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

            # Display the frame
            cv2.imshow('Gesture Detection System', processed_frame)


            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            # Check if window was closed with X button (must be after waitKey)
            try:
                window_prop = cv2.getWindowProperty('Gesture Detection System', cv2.WND_PROP_VISIBLE)
                if window_prop < 1:
                    print("\nWindow closed by user...")
                    break
            except cv2.error:
                print("\nWindow closed by user...")
                break
           
            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord('s'):
                # Save screenshot
                screenshot_count += 1
                filename = f"screenshot_{screenshot_count}.png"
                cv2.imwrite(filename, processed_frame)
                print(f"Screenshot saved: {filename}")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")

    finally:
        # Cleanup
        print("\nCleaning up...")
        cap.release()
        cv2.destroyAllWindows()
        detector.cleanup()
        print("Done!")


if __name__ == "__main__":
    main()

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Optional, List
import time


class GestureDetector:
    """
    A class to detect faces and hand gestures using MediaPipe and OpenCV.
    Specifically designed to detect fist gestures and trigger alerts.
    """

    def __init__(self):
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=0.5
        )

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Drawing utilities
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Alert state management
        self.alert_active = False
        self.alert_start_time = 0
        self.alert_duration = 2  # seconds

    def is_fist(self, hand_landmarks) -> bool:
        """
        Detect if the hand is making a fist gesture.
        A fist is detected when all fingertips are below their respective PIP joints.

        Args:
            hand_landmarks: MediaPipe hand landmarks

        Returns:
            bool: True if hand is making a fist, False otherwise
        """
        # Get landmark coordinates
        landmarks = hand_landmarks.landmark

        # Finger tip and PIP joint indices
        # Thumb: tip=4, IP=3
        # Index: tip=8, PIP=6
        # Middle: tip=12, PIP=10
        # Ring: tip=16, PIP=14
        # Pinky: tip=20, PIP=18

        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
        finger_pips = [6, 10, 14, 18]

        # Check if all fingers are curled (tips below PIPs in y-coordinate)
        fingers_curled = 0
        for tip, pip in zip(finger_tips, finger_pips):
            # Y increases downward in image coordinates
            if landmarks[tip].y > landmarks[pip].y:
                fingers_curled += 1

        # Check thumb separately (different orientation)
        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]
        thumb_mcp = landmarks[2]

        # Thumb is curled if tip is close to palm (comparing x-coordinates)
        thumb_curled = abs(thumb_tip.x - thumb_mcp.x) < abs(landmarks[5].x - thumb_mcp.x)

        # Fist detected if at least 3 fingers are curled and thumb is curled
        return fingers_curled >= 3 and thumb_curled

    def is_left_hand(self, hand_landmarks, image_width: int) -> bool:
        """
        Determine if the detected hand is the left hand.
        Uses the wrist and middle finger MCP positions.

        Args:
            hand_landmarks: MediaPipe hand landmarks
            image_width: Width of the image

        Returns:
            bool: True if left hand, False if right hand
        """
        # Get wrist position
        wrist = hand_landmarks.landmark[0]
        # Get middle finger MCP (base)
        middle_mcp = hand_landmarks.landmark[9]

        # Simple heuristic: if hand is on the left side of the image
        # and palm faces camera, it's likely the left hand
        hand_center_x = wrist.x

        return hand_center_x < 0.5

    def trigger_alert(self):
        """Activate the alert state."""
        self.alert_active = True
        self.alert_start_time = time.time()
        print("\n" + "="*50)
        print("ALERT: LEFT HAND FIST DETECTED!")
        print("="*50 + "\n")

    def check_alert_timeout(self):
        """Check if alert should be deactivated."""
        if self.alert_active:
            if time.time() - self.alert_start_time > self.alert_duration:
                self.alert_active = False

    def draw_alert_overlay(self, image: np.ndarray) -> np.ndarray:
        """
        Draw alert overlay on the image.

        Args:
            image: Input image

        Returns:
            Image with alert overlay
        """
        if self.alert_active:
            # Create semi-transparent red overlay
            overlay = image.copy()
            height, width = image.shape[:2]

            # Draw red border
            cv2.rectangle(overlay, (0, 0), (width, height), (0, 0, 255), 30)

            # Add alert text
            alert_text = "ALERT: FIST DETECTED!"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.5
            thickness = 3

            # Get text size
            (text_width, text_height), baseline = cv2.getTextSize(
                alert_text, font, font_scale, thickness
            )

            # Position text at top center
            text_x = (width - text_width) // 2
            text_y = 80

            # Draw background rectangle for text
            cv2.rectangle(
                overlay,
                (text_x - 10, text_y - text_height - 10),
                (text_x + text_width + 10, text_y + 10),
                (0, 0, 255),
                -1
            )

            # Draw text
            cv2.putText(
                overlay,
                alert_text,
                (text_x, text_y),
                font,
                font_scale,
                (255, 255, 255),
                thickness
            )

            # Blend overlay with original image
            cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)

        return image

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, dict]:
        """
        Process a single frame to detect faces and hand gestures.

        Args:
            frame: Input frame from camera

        Returns:
            Tuple of (processed_frame, detection_info)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape

        detection_info = {
            'faces_detected': 0,
            'hands_detected': 0,
            'left_fist_detected': False
        }

        # Detect faces
        face_results = self.face_detection.process(rgb_frame)
        if face_results.detections:
            detection_info['faces_detected'] = len(face_results.detections)
            for detection in face_results.detections:
                self.mp_drawing.draw_detection(frame, detection)

        # Detect hands
        hand_results = self.hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks:
            detection_info['hands_detected'] = len(hand_results.multi_hand_landmarks)

            for idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                # Draw hand landmarks
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )

                # Check if it's a fist
                is_fist = self.is_fist(hand_landmarks)
                is_left = self.is_left_hand(hand_landmarks, width)

                # Get hand label from MediaPipe results
                if hand_results.multi_handedness:
                    hand_label = hand_results.multi_handedness[idx].classification[0].label

                    # Draw hand label
                    wrist = hand_landmarks.landmark[0]
                    label_x = int(wrist.x * width)
                    label_y = int(wrist.y * height) - 20

                    label_text = f"{hand_label}"
                    if is_fist:
                        label_text += " - FIST"

                    cv2.putText(
                        frame,
                        label_text,
                        (label_x, label_y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0) if not is_fist else (0, 0, 255),
                        2
                    )

                    # Trigger alert if left hand fist detected
                    if hand_label == "Left" and is_fist:
                        detection_info['left_fist_detected'] = True
                        self.trigger_alert()

        # Check alert timeout
        self.check_alert_timeout()

        # Draw alert overlay
        frame = self.draw_alert_overlay(frame)

        # Draw info panel
        self.draw_info_panel(frame, detection_info)

        return frame, detection_info

    def draw_info_panel(self, frame: np.ndarray, info: dict):
        """
        Draw information panel on the frame.

        Args:
            frame: Input frame
            info: Detection information dictionary
        """
        y_offset = 30
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2

        # Draw background for info panel
        cv2.rectangle(frame, (10, 10), (300, 100), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (300, 100), (255, 255, 255), 2)

        # Draw info text
        cv2.putText(
            frame,
            f"Faces: {info['faces_detected']}",
            (20, y_offset),
            font,
            font_scale,
            (255, 255, 255),
            thickness
        )

        y_offset += 30
        cv2.putText(
            frame,
            f"Hands: {info['hands_detected']}",
            (20, y_offset),
            font,
            font_scale,
            (255, 255, 255),
            thickness
        )

        y_offset += 30
        status_color = (0, 255, 0) if not info['left_fist_detected'] else (0, 0, 255)
        cv2.putText(
            frame,
            f"Status: {'ALERT!' if info['left_fist_detected'] else 'Normal'}",
            (20, y_offset),
            font,
            font_scale,
            status_color,
            thickness
        )

    def cleanup(self):
        """Release resources."""
        self.face_detection.close()
        self.hands.close()
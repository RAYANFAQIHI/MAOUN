import math  # Import math library for mathematical functions
import numpy as np  # Import NumPy for numerical operations
import cv2  # Import OpenCV for image processing
from .pupil import Pupil  # Import the Pupil class from the current package

class Eye(object):
    """
    This class handles creating a new frame to isolate the eye and
    kicks off the pupil detection process.
    """

    LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]  # Points representing the left eye landmarks
    RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]  # Points representing the right eye landmarks

    def __init__(self, original_frame, landmarks, side, calibration):
        self.frame = None  # Will hold the isolated eye frame
        self.origin = None  # Will store the origin coordinates of the eye in the frame
        self.center = None  # Will store the center coordinates of the eye frame
        self.pupil = None  # Will hold the detected pupil information
        self.landmark_points = None  # Will store the eye's landmark points

        # Start analyzing the eye by isolating it and detecting the pupil
        self._analyze(original_frame, landmarks, side, calibration)

    @staticmethod
    def _middle_point(p1, p2):
        """Get the middle point between two points.

        Args:
            p1 (dlib.point): First point
            p2 (dlib.point): Second point
        """
        x = int((p1.x + p2.x) / 2)
        y = int((p1.y + p2.y) / 2)
        return (x, y)

    def _isolate(self, frame, landmarks, points):
        """Isolate the eye region from the rest of the face.

        Args:
            frame (numpy.ndarray): The image frame containing the face
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            points (list): Points representing the eye landmarks
        """
        # Get the coordinates of the eye region
        region = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in points])
        region = region.astype(np.int32)
        self.landmark_points = region

        # Create a mask to isolate the eye
        height, width = frame.shape[:2]
        black_frame = np.zeros((height, width), np.uint8)
        mask = np.full((height, width), 255, np.uint8)
        cv2.fillPoly(mask, [region], (0, 0, 0))
        eye = cv2.bitwise_not(black_frame, frame.copy(), mask=mask)

        # Crop the frame to the eye region with a small margin
        margin = 5
        min_x = np.min(region[:, 0]) - margin
        max_x = np.max(region[:, 0]) + margin
        min_y = np.min(region[:, 1]) - margin
        max_y = np.max(region[:, 1]) + margin

        self.frame = eye[min_y:max_y, min_x:max_x]  # The isolated eye frame
        self.origin = (min_x, min_y)  # The origin point of the eye in the frame

        # Calculate the center of the isolated eye frame
        height, width = self.frame.shape[:2]
        self.center = (width / 2, height / 2)

    def _blinking_ratio(self, landmarks, points):
        """Calculate a ratio to determine if the eye is blinking.

        This ratio is the width of the eye divided by its height.

        Args:
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            points (list): Points representing the eye landmarks

        Returns:
            float: The blinking ratio
        """
        left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
        right = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)
        top = self._middle_point(landmarks.part(points[1]), landmarks.part(points[2]))
        bottom = self._middle_point(landmarks.part(points[5]), landmarks.part(points[4]))

        eye_width = math.hypot((left[0] - right[0]), (left[1] - right[1]))  # Width of the eye
        eye_height = math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))  # Height of the eye

        try:
            ratio = eye_width / eye_height  # Blinking ratio
        except ZeroDivisionError:
            ratio = None  # In case of division by zero

        return ratio

    def _analyze(self, original_frame, landmarks, side, calibration):
        """Isolate the eye in a new frame, handle calibration, and detect the pupil.

        Args:
            original_frame (numpy.ndarray): The original frame from the webcam
            landmarks (dlib.full_object_detection): Facial landmarks for the face region
            side (int): 0 for the left eye, 1 for the right eye
            calibration (calibration.Calibration): The calibration object to manage threshold values
        """
        if side == 0:
            points = self.LEFT_EYE_POINTS  # Use left eye points
        elif side == 1:
            points = self.RIGHT_EYE_POINTS  # Use right eye points
        else:
            return

        # Calculate blinking ratio
        self.blinking = self._blinking_ratio(landmarks, points)
        # Isolate the eye in the frame
        self._isolate(original_frame, landmarks, points)

        # Evaluate calibration if not complete
        if not calibration.is_complete():
            calibration.evaluate(self.frame, side)

        # Get the threshold value and detect the pupil
        threshold = calibration.threshold(side)
        self.pupil = Pupil(self.frame, threshold)

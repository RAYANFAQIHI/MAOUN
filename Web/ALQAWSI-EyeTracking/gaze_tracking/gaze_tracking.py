import os  # To handle file paths and operations
import cv2  # For computer vision tasks
import dlib  # For facial landmark detection
from .eye import Eye  # Importing the Eye class from the same package
from .calibration import Calibration  # Importing the Calibration class from the same package

class GazeTracking(object):
    """
    This class tracks where you're looking. It can tell you about the position
    of your eyes and pupils, and whether your eyes are open or closed.
    """

    def __init__(self):
        self.frame = None  # This will store the frame captured from the webcam
        self.eye_left = None  # This will store the left eye object
        self.eye_right = None  # This will store the right eye object
        self.calibration = Calibration()  # Initializes the calibration for pupil detection

        # This detector will find faces in the frame
        self._face_detector = dlib.get_frontal_face_detector()

        # This predictor will find the facial landmarks on the detected face
        cwd = os.path.abspath(os.path.dirname(__file__))  # Get the current working directory
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)  # Load the facial landmark model

    @property
    def pupils_located(self):
        """Checks if the pupils have been found"""
        try:
            int(self.eye_left.pupil.x)  # Check if left pupil x-coordinate is valid
            int(self.eye_left.pupil.y)  # Check if left pupil y-coordinate is valid
            int(self.eye_right.pupil.x)  # Check if right pupil x-coordinate is valid
            int(self.eye_right.pupil.y)  # Check if right pupil y-coordinate is valid
            return True  # If all are valid, pupils are located
        except Exception:
            return False  # If any are not valid, pupils are not located

    def _analyze(self):
        """Detects the face and initializes Eye objects for left and right eyes"""
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
        faces = self._face_detector(frame)  # Detect faces in the frame

        try:
            landmarks = self._predictor(frame, faces[0])  # Get the facial landmarks for the first detected face
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)  # Initialize the left eye
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)  # Initialize the right eye

        except IndexError:
            self.eye_left = None  # If no face is detected, set left eye to None
            self.eye_right = None  # If no face is detected, set right eye to None

    def refresh(self, frame):
        """Updates the frame and analyzes it.

        Args:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame  # Update the frame
        self._analyze()  # Analyze the new frame

    def pupil_left_coords(self):
        """Gives the coordinates of the left pupil"""
        if self.pupils_located:  # Check if pupils are located
            x = self.eye_left.origin[0] + self.eye_left.pupil.x  # Calculate x-coordinate
            y = self.eye_left.origin[1] + self.eye_left.pupil.y  # Calculate y-coordinate
            return (x, y)  # Return the coordinates

    def pupil_right_coords(self):
        """Gives the coordinates of the right pupil"""
        if self.pupils_located:  # Check if pupils are located
            x = self.eye_right.origin[0] + self.eye_right.pupil.x  # Calculate x-coordinate
            y = self.eye_right.origin[1] + self.eye_right.pupil.y  # Calculate y-coordinate
            return (x, y)  # Return the coordinates

    def horizontal_ratio(self):
        """Gives a number between 0.0 and 1.0 that shows the horizontal direction of the gaze.
        Looking far right is 0.0, center is 0.5, and far left is 1.0.
        """
        if self.pupils_located:  # Check if pupils are located
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)  # Calculate left pupil ratio
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)  # Calculate right pupil ratio
            return (pupil_left + pupil_right) / 2  # Average the ratios

    def vertical_ratio(self):
        """Gives a number between 0.0 and 1.0 that shows the vertical direction of the gaze.
        Looking far up is 0.0, center is 0.5, and far down is 1.0.
        """
        if self.pupils_located:  # Check if pupils are located
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)  # Calculate left pupil ratio
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)  # Calculate right pupil ratio
            return (pupil_left + pupil_right) / 2  # Average the ratios

    def is_right(self):
        """Returns true if the user is looking to the right"""
        if self.pupils_located:  # Check if pupils are located
            return self.horizontal_ratio() <= 0.35  # Check if looking right

    def is_left(self):
        """Returns true if the user is looking to the left"""
        if self.pupils_located:  # Check if pupils are located
            return self.horizontal_ratio() >= 0.65  # Check if looking left

    def is_center(self):
        """Returns true if the user is looking to the center"""
        if self.pupils_located:  # Check if pupils are located
            return not self.is_right() and not self.is_left()  # Check if not looking left or right

    def is_blinking(self):
        """Returns true if the user is blinking"""
        if self.pupils_located:  # Check if pupils are located
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2  # Calculate blinking ratio
            return blinking_ratio > 3.8  # Check if blinking ratio indicates blinking

    def annotated_frame(self):
        """Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()  # Make a copy of the frame

        if self.pupils_located:  # Check if pupils are located
            color = (0, 255, 0)  # Color for the annotation (green)
            x_left, y_left = self.pupil_left_coords()  # Get left pupil coordinates
            x_right, y_right = self.pupil_right_coords()  # Get right pupil coordinates
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)  # Draw cross on left pupil
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)  # Draw cross on right pupil
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)

        return frame  # Return the annotated frame

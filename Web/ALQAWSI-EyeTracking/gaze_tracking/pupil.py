import numpy as np  # For numerical operations
import cv2  # For computer vision tasks

class Pupil(object):
    """
    This class is responsible for detecting the iris of an eye and estimating
    the position of the pupil.
    """

    def __init__(self, eye_frame, threshold):
        self.iris_frame = None  # This will store the processed frame containing the iris
        self.threshold = threshold  # Threshold value for binarization
        self.x = None  # X-coordinate of the pupil
        self.y = None  # Y-coordinate of the pupil

        self.detect_iris(eye_frame)  # Start the iris detection process

    @staticmethod
    def image_processing(eye_frame, threshold):
        """Processes the eye frame to isolate the iris.

        Args:
            eye_frame (numpy.ndarray): Frame that only contains the eye
            threshold (int): Threshold value for binarizing the frame

        Returns:
            numpy.ndarray: A frame where the iris is isolated
        """
        # Create a kernel for morphological operations
        kernel = np.ones((3, 3), np.uint8)
        
        # Apply bilateral filter to reduce noise and keep edges sharp
        new_frame = cv2.bilateralFilter(eye_frame, 10, 15, 15)
        
        # Erode the image to remove small white noise and detach connected objects
        new_frame = cv2.erode(new_frame, kernel, iterations=3)
        
        # Binarize the frame using the given threshold
        new_frame = cv2.threshold(new_frame, threshold, 255, cv2.THRESH_BINARY)[1]

        return new_frame  # Return the processed frame

    def detect_iris(self, eye_frame):
        """Detects the iris and estimates its position by calculating the centroid.

        Args:
            eye_frame (numpy.ndarray): Frame that only contains the eye
        """
        # Process the frame to isolate the iris
        self.iris_frame = self.image_processing(eye_frame, self.threshold)

        # Find contours in the processed frame
        contours, _ = cv2.findContours(self.iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        contours = sorted(contours, key=cv2.contourArea)  # Sort contours by area

        try:
            # Get the moments of the largest contour
            moments = cv2.moments(contours[-2])
            
            # Calculate the x and y coordinates of the centroid
            self.x = int(moments['m10'] / moments['m00'])
            self.y = int(moments['m01'] / moments['m00'])
        except (IndexError, ZeroDivisionError):
            pass  # Handle cases where moments can't be calculated

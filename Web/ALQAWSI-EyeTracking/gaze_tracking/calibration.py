from __future__ import division  # Ensure division in Python 2 behaves like Python 3
import cv2  # Import the OpenCV library for image processing
from .pupil import Pupil  # Import the Pupil class from the current package

class Calibration(object):
    """
    This class helps calibrate the pupil detection algorithm by finding the
    best position of them on webcam
    """

    def __init__(self):
        self.nb_frames = 20  # Number of frames needed to complete calibration
        self.thresholds_left = []  # List to store threshold values for the left eye
        self.thresholds_right = []  # List to store threshold values for the right eye

    def is_complete(self):
        """Check if calibration is done by seeing if we've processed enough frames."""
        return len(self.thresholds_left) >= self.nb_frames and len(self.thresholds_right) >= self.nb_frames

    def threshold(self, side):
        """Get the threshold value for the given eye (left or right).

        Args:
            side: 0 for the left eye, 1 for the right eye
        """
        if side == 0:
            # Calculate the average threshold for the left eye
            return int(sum(self.thresholds_left) / len(self.thresholds_left))
        elif side == 1:
            # Calculate the average threshold for the right eye
            return int(sum(self.thresholds_right) / len(self.thresholds_right))

    @staticmethod
    def iris_size(frame):
        """Calculate what percentage of the eye's surface is covered by the iris.

        Args:
            frame (numpy.ndarray): A binarized image of the iris
        """
        # Crop the frame to remove the borders
        frame = frame[5:-5, 5:-5]
        height, width = frame.shape[:2]
        nb_pixels = height * width  # Total number of pixels in the frame
        nb_blacks = nb_pixels - cv2.countNonZero(frame)  # Number of black pixels (iris area)
        return nb_blacks / nb_pixels  # Percentage of the frame covered by the iris

    @staticmethod
    def find_best_threshold(eye_frame):
        """Find the best threshold to binarize the eye image.

        Args:
            eye_frame (numpy.ndarray): The image of the eye to analyze
        """
        average_iris_size = 0.48  # Expected average size of the iris in the eye image
        trials = {}  # Dictionary to store the iris size for different threshold values

        # Try different threshold values from 5 to 95 in steps of 5
        for threshold in range(5, 100, 5):
            iris_frame = Pupil.image_processing(eye_frame, threshold)  # Process the image with the current threshold
            trials[threshold] = Calibration.iris_size(iris_frame)  # Store the iris size for the current threshold

        # Find the threshold that makes the iris size closest to the average iris size
        best_threshold, iris_size = min(trials.items(), key=(lambda p: abs(p[1] - average_iris_size)))
        return best_threshold

    def evaluate(self, eye_frame, side):
        """Improve calibration by using the given eye image.

        Args:
            eye_frame (numpy.ndarray): The image of the eye
            side: 0 for the left eye, 1 for the right eye
        """
        threshold = self.find_best_threshold(eye_frame)  # Find the best threshold for the current eye image

        if side == 0:
            self.thresholds_left.append(threshold)  # Add the threshold to the left eye's list
        elif side == 1:
            self.thresholds_right.append(threshold)  # Add the threshold to the right eye's list

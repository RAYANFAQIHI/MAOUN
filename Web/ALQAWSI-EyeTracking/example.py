

import cv2  # Import the OpenCV library for computer vision tasks
from gaze_tracking import GazeTracking  # Import the GazeTracking library

gaze = GazeTracking()  # Create an instance of the GazeTracking class
webcam = cv2.VideoCapture(0)  # Open a connection to the default webcam

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()  # Read a frame from the webcam

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)  # Analyze the frame using the GazeTracking library

    frame = gaze.annotated_frame()  # Get the annotated frame with gaze information
    text = ""  # Initialize an empty string for the status text

    if gaze.is_blinking():
        text = "Blinking"  # Set text to "Blinking" if the user is blinking
    elif gaze.is_right():
        text = "Looking right"  # Set text to "Looking right" if the user is looking right
    elif gaze.is_left():
        text = "Looking left"  # Set text to "Looking left" if the user is looking left
    elif gaze.is_center():
        text = "Looking center"  # Set text to "Looking center" if the user is looking center

    # Display the gaze status text on the frame in red
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 0, 255), 2)

    left_pupil = gaze.pupil_left_coords()  # Get the coordinates of the left pupil
    right_pupil = gaze.pupil_right_coords()  # Get the coordinates of the right pupil

    # Display the left pupil coordinates on the frame in red
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 1)
    # Display the right pupil coordinates on the frame in red
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 1)

    # Show the annotated frame in a window named "ALQAWSI"
    cv2.imshow("ALQAWSI", frame)

    # Break the loop if the 'Esc' key is pressed
    if cv2.waitKey(1) == 27:
        break

webcam.release()  # Release the webcam resource
cv2.destroyAllWindows()  # Close all OpenCV windows

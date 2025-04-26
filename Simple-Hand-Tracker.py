import mediapipe
import cv2

# Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

# Use CV2 Functionality to create a Video stream and add some values
cap = cv2.VideoCapture(0)  # Change index if you have multiple cameras

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

# Add confidence values and extra settings to MediaPipe hand tracking
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        
        # Resize the frame to a desired size for faster processing
        frame1 = cv2.resize(frame, (640, 480))
        
        # Process the frame using MediaPipe for hand detection
        results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
        
        # Check if hands are detected
        if results.multi_hand_landmarks is not None:
            for handLandmarks in results.multi_hand_landmarks:
                # Draw landmarks on the frame
                drawingModule.draw_landmarks(frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
                
        # Show the current frame to the desktop
        cv2.imshow("Frame", frame1)
        
        # If 'q' is pressed, exit the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

# Release the capture object and close any open windows
cap.release()
cv2.destroyAllWindows()

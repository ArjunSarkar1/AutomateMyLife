# Installations Required
# pip install opencv-python
# Usage: computer vision, image processing and machine learning!

#Others Requirement:
# Python3
# Enbaling VS-Code to access Systems Events

import os, datetime, cv2 as cv

reset = False

def detectFace():
    # `video = cv.VideoCapture(0)` is creating a `VideoCapture` object that captures video from the
    # default camera (index 0). This object is used to read frames from the video stream.
    video = cv.VideoCapture(0)
    
    # harracascade classifier that detects face
    # The line `face_cascade = cv.CascadeClassifier(cv.data.harracascades +
    # 'haarcascade_frontalface_default.xml')` is creating an instance of the `CascadeClassifier` class
    # from the OpenCV library. It is used to detect faces in an image or video frame using the Haar
    # cascade classifier. The `haarcascade_frontalface_default.xml` file contains the trained data for
    # detecting frontal faces.
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    faceDetectionList = []
    
    playVid = True
    
    while playVid:
        detect, frame = video.read()

        if not detect:
            print("Error in reading video...")
            break
        
        # converting frame to grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # The line `faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
        # minSize=(50, 50))` is using the `detectMultiScale` method of the `CascadeClassifier` class
        # to detect faces in the grayscale image.
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        
        # print("Number of faces detected:", len(faces))
        
        # draws a rectangle around the face
        # for (x, y, w, h) in faces:
        #     cv.rectangle(frame, (x, y), (x+w, y+h), (255, 199, 0), 5)     
        
        if len(faces) > 0:
            faceDetectionList.append(True)
        else:
            faceDetectionList.append(False)
        
        faceChecker(faceDetectionList)
        
        # Checking to see if it detects face using boolean value
        # print(listDetection[-1])
        
        # The line `cv.imshow("Recording...", frame)` is displaying the current frame of the video with a
        # window title "Recording...". It is used to show the video feed in real-time while the face detection
        # is being performed.
        # cv.imshow("Recording...", frame)
        
        if cv.waitKey(10) == ord("q"):
            playVid = False
    
    video.release()
    cv.destroyAllWindows()
    
def faceChecker(listDetection):
    global reset
    
    latestChecks = 15
    
    if len(listDetection) > latestChecks:
    
        theLastCheck = listDetection[-1] 
        
        # extracting the last 15 elements
        lastChecks = listDetection[-latestChecks:]
        
        lastAllSame = True
        for elem in lastChecks:
            if elem != theLastCheck:
                lastAllSame = False
                break
        
        if lastAllSame and (theLastCheck == reset):
            if not reset:
                decreaseBrightness()
                reset = True
                
            elif reset:
                adaptBrightness()
                reset = False
    
def increaseBrightness():
   """Increases screen brightness all the way"""
   script = f"""
        tell application "System Events"
            repeat 33 times
                key code 144
            end repeat
        end tell
    """
   os.system(f"osascript -e '{script}'")


def decreaseBrightness():
   """Decreases screen brightness all the way"""
   script = f"""
        tell application "System Events"
            repeat 33 times
                key code 145
            end repeat
        end tell
    """
   os.system(f"osascript -e '{script}'")


def adaptBrightness():
   """Sets brightness according to the time of day"""
  
   currentTime = datetime.datetime.now().hour

   if 6 < currentTime < 18: # between 6am to 6pm
       setBrightness(60) # day time
   else:
       setBrightness(30) # night time


def setBrightness(level):
   """
   Adjusts screen brightness based on user input.

   Parameters:
   - brightness_level (int): The desired brightness level (0-100).
   """
   if not (0 <= level <= 100):
       print("Error: Brightness level should be between 0 and 100.")
       return

   # Convert the brightness level to the corresponding key code
   key_code = int(level * 32 / 100)

   # Executing apple script to set brightness
   script = f"""
        tell application "System Events"
            repeat {key_code} times
                key code 144
            end repeat
        end tell
   """
   os.system(f"osascript -e '{script}'")


detectFace()
# if __name__ == "__main__":
#    while True:       
#        action = input('Enter "i", "d", or "a": ')
#        if action == "i":
#            increaseBrightness()
#        elif action == "d":
#            decreaseBrightness()
#        elif action == "a":
#             adaptBrightness()
#        else :
#            print("\nExiting...")
#            quit()
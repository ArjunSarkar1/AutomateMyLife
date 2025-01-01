from datetime import datetime
import pyautogui
import subprocess
import time
import pandas
import os
import csv

# Specify the path to the Zoom application on your macOS
zoom_path = '/Applications/zoom.us.app'

current_directory = os.getcwd()
relative_csv_path = 'info.csv'
# Joining the current directory and the relative path to get the absolute path to the CSV file
csv_path = os.path.join(current_directory, relative_csv_path)

dates_and_times = []
meeting_ids = []
meeting_passcodes = []
meeting_links = []

def main():
    # Get the current date and time.
    date = datetime.now().date() 
    time = datetime.now().strftime("%I:%M:%S %p")
    print("\nCurrent Session: ["+ str(date) +"] - ["+ str(time) + "]\n")

    #######################
    meetID = 89449378598
    passcode = "codepath"
    #######################
    
    print("Meeting Infromation: \n")
    print("Accessing meeting with ID: "+ str(meetID) +" and Passcode: "+ passcode + " .....")
    # readCSVFile(relative_csv_path)
    # getTodayMeetings(relative_csv_path)
    openZoom()
    joinMeeting(str(meetID),str(passcode))

def getTodayMeetings(csv_path):
    global dates_and_times, meeting_ids, meeting_passcodes, meeting_links
    
    today_date = datetime.today().strftime('%Y-%m-%d')
    curr_meet_counter = 0

    if os.path.getsize(csv_path) > 0:
        with open(csv_path, 'r') as file:
            csv_reader = csv.reader(file)

            # Skipping the header row
            next(csv_reader, None)

            # Iterate over the remaining rows
            for row in csv_reader:
                row_date = row[0]
                row_date_obj = datetime.strptime(row_date, '%Y-%m-%d %H:%M:%S')

                # Check if the row date matches today's date
                if row_date.startswith(today_date) and row_date_obj.time() > datetime.now().time():
                    curr_meet_counter += 1
                    if curr_meet_counter == 1:
                        print("\n[ Meeting(s) for today ]\n")
                    print("Meeting "+str(curr_meet_counter)+":")
                    print(f"Date and Time: {row[0]}")
                    print(f"Meeting ID: {row[1]}")
                    print(f"Meeting Passcode: {row[2]}")
                    print(f"Meeting Link: {row[3] if row[3].strip() else None}")
                    print()
        
        if curr_meet_counter == 0:
            print("\n[ No meetings found for today ] \n")
    else:
        print("\n[ The CSV file is empty ]\n")

def readCSVFile(path):
    global dates_and_times, meeting_ids, meeting_passcodes, meeting_links
    # Read the CSV file into a pandas DataFrame
    df = pandas.read_csv(path)

    # Now you can access the columns as follows:
    dates_and_times = df['date_and_time'].tolist()
    meeting_ids = df['meeting_id'].tolist()
    meeting_passcodes = df['meeting_passcode'].tolist()
    meeting_links = df['meeting_link'].tolist()

    for i in range(len(dates_and_times)):
        print("\nDate and Time: " + dates_and_times[i])
        print("Meeting ID: " + str(meeting_ids[i]))
        print("Meeting Passcode: " + str(meeting_passcodes[i]))
        print("Meeting Link: " + str(meeting_links[i]) if pandas.notna(meeting_links[i]) else "Meeting Link: None")

def openZoom():
    """Open the Zoom app."""
    try: 
        # Open Zoom using subprocess
        # userName = input("Enter preferred user name: ")
        subprocess.run(['open', zoom_path])
        print("Opening Zoom...")
        time.sleep(3)
        print("Zoom opened.")

    except Exception as e:
        print(f"An error occurred: {e}")

def joinMeeting(meeting_ID, meeting_password):
    """Join a meeting by entering the meeting number and passcode"""
    try:
        x,y = pyautogui.locateCenterOnScreen('join-a-meeting.png')
        pyautogui.moveTo(x/2,y/2,0.5)
        pyautogui.click()
        print("Clicked on the Join Meeting button.")
        time.sleep(0.5)
        
        # Meeting Info
        # meeting_ID = "599 964 5575"
        # meeting_password = "R79xbj"

        meetX,meetY = pyautogui.locateCenterOnScreen('meetingID.png')
        pyautogui.moveTo(meetX/2,meetY/2,0.3)
        pyautogui.click()
        pyautogui.typewrite(meeting_ID)
        time.sleep(0.2)
        print("Clicked on the Meeting ID.")
    except pyautogui.ImageNotFoundException:
        print("Error: 'meetingID' image not found.")
    
    try:
        locX,locY = pyautogui.locateCenterOnScreen('audio.png')
        pyautogui.moveTo(locX/2,locY/2,0.2)
        pyautogui.click()
        time.sleep(0.2)
        print("Checked off don't connect to audio.")
    except pyautogui.ImageNotFoundException:
        print("Error: 'audio.png' image not found.")
    
    try:
        locX1,locY1 = pyautogui.locateCenterOnScreen('video.png')
        pyautogui.moveTo(locX1/2,locY1/2,0.2)
        pyautogui.click()
        time.sleep(0.2)
        print("Checked off don't show video.")
    except pyautogui.ImageNotFoundException:
        print("Error: 'video.png' image not found.")

    try:
        locX2,locY2 = pyautogui.locateCenterOnScreen('join.png')
        pyautogui.moveTo(locX2/2,locY2/2,0.2)
        pyautogui.click()
        time.sleep(0.5)
        print("Clicked joined button.")
    except pyautogui.ImageNotFoundException:
        print("Error: 'join.png' image not found.")

    try:
        locX3, locY3 = pyautogui.locateCenterOnScreen('pass.png')
        pyautogui.moveTo(locX3/2,locY3/2)
        pyautogui.click()
        pyautogui.typewrite(meeting_password)
        time.sleep(0.2)
        print("Entered meeting password button.")
    except pyautogui.ImageNotFoundException:
        print("Error: 'pass.png' image not found.")

    try:
        locX4,locY4 = pyautogui.locateCenterOnScreen('joinn.png')
        pyautogui.moveTo(locX4/2,locY4/2,0.2)
        pyautogui.click()
        time.sleep(0.2)
        print("Clicked joined button.")
    except pyautogui.ImageNotFoundException:
        print("Error: 'joinn.png' image not found.")

def loginToZoom():
    """Login to Zoom by finding the Login button, clicking it, and typing in the username
    and password fields."""
    pass

def signUpForZoom():
    """Navigate to the Sign Up page of Zoom by positioning the cursor over the
    'Sign up' button on the homepage and pressing enter."""
    pass

if __name__ == "__main__":
    main()

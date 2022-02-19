# Zoom_Automation_in_Python
This python script will automatically enter your zoom meetings and send a message of your choice in the chat.

## Setup instructions

**Requirements:** python-3.8 or higher.

* Clone the GitHub repo
```
git clone https://github.com/RonelShorPacker/Zoom_Automation_in_Python.git
```

* cd into the directory
* Install required libraries(if one of them doesn't have an updated version in your os, change the version to the last updated one).
```
pip3 install -r requirements.txt
```
* In configs.yaml, update work_dir and the operating system to your own.

* For every screenshot in the screenshots directory, update it with your own screenshots with pyautogui library with this script(you will have to open a zoom by youself and screenshot each stage):
```
import pyautogui
import time

time.sleep(5)
img = pyautogui.screenshot(f'{path_to_screenshots_dir}/{file_name}.png')
```

* If you are in ubuntu I recommend gthumb, which can be installed in the terminal as so:
```
sudo apt install gthumb
```

* If you are in windows, I recommend using Photos.
* Update the timings.csv with the time of the meeting, meeting url and the message you want to send(optional), for example:
```
timings, meeting_url, message
18/02; 12:00, {meeting_url}, Hello World
```

* run main.py, if your on linux, you can run it in the backround with the following command in the terminal(I will add for window users in the future):
```
cd {path_to_project}
chmod +x main.py
nohup {path_to_project}/main.py > output.log &
```
If you want to kill the script, you can find the proccess ID and kill it with these commands in the terminal:
```
ps ax | grep main.py
kill PID
```

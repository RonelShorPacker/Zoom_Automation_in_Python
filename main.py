import pyautogui
import time
import pandas as pd
from datetime import datetime
import webbrowser
import requests
import hydra
import os
import win32api

def zoom(cfg, meeting_url: str, msg: str=None, leave_after_amount_of_time: bool = True):
    """
    :param cfg: Configs file
    :param meeting_url: Zoom meeting url
    :param msg: The message you want to send in chat
    :return: boolean value if the whole process was a success than 1, otherwise False
    """
    # checking internet connection
    try:
        request = requests.get("https://www.google.com/", timeout=1)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Bad internet connection")
        return 0

    # opening zoom meeting via url
    if cfg.operating_system.os == 'linux' and cfg.operating_system.os_type == 'ubuntu':
        webbrowser.open_new(meeting_url)
    elif cfg.operating_system.os == 'windows':
        webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s &').open(meeting_url)
    else:
        print("This script may not work in your operating system")
        return 0

    time.sleep(cfg.time_breaks.time1)

    if cfg.operating_system.os_type == 'ubuntu':
        # Sometimes in ubuntu it doesn't always open the browser on screen
        open_firefox_btn = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/open_firefox_btn.png', confidence=0.8)
        if open_firefox_btn:
            pyautogui.moveTo(open_firefox_btn)
            pyautogui.click()

    time.sleep(cfg.time_breaks.time2)
    # opening link
    try:
        open_link_btn = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/open_link_btn.png', confidence=0.8)
        assert open_link_btn
        pyautogui.moveTo(open_link_btn)
        pyautogui.click()
    except:
        print("Couldn't find open link button, will take screenshot for future development")
        img_bug = pyautogui.screenshot(f'{cfg.directories.bugs_dir}/open_link_bug.png')
        return 0

    time.sleep(cfg.time_breaks.time3)
    
    # joining meeting with camera off
    try:
        join_without_video_btn = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/join_without_video_btn.png', confidence=0.8)
        assert join_without_video_btn
        pyautogui.moveTo(join_without_video_btn)
        pyautogui.click()
    except:
        print("Couldn't find join without video button button, will take screenshot for future development")
        img_bug = pyautogui.screenshot(f'{cfg.directories.bugs_dir}/join_without_video_bug.png')
        return 0

    time.sleep(cfg.time_breaks.time4)
    
    # waiting for host to authorize entrance
    start_waiting = time.time()
    while True:
        green_check_meeting_btn = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/green_check_btn.png', confidence=0.8)
        if not green_check_meeting_btn:
            if time.time() - start_waiting > cfg.params.patience:
                print("Bug or host didn't authorize entrance before maximum patience, will take screenshot for future development")
                img_bug = pyautogui.screenshot(f'{cfg.directories.bugs_dir}/waiting_bug.png')
                return 0
            continue
        else:
            break

    time.sleep(cfg.time_breaks.time5)

    # sometimes the zoom doesn't open on full screen, so we need to move the mouse so it will be in the zoom
    pyautogui.moveTo(green_check_meeting_btn.x + cfg.params.number_pixels_x_from_green_check, green_check_meeting_btn.y + cfg.params.number_pixels_y_from_green_check)

    time.sleep(cfg.time_breaks.time6)

    # opening chat
    num_tries = 0
    while True:
        try:
            pyautogui.rightClick()
            time.sleep(0.1)
            chat_after_right_click_btn = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/chat_after_right_click.png', confidence=0.8)
            assert chat_after_right_click_btn
            pyautogui.moveTo(chat_after_right_click_btn)
            pyautogui.click()
            break
        except:
            print("Couldn't find chat, will do screenshot for future development")
            img_bug = pyautogui.screenshot(f'{cfg.directories.bugs_dir}/chat_after_right_click_bug.png')
            num_tries += 1
            if num_tries >= cfg.params.num_tries_right_click:
                print("Failed to find chat")
                return 0

    time.sleep(cfg.time_breaks.time7)

    # writing text, tries few attempts because of relatively low chance of finding chat
    num_tries = 0
    while True:
        try:
            type_message_here = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/type_message_here.png', confidence=0.5)
            assert type_message_here
            pyautogui.moveTo(type_message_here)
            pyautogui.click()
            pyautogui.write(msg,  interval=cfg.params.secs_between_keys)
            time.sleep(0.4)
            pyautogui.press('enter')
            break
        except:
            print("Couldn't find type message, will do screenshot for future development")
            img_bug = pyautogui.screenshot(f'{cfg.directories.bugs_dir}/green_check_btn_bug.png')
            num_tries += 1
            if num_tries >= cfg.params.num_tries_type_message:
                print("Failed to write message")
                return 0

    # TODO: How do I know if it is a short meeting or a long meeting? For know, default time is an hour
    start = time.time()
    if leave_after_amount_of_time:
        time.sleep(cfg.time_breaks.time_meeting)
    else:
        # Normally, in formal meetings there is someone that writes Thank you at the end of the meeting, so we wait until
        # that happens and then we leave
        while True:
            thank_you_txt = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/thank_you_txt.png',
                                                           confidence=0.75)
            if thank_you_txt:
                break
            if time.time() - start >= 4800:
                break

    # Leaving meeting
    if cfg.operating_system.os == 'windows':
        os.system("taskkill /f /im  Zoom.exe")
    elif cfg.operating_system.os == 'linux':
        num_tries = 0
        while True:
                try:
                    x_btn = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/x_btn.png')
                    assert x_btn
                    pyautogui.moveTo(x_btn)
                    pyautogui.click()
                    break
                except:
                    print("Couldn't find x button, will do screenshot for future development")
                    img_bug = pyautogui.screenshot(f'{cfg.directories.bugs_dir}/x_btn_bug.png')
                    num_tries += 1
                    if num_tries >= cfg.params.num_tries_x_btn:
                        print("Failed to find x button")
                        return 0

        try:
            leave_btn = pyautogui.locateCenterOnScreen(f'{cfg.directories.screenshots_dir}/leave_btn.png', confidence=0.8)
            assert leave_btn
            pyautogui.moveTo(leave_btn)
            pyautogui.click()
        except:
            print("Couldn't find leave button, will do screenshot for future development")
            img_bug = pyautogui.screenshot(f'{cfg.directories.bugs_dir}/leave_btn_bug.png')
            return 0
    
    return 1


@hydra.main(config_path="./", config_name="configs.yaml")
def main(cfg):
    df = pd.read_csv(f'{cfg.meetings.meeting_file}')

    while True:
        now = datetime.now().strftime("%d.%m; %H:%M")
        if now in str(df['timings']):
            print("There is a meeting scheduled now")
            row = df.loc[df['timings'] == now]
            m_url = str(row.iloc[0, 1])
            m_message = str(row.iloc[0, 2])
            success = zoom(cfg, m_url, m_message, False)
            if success:
                print('Success')
            else:
                print("Failed")
            time.sleep(60)
                
                
if __name__ == "__main__":
    main()



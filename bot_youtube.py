from selenium_utils import *

# Global variable to store the YouTube browser instance
youtube_driver = None

def open_youtube():
    global youtube_driver

    if youtube_driver is None:
        speak("Abriendo YouTube...")
        # Create the YouTube browser instance only if it doesn't exist
        youtube_driver = uc.Chrome()
    else:
        speak("Reutilizando YouTube...")

    # Flag variable
    error_occurred = False

    # Open youtube, ask search query and target search element
    try:
        youtube_driver.get("https://www.youtube.com")
        speak("Qué video deseas ver?")
        video_query = listen_without_name_call()

        bring_window_to_front(youtube_driver)

        search_box = WebDriverWait(youtube_driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )
        search_box.clear()
        search_box.send_keys(video_query.replace("youtube", "").strip())
        search_box.send_keys(Keys.ENTER)
    except:
        speak("No pude acceder a Youtube")
        error_occurred = True

    # Select proper video based on the title of the link
    if not error_occurred:
        try:
            first_video = WebDriverWait(youtube_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//a[@id='video-title' and contains(@title, '{video_query}')]"))
            )
            first_video.click()
        except:
            speak("No encontré el video")
            error_occurred = True

    # Check if video autoplays
    if not error_occurred:
        try:
            WebDriverWait(youtube_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "playing-mode"))
            )
        except:
            speak("No pude reproducir el video")
            error_occurred = True

    #Check if there are any ads active
    if not error_occurred:
        try:
            btnAdPreview = WebDriverWait(youtube_driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "video-ads"))
            )
            if btnAdPreview:
                btnAdSkip = WebDriverWait(youtube_driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ytp-skip-ad-button"))
                )
                btnAdSkip.click()
                print("Ad skipped.")
        except:
            print("No ad to skip.")

        # Minimize the YouTube window
        #youtube_driver.set_window_position(-10000, 0)
        # Restore focus to the command window
        #restore_cmd_window()

        print("YouTube está reproduciendo el video.")
        
def cleanup_for_youtube_driver():
    global youtube_driver
    if youtube_driver:
        youtube_driver.quit()
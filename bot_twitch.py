from selenium_utils import *

# Global variable to store the Twitch browser instance
twitch_driver = None

def open_twitch():
    global twitch_driver

    if twitch_driver is None:
        speak("Abriendo Twitch...")
        # Create the Twitch browser instance only if it doesn't exist
        twitch_driver = uc.Chrome()
        twitch_driver.get("https://www.twitch.tv")
    else:
        speak("Reutilizando la ventana de Twitch...")
        twitch_driver.get("https://www.twitch.tv")

    speak("Qué canal deseas ver?")
    channel_query = listen_without_name_call()

    bring_window_to_front(twitch_driver)

    error_occurred = False

    try:
        # Search for a channel
        search_box = WebDriverWait(twitch_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ScInputBase-sc-vu7u7d-0"))
        )
        search_box.clear()
        search_box.send_keys(channel_query)
        search_box.send_keys(Keys.ENTER)
    except:
        speak("No pude acceder a Twitch")
        error_occurred = True

    if not error_occurred:
        try:
            # Wait for the search results to load and click on the first channel
            first_channel = WebDriverWait(twitch_driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, channel_query))
            )
            first_channel.click()
        except:
            speak("No encontré el canal")
            error_occurred = True

    if not error_occurred:
        try:
            # Wait for the stream to start playing
            WebDriverWait(twitch_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//video[@autoplay]"))
            )
        except Exception as e:
            speak("El canal no está disponible")
            error_occurred = True

        # Minimize the Twitch window
        # twitch_driver.set_window_position(-10000, 0)
        # Restore focus to the command window
        # restore_cmd_window()

        print("Twitch está reproduciendo el canal.")

def cleanup_for_twitch_driver():
    global twitch_driver
    if twitch_driver:
        twitch_driver.quit()
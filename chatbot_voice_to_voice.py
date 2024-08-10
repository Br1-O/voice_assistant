from selenium_utils import *
from bot_youtube import *
from bot_twitch import *

# Load the environment variables from the .env file
load_dotenv()

# Get the variables from the environment
url = os.getenv("URL")
answer_css_selector = os.getenv("ANSWER_CSS_SELECTOR")
data_attribute = os.getenv("DATA_ATTRIBUTE")
value_of_description_in_attribute = os.getenv("VALUE_OF_DESCRIPTION_IN_ATTRIBUTE")
chatDriver = None

def main():

    prompt = ""

    speak("¡Hola! ¿En qué puedo ayudarte?")

    while prompt != "salir":

        print(
            """  
            ╔══════════════════════════════════════════════╗
            ║    Ingresa el prompt que deseas ejecutar:    ║
            ╚══════════════════════════════════════════════╝
            """
        )

        prompt = listen()

        if prompt != "salir":

            if "youtube" in prompt.lower():
                open_youtube()
            elif "twitch" in prompt.lower():
                open_twitch()
            elif "cerrar" in prompt.lower():
                speak("¿Qué deseas cerrar?")
                closingOption = listen_without_name_call()

                if "youtube" in closingOption.lower():
                    try:
                        cleanup_for_youtube_driver()
                    except:
                        speak("No pude cerrar youtube")
                elif "twitch" in closingOption.lower():
                    try:
                        cleanup_for_twitch_driver()
                    except:
                        speak("No pude cerrar Twitch")
                elif "todos" in closingOption.lower():
                    try:
                        cleanup_for_youtube_driver()
                        cleanup_for_twitch_driver()
                    except:
                        speak("No pude cerrar todos")
            else:
                #Chatbot AI option
                global chatDriver

                if chatDriver is None:
                    # Configure the Chrome options
                    options = uc.ChromeOptions()
                    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    options.add_argument("--start-maximized")
                    # Initialize the undetected Chrome driver
                    chatDriver = uc.Chrome(options=options)
                    # Open the page
                    chatDriver.get(url)
                
                human_delay()

                # Minimize the browser window by moving it off-screen
                chatDriver.set_window_position(-10000, 0)  # Move the window far off-screen

                restore_cmd_window()

                # Scroll to ensure the input element is visible
                chatDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                human_delay()
                
                # Move mouse to the input field before interacting
                input_element = WebDriverWait(chatDriver, 15).until(
                    EC.presence_of_element_located((By.ID, "prompt-textarea"))
                )
                
                human_delay()

                input_element.clear()
                
                # Simulate human-like delays before starting to type
                human_delay()
                
                # Type each character with a random delay
                for c in prompt:
                    input_element.send_keys(c)
                    human_delay(0.05, 0.08)
                
                # Press Enter with a slight delay
                human_delay(0.05, 0.08)
                input_element.send_keys(Keys.ENTER)

                # Ensure the browser window is brought to the front and maximized
                bring_window_to_front(chatDriver)
                
                # Wait for and retrieve the response element
                WebDriverWait(chatDriver, 15).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, answer_css_selector))
                )
                
                # Get the full text of the last odd div
                complete_answer = get_full_text_of_last_div(chatDriver, answer_css_selector, data_attribute, value_of_description_in_attribute)
                
                print(
                    """  
                    ╔══════════════════╗
                    ║    Respuesta:    ║
                    ╚══════════════════╝
                    """
                )

                print(complete_answer + "\n")

                # Make the bot speak out loud the whole answer
                speak(complete_answer)
        else:

            speak("Nos vemos")

            atexit.register(cleanup_for_youtube_driver)
            atexit.register(cleanup_for_twitch_driver)

            # Exit the loop and quit the driver
            chatDriver.quit()

if __name__ == "__main__":
    main()
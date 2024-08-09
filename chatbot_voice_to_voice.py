from selenium_utils import *

# Load the environment variables from the .env file
load_dotenv()

# Get the variables from the environment
url = os.getenv("URL")
answer_css_selector = os.getenv("ANSWER_CSS_SELECTOR")
data_attribute = os.getenv("DATA_ATTRIBUTE")
value_of_description_in_attribute = os.getenv("VALUE_OF_DESCRIPTION_IN_ATTRIBUTE")


def main():

    # Configure the Chrome options
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    
    # Initialize the undetected Chrome driver
    driver = uc.Chrome(options=options)

    human_delay()

    # Open the page
    driver.get(url)
    
    human_delay()

    prompt = ""

    while prompt != "salir":
    
        # Minimize the browser window by moving it off-screen
        driver.set_window_position(-10000, 0)  # Move the window far off-screen

        restore_cmd_window()

        print(
            """  
            ╔══════════════════════════════════════════════╗
            ║    Ingresa el prompt que deseas ejecutar:    ║
            ╚══════════════════════════════════════════════╝
            """
        )
        prompt = listen()

        if prompt != "salir":
            
            # Scroll to ensure the input element is visible
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            human_delay()
            
            # Move mouse to the input field before interacting
            input_element = WebDriverWait(driver, 15).until(
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
            bring_window_to_front(driver)
            
            # Wait for and retrieve the response element
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, answer_css_selector))
            )
            
            # Get the full text of the last odd div
            complete_answer = get_full_text_of_last_div(driver, answer_css_selector, data_attribute, value_of_description_in_attribute)
            
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
            # Exit the loop and quit the driver
            driver.quit()

if __name__ == "__main__":
    main()
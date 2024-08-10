#selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

#chrome driver for stealth
import undetected_chromedriver as uc

#for os and general functionality
import time
import random
import os
from dotenv import load_dotenv
import platform
import subprocess
import ctypes
import atexit

# for speech recognition
import pyttsx3
import speech_recognition as sr

#for mouse movement
import pyautogui


def create_webdriver(service_path):
    service = Service(executable_path=service_path)
    driver = webdriver.Chrome(service=service)
    return driver

def bring_window_to_front(driver):
    # Maximize the window
    driver.maximize_window()
                
    # Bring the browser window to the front to ensure it refreshes correctly
    driver.switch_to.window(driver.current_window_handle)

    # Attempt to bring the window to the front using JavaScript
    driver.execute_script("window.focus();")

    # Platform-specific focus adjustment
    if platform.system() == "Windows":
        # On Windows, you might need to use additional libraries to force focus
        # This is a workaround and might require pywin32 or similar libraries
        import win32gui
        import win32con
        hwnd = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    elif platform.system() == "Darwin":
        # On macOS, there’s no direct equivalent, so we rely on maximizing
        pass
    elif platform.system() == "Linux":
        # On Linux, we rely on maximizing and focusing
        pass

# Function to focus cmd window
def restore_cmd_window():
    # Minimize the CMD window
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)  # SW_MINIMIZE

    # Wait for a moment before restoring
    time.sleep(0.25)

    # Restore the CMD window
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 9)  # SW_RESTORE


# Function to simulate human-like delay
def human_delay(min_time=0.1, max_time=0.25):
    time.sleep(random.uniform(min_time, max_time))

def click_element_when_clickable(driver, by, value, doXTimes=1, callback = None, max_retries=5, timeout=10):
    for attempt in range(max_retries):
        try:
            for _ in range(doXTimes):
                # Wait for the element to be clickable
                element = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
                element.click()

                callback()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    return False


# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognition
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    text = ""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Escuchando...")

        while text == "":
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Set a timeout for listening
                generalSpeak = recognizer.recognize_google(audio, language='es-ES')
                
                if "viernes" in generalSpeak.lower():  # Case-insensitive check
                    speak("Te escucho")
                    print("Esperando comando...")

                    while text == "":
                        try:
                            # Listen for the actual command
                            command_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                            text = recognizer.recognize_google(command_audio, language='es-ES')
                            speak("Entendido.")
                            print(f"Usuario dijo: {text}")
                        except sr.WaitTimeoutError:
                            print("Tiempo de espera agotado, no se detectó audio.")
                        except sr.UnknownValueError:
                            print("No se entendió el audio.")
                        except sr.RequestError as e:
                            print(f"Error en la solicitud: {e}")
                else:
                    print(f"General speech detected: {generalSpeak}")
            except sr.WaitTimeoutError:
                print("Tiempo de espera agotado, no se detectó audio.")
            except sr.UnknownValueError:
                print("No se entendió el audio.")
            except sr.RequestError as e:
                print(f"Error en la solicitud: {e}")
    return text

        
# Selector of last div for
def get_full_text_of_last_div(driver, css_selector, data_attribute, value_of_description_in_attribute):
    try:
        while True:
            # Find all div elements that match the CSS selector
            all_divs = driver.find_elements(By.CSS_SELECTOR, css_selector)
            
            # Filter odd divs based on the data-testid attribute
            odd_divs = [div for div in all_divs if int(div.get_attribute(data_attribute).replace(value_of_description_in_attribute, "")) % 2 != 0]
            
            if odd_divs:
                # Get the last odd div
                last_odd_div = odd_divs[-1]
                
                # Get the initial text
                initial_text = last_odd_div.text
                
                # Wait for the text to update
                while True:
                    time.sleep(2)  # Wait before checking again
                    
                    # Recheck the text
                    all_divs = driver.find_elements(By.CSS_SELECTOR, css_selector)
                    odd_divs = [div for div in all_divs if int(div.get_attribute(data_attribute).replace(value_of_description_in_attribute, "")) % 2 != 0]
                    
                    if odd_divs:
                        last_odd_div = odd_divs[-1]
                        current_text = last_odd_div.text
                        
                        if current_text != initial_text:
                            initial_text = current_text
                        else:
                            break  # Exit if no new content is detected
                    else:
                        break  # Exit if no more odd divs are found
                return initial_text
            else:
                full_text = "No se encontraron elementos con el selector dado."
                return full_text
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def listen_without_name_call():
    text = ""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Escuchando...")
        while text == "":
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Set a timeout for listening                
                text = recognizer.recognize_google(audio, language='es-ES')
            except sr.WaitTimeoutError:
                print("Tiempo de espera agotado, no se detectó audio.")
            except sr.UnknownValueError:
                print("No se entendió el audio.")
            except sr.RequestError as e:
                print(f"Error en la solicitud: {e}")
    speak("Entendido.")
    print(f"Usuario dijo: {text}")
    return text
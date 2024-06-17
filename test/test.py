import unittest
import threading
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app import app

class TestMusicPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Chrome WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Start the Flask app in a separate thread
        cls.app_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': True, 'use_reloader': False})
        cls.app_thread.start()

        # Give the server a second to ensure it starts
        WebDriverWait(cls.driver, 10).until(lambda driver: driver.get("http://localhost:5000"))

    @classmethod
    def tearDownClass(cls):
        # Close the browser window
        cls.driver.quit()
        # Terminate the Flask app thread
        cls.app_thread.join()

    def test_index(self):
        self.driver.get("http://localhost:5000")

        try:
            # Check if the page contains the music files
            self.assertTrue(WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//audio"))))

        except S3Error as exc:
            print("Error occurred.", exc)
            self.fail("S3Error occurred")

    def test_next_previous_song(self):
        self.driver.get("http://localhost:5000")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='nextSong()']"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='nextSong()']"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='previousSong()']"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='previousSong()']"))
        ).click()

    def test_play_pause(self):
        self.driver.get("http://localhost:5000")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='togglePlayPause()']"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='togglePlayPause()']"))
        ).click()

if __name__ == '__main__':
    unittest.main()

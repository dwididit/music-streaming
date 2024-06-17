import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os

from app import app

class TestMusicPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask app in a separate thread
        cls.server = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5002})
        cls.server.setDaemon(True)
        cls.server.start()

        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")

        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        cls.driver.get("http://localhost:5002")
        cls.driver.implicitly_wait(10)

    def test_play_song(self):
        self.driver.find_element(By.XPATH, "//button[@onclick=\"playAudio(this.parentElement.getAttribute('data-url'), this.parentElement)\"]").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@onclick=\"playAudio(this.parentElement.getAttribute('data-url'), this.parentElement)\"]")))

    def test_play_pause(self):
        self.driver.find_element(By.XPATH, "//button[@onclick='togglePlayPause()']").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@onclick='togglePlayPause()']")))

    def test_next_previous_song(self):
        self.driver.find_element(By.XPATH, "//button[@onclick='nextSong()']").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@onclick='nextSong()']")))
        self.driver.find_element(By.XPATH, "//button[@onclick='previousSong()']").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@onclick='previousSong()']")))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()

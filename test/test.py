import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app import app
import threading

class TestMusicPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5002, 'debug': True})
        cls.server.start()
        cls.chrome_options = Options()
        cls.chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        cls.chrome_options.add_argument("--headless")  # Run without a GUI
        cls.chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    def setUp(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.driver.get("http://localhost:5000")
        self.driver.implicitly_wait(30)

    def test_play_song(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick=\"playAudio(this.parentElement.getAttribute('data-url'), this.parentElement)\"]"))
        ).click()

    def test_play_pause(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='togglePlayPause()']"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@onclick='togglePlayPause()']"))
        ).click()

    def test_next_previous_song(self):
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

    def tearDown(self):
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask server
        terminate_server = threading.Thread(target=app.shutdown)
        terminate_server.start()
        terminate_server.join()

if __name__ == '__main__':
    unittest.main()

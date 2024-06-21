import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestMusicPlayer(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--headless")  # Run without a GUI
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("http://localhost:5000")
        self.wait = WebDriverWait(self.driver, 30)  # Explicit wait

    def test_play_song(self):
        play_button = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                  "//button[@onclick=\"playAudio(this.parentElement.getAttribute('data-url'), this.parentElement)\"]")))
        play_button.click()

    def test_play_pause(self):
        play_pause_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@onclick='togglePlayPause()']")))
        play_pause_button.click()
        self.driver.implicitly_wait(5)
        play_pause_button.click()

    def test_next_previous_song(self):
        next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick='nextSong()']")))
        next_button.click()
        self.driver.implicitly_wait(5)
        next_button.click()
        previous_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@onclick='previousSong()']")))
        previous_button.click()
        self.driver.implicitly_wait(5)
        previous_button.click()

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()

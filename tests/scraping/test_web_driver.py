import unittest
from catswalk.scraping.webdriver import CWWebDriver
import time

class TestCatsWebDriver(unittest.TestCase):
    binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    executable_path = "/Users/rv/ws/tools/chromedriver"
    proxy = None
    headless = True
    
    def test_simple_get(self):
        """[python -m unittest tests.scraping.test_web_driver.TestCatsWebDriver.test_simple_get]
        """
        """
        request = CWWebDriver(binary_location=self.binary_location, executable_path=self.executable_path)
        html = request.move(url="https://yahoo.co.jp")
        time.sleep(10)
        request.close()
        """
        
        with CWWebDriver(binary_location=self.binary_location, executable_path=self.executable_path) as request:
            responseHtml = request.move(url="https://yahoo.co.jp")
            print(responseHtml)
            print("end")
            time.sleep(10)
        

    def test_print_screen(self):
        """[python -m unittest tests.scraping.test_web_driver.TestCatsWebDriver.test_print_screen]
        """
        request = CWWebDriver(binary_location=self.binary_location, executable_path=self.executable_path)
        request.move(url="https://yahoo.co.jp")
        request.print_fullscreen("/tmp", "test_print_screen")
        time.sleep(10)
        request.close()

if __name__ == "__main__":
    unittest.main()
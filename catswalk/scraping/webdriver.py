import logging
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from catswalk.scraping.request import CWRequest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from catswalk.scraping.types.type_response import ResponseHtml 
from catswalk.scraping.types.type_webdriver import EXECUTION_ENV, DEVICE, DEVICE_MODE
from selenium.webdriver.common.action_chains import ActionChains

class CWWebDriver:
    def __init__(self, binary_location: str = None, executable_path: str = None, execution_env: EXECUTION_ENV = EXECUTION_ENV.LOCAL, device = DEVICE.DESKTOP_GENERAL, proxy: str = None, implicitly_wait = 5.0):
        """[summary]

        Args:
            binary_location (str): [description]
            executable_path (str): [description]
            execution_env (str, optional): [local, local_headless, aws]. Defaults to "local".
            proxy (str, optional): [description]. Defaults to None.
        """
        self.binary_location = binary_location
        self.executable_path = executable_path
        self.execution_env = execution_env
        self.proxy = proxy

        options = Options()
        if self.execution_env == EXECUTION_ENV.LOCAL_HEADLESS:
            options.binary_location = self.binary_location
            options.add_argument('--headless') # https://www.ytyng.com/blog/ubuntu-chromedriver/
            options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
            options.add_argument("start-maximized")  # open Browser in maximized mode
            options.add_argument("disable-infobars")  # disabling infobars
            options.add_argument("--disable-extensions")  # disabling extensions
            options.add_argument("--disable-gpu")  # applicable to windows os only
            options.add_argument("--no-sandbox")  # Bypass OS security model
        elif self.execution_env == EXECUTION_ENV.AWS_LAMBDA:
            os.environ['HOME'] = '/opt/browser/'
            self.executable_path = "/opt/browser/chromedriver"
            options.binary_location = "/opt/browser/headless-chromium"
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--single-process")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280x1696")
            options.add_argument("--disable-application-cache")
            options.add_argument("--disable-infobars")
            options.add_argument("--hide-scrollbars")
            options.add_argument("--enable-logging")
            options.add_argument("--log-level=0")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--homedir=/tmp")
            options.add_argument('--disable-dev-shm-usage')
        else:
            options.binary_location = self.binary_location
        if self.proxy:
            logging.info("WebDriverSession proxy on")
            options.add_argument(f"proxy-server={self.proxy}")

        if device.value.mode == DEVICE_MODE.MOBILE:
            mobile_emulation = { "deviceName": "Galaxy S5" }
            options.add_experimental_option("mobileEmulation", mobile_emulation)

        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'INFO'}
        #logging.info(f"WebDriverSession.__init__ : {binary_location}, {executable_path}, {proxy}, {execution_env}")
        self.driver = webdriver.Chrome(options=options, executable_path=self.executable_path, desired_capabilities=caps)
        self.driver.implicitly_wait(implicitly_wait)



    def __enter__(self):
        """

        :return:
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.close()

    def close(self):
        """[Close WebDriverSession, if chromewebdriver dosen't kill, plsease execute "killall chromedriver"]
        
        """
        self.driver.quit()

    def reload(self):
        self.driver.refresh()

    @property
    def cookies(self):
        """[Get cookie info]

        Returns:
            [type]: [description]
        """
        return self.driver.get_cookies()

    def to_request_session(self) -> CWRequest:
        """[summary]
        
        Returns:
            Request -- [description]
        """
        session = CWRequest()
        for cookie in self.driver.get_cookies():
            self.session.cookies.set(cookie["name"], cookie["value"])
        return session

    def wait_rendering_by_id(self, id, timeout=20):
        """[summary]
        
        Arguments:
            id {[type]} -- [description]
        
        Keyword Arguments:
            timeout {int} -- [description] (default: {20})
        """
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.ID, id)))

    def wait_rendering_by_class(self, _class, timeout=20):
        """[summary]
        
        Arguments:
            _class {[type]} -- [description]
        
        Keyword Arguments:
            timeout {int} -- [description] (default: {20})
        """
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, _class)))

    def transition(self, url: str):
        """[summary]

        Args:
            url (str): [description]
        """
        self.driver.get(url)

    def get(self, url: str):
        self.transition(url=url)
        #WebDriverWait(self.driver, 10).until(EC.url_changes(url))
        soup = self.html
        return soup

    def print_screen_by_position(self, w, h, output_path: str, filename:str):
        """[summary]

        Args:
            w ([type]): [description]
            h ([type]): [description]
            output_path (str): [description]
            filename (str): [description]
        """
        # set window size
        self.driver.set_window_size(w, h)

        # Get Screen Shot
        fullpath = f"{output_path}/{filename}.png"
        self.driver.save_screenshot(fullpath)

    def print_screen_by_xpath(self, xpath:str, output_path: str, filename:str) -> str:
        """[summary]

        Args:
            xpath (str): [description]
            output_path (str): [description]
            filename (str): [description]
        """
        # Get Screen Shot
        fullpath = f"{output_path}/{filename}.png"
        # 範囲を指定してスクリーンショットを撮る
        png = self.driver.find_element_by_xpath(xpath).screenshot_as_png
        # ファイルに保存
        with open(fullpath, 'wb') as f:
            f.write(png)
        return fullpath

    def print_screen_by_class_name(self, class_name:str, output_path: str, filename:str) -> str:
        """[summary]

        Args:
            class_name (str): [description]
            output_path (str): [description]
            filename (str): [description]
        """
        # Get Screen Shot
        fullpath = f"{output_path}/{filename}.png"
        # 範囲を指定してスクリーンショットを撮る
        png = self.driver.find_element_by_class_name(class_name).screenshot_as_png
        # ファイルに保存
        with open(fullpath, 'wb') as f:
            f.write(png)
        return fullpath
    
    def print_fullscreen(self, path, filename):
        # get width and height of the page
        w = self.driver.execute_script("return document.body.scrollWidth;")
        h = self.driver.execute_script("return document.body.scrollHeight;")
        self.print_screen_by_position(w, h, path, filename)


    def click_by_class_name(self, class_name:str) -> str:
        """[summary]

        Args:
            class_name (str): [description]

        Returns:
            str: [description]
        """
        # Get Screen Shot
        elem = self.driver.find_element_by_class_name(class_name)
        elem.click()


    def move_to_element_by_class_name(self, class_name:str) -> str:
        """[summary]

        Args:
            class_name (str): [description]

        Returns:
            str: [description]
        """
        # Get Screen Shot
        elem = self.driver.find_element_by_class_name(class_name)
        elem.location_once_scrolled_into_view


    @property
    def html(self):
        html = self.driver.page_source.encode('utf-8')
        return BeautifulSoup(html, "lxml")

    @property
    def log(self):
        result = []
        for entry in self.driver.get_log('performance'):
            result.append(entry['message'])
        return result

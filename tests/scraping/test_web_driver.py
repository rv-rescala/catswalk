from catswalk.scraping.webdriver import CWWebDriver
import time
from catswalk.scraping.types.type_webdriver import *


binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
executable_path = "/Users/rv/ws/tools/chromedriver"
proxy = None
headless = True

request = CWWebDriver(binary_location=binary_location, executable_path=executable_path, execution_env=EXECUTION_ENV.LOCAL, is_secret_mode=True)
url="https://ebookjapan.yahoo.co.jp/books/626711/"
#res = request.get(url=url, remove_class="scapa-overlay-default")
res = request.get(url=url)
print(res)
#request.print_screen_by_size(100, 1000, "/tmp", "size")
time.sleep(1000)
request.close()
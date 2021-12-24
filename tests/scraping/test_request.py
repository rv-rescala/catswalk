import unittest
from catswalk.scraping.request import CWRequest


class TestCWRequest(unittest.TestCase):
    def test_get(self):
        request = CWRequest()
        responseHtml = request.get(url="https://yahoo.co.jp", response_content_type="html")
        print(responseHtml)
        request.close()


if __name__ == "__main__":
    unittest.main()
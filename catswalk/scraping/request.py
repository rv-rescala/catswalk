import requests
from requests import Session
import json
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from abc import ABCMeta, abstractmethod
from catsrequests.error import CatsRequestSessionError
from catsrequests.response import Response, ResponseHtml, ResponseJson
import time
import sys
import email.utils as eut
from datetime import datetime, timezone
import email.utils as eut
import logging

logger = logging.getLogger()

class Request:
    DEFAULT_TOR_PROXY = {'http':'socks5://127.0.0.1:9050','https':'socks5://127.0.0.1:9050'}
    DEFAULT_TIMEOUT = (10.0, 20.0)
    
    def __init__(self, proxy=None, verify=True, timeout=None):
        """[summary]
        """
        if timeout:
            self.timeout = timeout
        else:
            self.timeout = self.DEFAULT_TIMEOUT
        self.session = requests.Session()
        if proxy:
            self.session.proxies.update(proxy)
        self.session.verify=verify
        self.print_global_info()
        
    @classmethod
    def parse_http_date(s):
        return datetime(*eut.parsedate(s)[:6], tzinfo=timezone.utc)
        
    
    def __enter__(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """
        return self

    def __exit__(self, ex_type, ex_value, trace):
        """[summary]
        
        Arguments:
            ex_type {[type]} -- [description]
            ex_value {[type]} -- [description]
            trace {[type]} -- [description]
        """
        self.close()
        
    def close(self):
        """[summary]
        """
        self.session.close()

    def get_cookie(self, key):
        return self.session.cookies.get(key)

    def get_cookies(self):
        return self.session.cookies.get_dict()

    def _mk_result(self, ret, response_content_type: str):
        if response_content_type == "html":
            soup = BeautifulSoup(ret.content, features="html.parser")
            return ResponseHtml(ret.headers, soup, ret)
        elif response_content_type == "json":
            soup = BeautifulSoup(ret.content, features="html.parser")
            return ResponseJson(ret.headers, json.loads(str(soup)), ret)
        else:
            return Response(ret.headers, ret.content, ret)

    def _check_status_code(self, url, status_code):
        if status_code != 200:
            raise CatsRequestSessionError(f"{url} response code is {status_code}")
        return True

    def retry_get(self, url, response_content_type=None, retry_num=4, wait=1):
        reponse = None
        for i in range(retry_num):
            try:
                reponse = self.get(url, response_content_type)
                return reponse
            except Exception:
                print(f"retry_get: {url} retry {i}")
                time.sleep(wait)
        raise CatsRequestSessionError(f"{url} retry count is {retry_num}")

    def get(self, url, response_content_type=None):
        """[summary]
        
        Arguments:
            url {[type]} -- [description]
        
        Keyword Arguments:
            response_content_type {[type]} -- [html or json] (default: {None})
        
        Raises:
            RuntimeError: [description]
        
        Returns:
            [type] -- [description]
        """
        ret = self.session.get(url, timeout=self.timeout)
        self._check_status_code(url, ret.status_code)
        return self._mk_result(ret, response_content_type)

    def post(self, url, post_data, response_content_type):
        ret = self.session.post(url, post_data, timeout=self.timeout)
        self._check_status_code(url, ret.status_code)
        return self._mk_result(ret, response_content_type)

    def download(self, url:str, fullpath:str, request_type:str = "get", post_data=None):
        if request_type == "post":
            bi = self.post(url=url, post_data=post_data)
        else:
            bi = self.get(url=url).content
        with open(fullpath, "wb") as f:
            f.write(bi)

    def get_global_info(self):
        url = "https://ipinfo.io"
        result = None
        try:
            result = self.get(url=url, response_content_type="json").content
        except Exception:
            logger.warn(f"get_global_info response is null: {sys.exc_info()}")
        return result
    
    def print_global_info(self):
        logger.info(f"global network info is {self.get_global_info()}")
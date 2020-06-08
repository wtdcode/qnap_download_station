from requests import Session
from base64 import b64encode
from random import random
from datetime import datetime
import xml.etree.ElementTree as ET

class QtsException(Exception):
    pass

class LoginFailedException(Exception):
    pass

class Qts:

    def __init__(self, host, port, username, password, protocol="http"):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._protocol = protocol
        self._sid = None
        self._is_login = False
        self._user = Session()
    
    def build_cgi_link(self, cgi):
        return f"{self.baseurl}/cgi-bin/{cgi}"

    def login(self):
        r = self._user.post(self.build_cgi_link("authLogin.cgi"), data={
            "user" : self._username,
            "pwd" : b64encode(self._password.encode("utf-8")),
            "serviceKey" : "1",
            "r" : str(random())
        })
        t = ET.fromstring(r.text)
        authpassed = t.find("authPassed").text
        if '1' in authpassed:
            self._sid = t.find("authSid").text
            self._user.cookies['NAS_PW_STATUS'] = '0'
            self._user.cookies['NAS_USER'] = self._username
            self._user.cookies['NAS_SID'] = self._sid
            self._user.cookies['nas_lang'] = "ENG"
            self._user.cookies['QT'] = str(int(datetime.now().timestamp()*1000))
            self._is_login = True
        else:
            raise LoginFailedException()
    
    @property
    def user(self):
        return self._user
    
    @property
    def baseurl(self):
        return f"{self._protocol}://{self._host}:{self._port}"
    
    @property
    def sid(self):
        return self._sid

    @property
    def is_login(self):
        return self._is_login
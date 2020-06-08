from qnap import Qts, QtsException, LoginFailedException
from json import loads

class AddURLException(QtsException):
    pass

class DownloadStation:

    def __init__(self, qts :Qts):
        self._qts = qts
        self._user = qts.user
        self._sid = None
        self._is_login = False

    def _lazy_login(self):
        if not self._qts.is_login:
            self._qts.login()
        if not self._is_login:
            self.login()

    def build_ds_url(self, catagory, func, version="V4"):
        return f"{self._qts.baseurl}/downloadstation/{version}/{catagory}/{func}"

    def login(self):
        if not self._qts.is_login:
            self._qts.login()
        r  = self._user.post(self.build_ds_url("Misc", "Login"))
        j = loads(r.text)
        if j['error'] == 0:
            self._sid = j['sid']
            self._is_login = True
        else:
            raise LoginFailedException()
    
    def addurls(self, urls, temp, move):
        self._lazy_login()
        data = [
            ("temp", temp),
            ("move", move),
            ("sid", self._sid)
        ] + [("url", u) for u in urls]
        r  = self._user.post(self.build_ds_url("Task", "AddUrl"), data=data)
        j = r.json()
        if j['error'] == 0:
            return
        else:
            raise AddURLException()

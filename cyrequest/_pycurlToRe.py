# -*- encoding: utf-8 -*-
# !/usr/bin/python3

from tkinter import N
import pycurl
import io
from urllib.parse import urlencode
import json as jsOn
from requests.cookies import RequestsCookieJar

class _parseHtml:
    def __init__(self, req, html):
        self.req = req
        self.html = html
        self.encoding = "utf-8"
        self.content = None
        self.headers = None
        self.cookie = RequestsCookieJar()

    def getHeaders(self, encodeing):
        self.encoding = encodeing
        if self.content == None:
            self.gethtml()
        self.headers = {i.split(":")[0]:''.join(i.split(":")[1:]).strip() for i in self.content[:self.req.getinfo(pycurl.HEADER_SIZE)].split('\r\n')[1:]}

    def gethtml(self):
        self.content = self.html.getvalue().decode(self.encoding)

    def gettext(self, encodeing):
        self.encoding = encodeing
        if self.content == None:
            self.gethtml()
        return self.content[self.req.getinfo(pycurl.HEADER_SIZE):]

    def getcontent(self):
        return self.html.getvalue()[self.req.getinfo(pycurl.HEADER_SIZE):]

    def getcookie(self, encodeing):
        self.encoding = encodeing
        if self.content == None:
            self.gethtml()
        for i in self.content[:self.req.getinfo(pycurl.HEADER_SIZE)].split('\r\n')[1:]:
            if i.split(":")[0] == 'Set-Cookie':
                cook = ''.join(i.split(":")[1]).split(';')[0].split('=')
                self.cookie.set(cook[0].strip(), cook[1].strip())
        if "Cookie" in self.req.headers:
            for i in self.req.headers['Cookie'].split(';'):
                cook = i.split('=')
                self.cookie.set(cook[0].strip(), cook[1].strip())
        return self.cookie




class _response:
    def __init__(self, html, req):
        self.req = req
        self.html = _parseHtml(req, html)
        self.encoding = 'utf-8'

    @property
    def status_code(self):
        return self.req.getinfo(pycurl.HTTP_CODE)

    @property
    def text(self):
        return self.html.gettext(self.encoding)
    @property
    def content(self):
        return self.html.getcontent()

    def json(self):
        return jsOn.loads(self.text)
    @property
    def cookies(self):
        return self.html.getcookie(self.encoding)

class _request:
    def __init__(self,_state, req, html):
        self.req = req
        self.req._state = _state
        self.html = html
    @property
    def _state(self):
        return self.req._state
    def result(self):
        return _response(self.html, self.req)

class pycurlToRe:
    def __init__(self, max_workers=None, session=None):
        self.session = session
        self.cont = pycurl.CurlMulti()
        self.cont.handles = []

    def get(self, url=None, headers=None, verify=None, params=None, proxies=None, timeout=None,
                               allow_redirects=None):
        FOLLOWLOCATION = 5
        SSL_VERIFYPEER = 1
        SSL_VERIFYHOST = 1
        TIMEOUT = 15

        html = io.BytesIO()
        c = pycurl.Curl()
        c.setopt(c.HEADER, True)
        if allow_redirects == False:
            FOLLOWLOCATION = 0

        if verify == False:
            SSL_VERIFYPEER = 0
            SSL_VERIFYHOST = 0
        if timeout != None:
            TIMEOUT = timeout

        if headers != None:
            h = []
            for k, v in headers.items():
                h.append(k+": "+str(v))
            c.setopt(pycurl.HTTPHEADER, h)
            c.headers = headers
        else:
            c.headers = {}

        # 设置代理
        if proxies != None:
            name = None
            if 'http' in proxies:
                name = 'http'
            elif 'https' in proxies:
                name = 'https'
            if name != None:
                c.setopt(pycurl.PROXY, proxies[name])

        # 设置参数
        if params != None:
            url += "?"+urlencode(params)
        # 设置html
        c.setopt(pycurl.WRITEFUNCTION, html.write)
        # 设置重定向
        c.setopt(pycurl.FOLLOWLOCATION, FOLLOWLOCATION)
        # 设置忽略证书
        c.setopt(pycurl.SSL_VERIFYPEER, SSL_VERIFYPEER)
        c.setopt(pycurl.SSL_VERIFYHOST, SSL_VERIFYHOST)
        # 设置超时
        c.setopt(pycurl.TIMEOUT, TIMEOUT)
        # 设置url
        c.setopt(pycurl.URL, url)
        req = _request("RUNING", c, html)
        self.cont.add_handle(c)
        self.cont.handles.append(req)
        return req

    def updata(self):
        self.cont.perform()
        u = []
        for index, i in enumerate(self.cont.handles):
            if i.updata(self.cont) == True:
                u.append(index)
        j = 0
        for i in u:
            self.cont.handles.pop(i+j)
            j -= 1


    def post(self, url=None,
    data='',
    json=None

    ,  headers=None, verify=None, params=None, proxies=None, timeout=None,
                               allow_redirects=None):
        FOLLOWLOCATION = 5
        SSL_VERIFYPEER = 1
        SSL_VERIFYHOST = 1
        TIMEOUT = 15

        html = io.BytesIO()
        c = pycurl.Curl()
        c.setopt(c.HEADER, True)
        if allow_redirects == False:
            FOLLOWLOCATION = 0

        if verify == False:
            SSL_VERIFYPEER = 0
            SSL_VERIFYHOST = 0
        if timeout != None:
            TIMEOUT = timeout

        if headers != None:
            h = []
            for k, v in headers.items():
                h.append(k+": "+str(v))
            c.setopt(pycurl.HTTPHEADER, h)
            c.headers = headers
        else:
            c.headers = {}

        # 设置代理
        if proxies != None:
            name = None
            if 'http' in proxies:
                name = 'http'
            elif 'https' in proxies:
                name = 'https'
            if name != None:
                c.setopt(pycurl.PROXY, proxies[name])

        # 设置参数
        if params != None:
            url += "?"+urlencode(params)

        if type(data) == type({}):
            c.setopt(c.POSTFIELDS, urlencode(data))
        elif json == None:
            c.setopt(c.POSTFIELDS, data)
        else:
            c.setopt(c.POSTFIELDS, jsOn.dumps(json))

        # 设置html
        c.setopt(pycurl.WRITEFUNCTION, html.write)
        # 设置重定向
        c.setopt(pycurl.FOLLOWLOCATION, FOLLOWLOCATION)
        # 设置忽略证书
        c.setopt(pycurl.SSL_VERIFYPEER, SSL_VERIFYPEER)
        c.setopt(pycurl.SSL_VERIFYHOST, SSL_VERIFYHOST)
        # 设置超时
        c.setopt(pycurl.TIMEOUT, TIMEOUT)
        # 设置url
        c.setopt(pycurl.URL, url)
        req = _request("RUNING", c, html)
        self.cont.add_handle(c)
        self.cont.handles.append(req)
        return req

    def updata(self):
        self.cont.perform()
        u = []
        num_q, ok_list, err_list = self.cont.info_read()

        for index, i in enumerate(self.cont.handles):
            s = 0
            for i2 in ok_list + err_list:
                if i2 == i.req:
                    i.req._state = 'FINISHED'
                    s = 1
                    break
            if s == 1:
                u.append(index)
        j = 0
        for i in u:
            self.cont.handles.pop(i+j)
            j -= 1

class pycurlToRetb:

    def get(self, url=None, headers=None, verify=None, params=None, proxies=None, timeout=None,
                               allow_redirects=None):
        FOLLOWLOCATION = 5
        SSL_VERIFYPEER = 1
        SSL_VERIFYHOST = 1
        TIMEOUT = 15

        html = io.BytesIO()
        c = pycurl.Curl()
        c.setopt(c.HEADER, True)
        if allow_redirects == False:
            FOLLOWLOCATION = 0

        if verify == False:
            SSL_VERIFYPEER = 0
            SSL_VERIFYHOST = 0
        if timeout != None:
            TIMEOUT = timeout

        if headers != None:
            h = []
            for k, v in headers.items():
                h.append(k+": "+str(v))
            c.setopt(pycurl.HTTPHEADER, h)
            c.headers = headers
        else:
            c.headers = {}

        # 设置代理
        if proxies != None:
            name = None
            if 'http' in proxies:
                name = 'http'
            elif 'https' in proxies:
                name = 'https'
            if name != None:
                c.setopt(pycurl.PROXY, proxies[name])

        # 设置参数
        if params != None:
            url += "?"+urlencode(params)
        # 设置html
        c.setopt(pycurl.WRITEFUNCTION, html.write)
        # 设置重定向
        c.setopt(pycurl.FOLLOWLOCATION, FOLLOWLOCATION)
        # 设置忽略证书
        c.setopt(pycurl.SSL_VERIFYPEER, SSL_VERIFYPEER)
        c.setopt(pycurl.SSL_VERIFYHOST, SSL_VERIFYHOST)
        # 设置超时
        c.setopt(pycurl.TIMEOUT, TIMEOUT)
        # 设置url
        c.setopt(pycurl.URL, url)
        req = _request("RUNING", c, html)

        c.perform()
        return req.result()

    def post(self, url=None,
    data='',
    json=None

    ,  headers=None, verify=None, params=None, proxies=None, timeout=None,
                               allow_redirects=None):
        FOLLOWLOCATION = 5
        SSL_VERIFYPEER = 1
        SSL_VERIFYHOST = 1
        TIMEOUT = 15

        html = io.BytesIO()
        c = pycurl.Curl()
        c.setopt(c.HEADER, True)
        if allow_redirects == False:
            FOLLOWLOCATION = 0

        if verify == False:
            SSL_VERIFYPEER = 0
            SSL_VERIFYHOST = 0
        if timeout != None:
            TIMEOUT = timeout

        if headers != None:
            h = []
            for k, v in headers.items():
                h.append(k+": "+str(v))
            c.setopt(pycurl.HTTPHEADER, h)
            c.headers = headers
        else:
            c.headers = {}

        # 设置代理
        if proxies != None:
            name = None
            if 'http' in proxies:
                name = 'http'
            elif 'https' in proxies:
                name = 'https'
            if name != None:
                c.setopt(pycurl.PROXY, proxies[name])

        # 设置参数
        if params != None:
            url += "?"+urlencode(params)

        if type(data) == type({}):
            c.setopt(c.POSTFIELDS, urlencode(data))
        elif json == None:
            c.setopt(c.POSTFIELDS, data)
        else:
            c.setopt(c.POSTFIELDS, jsOn.dumps(json))

        # 设置html
        c.setopt(pycurl.WRITEFUNCTION, html.write)
        # 设置重定向
        c.setopt(pycurl.FOLLOWLOCATION, FOLLOWLOCATION)
        # 设置忽略证书
        c.setopt(pycurl.SSL_VERIFYPEER, SSL_VERIFYPEER)
        c.setopt(pycurl.SSL_VERIFYHOST, SSL_VERIFYHOST)
        # 设置超时
        c.setopt(pycurl.TIMEOUT, TIMEOUT)
        # 设置url
        c.setopt(pycurl.URL, url)
        req = _request("RUNING", c, html)
        return req.result()



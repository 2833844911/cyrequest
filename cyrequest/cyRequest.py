# -*- encoding: utf-8 -*-
# !/usr/bin/python3
'''
该库用于异步与同步请求
能自动试错

'''

from requests_futures.sessions import FuturesSession
import requests
import re
from queue import Queue
from cyrequest._pycurlToRe import pycurlToRe, pycurlToRetb


class _request:
    def __init__(self, id, response, request, data, errNum):
        self.id = id
        self.response = response
        self.request = request
        self.requestData = data
        self.errNum = errNum


class _error:
    def __init__(self, id, error, request, data, errNum):
        self.id = id
        self.error = error
        self.request = request
        self.requestData = data
        self.errNum = errNum


class cyRequest:
    def __init__(self, headers=None, cookie=None, verify=True, proxies=None, errback=None, errNum=1, max_workers=8,
                 session=None, typer=0):
        '''

        :param headers:请求头的设置
        :param cookie: 设置cookie
        :param verify: 设置是否信任ssl证书
        :param proxies: 设置代理
        :param errback: 设置失败后的回调
        :param errNum: 设置最大重试次数
        :param max_workers: 设置最大异步数量
        :param session: 输入requests.session会话
        :param typer: 切换pycurl或者requests
        '''
        self.responeList = []
        self.requestList = []
        self.errNum = errNum
        self.asnum = max_workers
        if typer == 1:
            self.session = pycurlToRe(max_workers=max_workers, session=session)
        else:
            self.session = FuturesSession(max_workers=max_workers, session=session)
        if verify != None:
            self.verify = verify
        if proxies != None:
            self.proxies = proxies
        else:
            self.proxies = {}
        if headers != None:
            self.session.headers = headers
        if cookie != None:
            self.session.cookie = cookie
        if errback == None:
            self.errback = self._errback
        else:
            self.errback = errback

    def _errback(self, e, callback, err, errfun):
        if e.requestData['AT'] == "GET":
            self.get(e.requestData['url'], e.requestData['headers'], e.requestData['verify'], e.requestData['proxies'],
                     e.requestData['params'], e.id, callback, e.requestData['timeout'], e.requestData['allow_redirects'], err, e.errNum, errfun)
        elif e.requestData['AT'] == "POST":
            self.post(e.requestData['url'], e.requestData['data'], e.requestData['json'], e.requestData['headers'],
                      e.requestData['verify'], e.requestData['proxies'], e.id,
                      callback, e.requestData['timeout'], e.requestData['allow_redirects'], err, e.errNum, errfun
                      )

    def get(self, url=None, headers=None, verify=None, proxies={},params=None, id=None, callback=None, timeout=20,
            allow_redirects=True, errback=None, _errNum=0, errfun=None):
        if verify == None:
            verify = self.verify
        if type(proxies) == type({}):
            if len(proxies) == 0:
                proxies = self.proxies
        self.requestList.append(
            ["GET", url, headers,params, verify, proxies, id, callback, timeout, allow_redirects, errback, _errNum, errfun])
        self._pushRequest()

    def _get(self, url=None, headers=None, params=None, verify=True, proxies=None, id=None, callback=None, timeout=20,
             allow_redirects=True, errback=None, errNum=None, errfun=None):

        if type(proxies) != type({}):
            proxiesstr_ = proxies.get()
            if proxiesstr_ == None:
                self.requestList.append(
                    ["GET", url, headers, params, verify, proxies, id, callback, timeout, allow_redirects, errback,
                     errNum, errfun])
                return
            if proxiesstr_[:5] != "https":
                proxies_ = {"http": proxiesstr_}
            else:
                proxies_ = {"http": "http" + proxiesstr_[5:], "https": "http" + proxiesstr_[5:]}
        else:
            proxies_ = proxies

        req = self.session.get(url, headers=headers, verify=verify,params=params, proxies=proxies_, timeout=timeout,
                               allow_redirects=allow_redirects)
        self.responeList.append([req, callback, id, errback,
                                 {"AT": "GET", "url": url, "headers": headers,"params":params, "verify": verify, "proxies": proxies_,
                                  "timeout": timeout, "allow_redirects": allow_redirects}, errNum, errfun, proxies])

    def post(self, url=None, data=None, json=None, headers=None, verify=None, proxies={}, id=None, callback=None,
             timeout=20, allow_redirects=True, errback=None, _errNum=0, errfun=None):
        if verify == None:
            verify = self.verify
        if type(proxies) == type({}):
            if len(proxies) == 0:
                proxies = self.proxies
        self.requestList.append(
            ["POST", url, data, json, headers, verify, proxies, id, callback, timeout, allow_redirects, errback, _errNum,
             errfun])
        self._pushRequest()

    def _post(self, url=None, data=None, json=None, headers=None, verify=True, proxies=None, id=None, callback=None,
              timeout=20, allow_redirects=True, errback=None, errNum=None, errfun=None):
        if type(proxies) != type({}):
            proxiesstr_ = proxies.get()
            if proxiesstr_ == None:
                self.requestList.append(
                    ["POST", url, data, json, headers, verify, proxies, id, callback, timeout, allow_redirects, errback,
                     errNum,
                     errfun])
                return
            if proxiesstr_[:5] != "https":
                proxies_ = {"http": proxiesstr_}
            else:
                proxies_ = {"http": "http" + proxiesstr_[5:], "https": "http" + proxiesstr_[5:]}
        else:
            proxies_ = proxies

        req = self.session.post(url, data=data, json=json, headers=headers, verify=verify, proxies=proxies_,
                                timeout=timeout, allow_redirects=allow_redirects)
        self.responeList.append([req, callback, id, errback,
                                 {"AT": "POST", "url": url, "data": data, "json": json, "headers": headers,
                                  "verify": verify, "proxies": proxies_, "timeout": timeout,
                                  "allow_redirects": allow_redirects}, errNum, errfun, proxies])

    def _pushRequest(self):
        for i in range(self.asnum - len(self.responeList)):
            if len(self.requestList) == 0:
                break
            datar = self.requestList.pop(0)
            if datar[0] == "GET":
                self._get(*datar[1:])
            elif datar[0] == "POST":
                self._post(*datar[1:])

    def advance(self):
        while len(self.responeList + self.requestList):
            self._pushRequest()
            deleList = []
            if 'updata' in dir(self.session):
                self.session.updata()
            for index, (req, callback, id, err, requestData, errNum, errfun, proxies) in enumerate(self.responeList):
                if req._state == "FINISHED":
                    if 'https' in requestData['proxies']:
                        proxiesstr_ = "https"+requestData["proxies"]['https'][4:]
                    elif 'http' in requestData['proxies']:
                        proxiesstr_ = requestData["proxies"]['http']
                    deleList.append(index)
                    try:
                        data = _request(id, req.result(), self, requestData, errNum)
                        if errfun != None:
                            enrr = errfun(data)
                            if enrr != True:
                                raise Exception(enrr)

                        if type(proxies) != type({}):
                            proxies.updata(proxiesstr_)

                        if callback != None:
                            callback(data)

                    except Exception as e:
                        if type(proxies) != type({}):
                            proxies.puterr(proxiesstr_)
                            requestData['proxies'] = proxies
                        errNum += 1
                        if self.errNum > errNum:
                            self._errback(_error(id, e, self, requestData, errNum), callback, err, errfun)
                            continue
                        if err == None:
                            self.errback(_error(id, e, self, requestData, errNum))
                        else:
                            err(_error(id, e, self, requestData, errNum))
            jf = 0
            deleList.sort()
            for i in deleList:
                self.responeList.pop(i - jf)
                jf += 1

    def adyield(self):
        while len(self.responeList) + len(self.requestList):
            self._pushRequest()
            if 'updata' in dir(self.session):
                self.session.updata()
            deleList = []
            for index, (req, callback, id, err, requestData, errNum, errfun, proxies) in enumerate(self.responeList):

                if req._state == "FINISHED":
                    if 'https' in requestData['proxies']:
                        proxiesstr_ = "https"+requestData["proxies"]['https'][4:]
                    elif 'http' in requestData['proxies']:
                        proxiesstr_ = requestData["proxies"]['http']

                    deleList.append(index)
                    try:
                        data = _request(id, req.result(), self, requestData, errNum)
                        if errfun != None:
                            e = errfun(data)
                            if e != True:
                                raise Exception(e)

                        data = _request(id, req.result(), self, requestData, errNum)
                        if errfun != None:
                            enrr = errfun(data)
                            if enrr != True:
                                raise Exception(enrr)

                        if type(proxies) != type({}):
                            proxies.updata(proxiesstr_)

                        if callback != None:
                            id = callback(data)
                        yield data
                    except Exception as y:

                        if type(proxies) != type({}):
                            proxies.puterr(proxiesstr_)
                            requestData['proxies'] = proxies

                        e = y
                        errNum += 1
                        if self.errNum > errNum:
                            self._errback(_error(id, e, self, requestData, errNum), callback, err, errfun)
                            continue
                        if err == None:
                            self.errback(_error(id, e, self, requestData, errNum))
                        else:
                            err(_error(id, e, self, requestData, errNum))
            jf = 0
            deleList.sort()
            for i in deleList:
                self.responeList.pop(i - jf)
                jf += 1
class cyProxy:
    def __init__(self, getProxy=None, proxyList=[], max=3, maxerr=2):
        '''

        :param getProxy: 返回一个代理的列表的函数
        :param proxyList: 初始化代理输入列表
        :param max: 最大的代理请求连接数
        :param maxerr: 最大的代理错误数
        '''
        self._proxies = {}
        self._badproxy = set('')
        self.maxerr = maxerr
        self._max = max
        self._getproxy = getProxy
        self._proxyList = proxyList
        self._Qproxy = Queue(maxsize=max * 5)
        self._putProxyDict()
        self._putProxy()

    def _putProxyDict(self):
        if self._getproxy != None:
            self._proxyList += self._getproxy()
        while 1:
            if len(self._proxyList) + self._Qproxy.qsize() == 0:
                if len(self._proxies) == 0:
                    raise Exception("代理不够了")
                return
            if len(self._proxyList) == 0:
                return
            s = self._proxyList.pop()
            if s in self._badproxy:
                if len(self._proxyList) == 0:
                    break
                continue
            self._proxies[s] = [self._max, 0]
            if len(self._proxyList) == 0:
                break

    def _putProxy(self):
        while 1:
            off2 = 0
            off = 1
            for k, v in self._proxies.items():
                if self._Qproxy.full():
                    off = 0
                    break
                elif v[0] > 0:
                    off2 = 1
                    self._Qproxy.put(k)
                    v[0] -= 1
            if off == 0 or off2 == 0:
                break

    def get(self):
        if self._Qproxy.empty():
            self._putProxyDict()
            self._putProxy()
            if self._Qproxy.empty():
                return None
        proxy = self._Qproxy.get()
        if self._Qproxy.qsize() < 4:
            self._putProxyDict()
            self._putProxy()
        return proxy

    def updata(self, proxy):
        if proxy not in self._proxies:
            return
        self._proxies[proxy][0] += 1

    def puterr(self, proxies):
        if proxies not in self._proxies:
            return
        self._proxies[proxies][1] += 1
        if self._proxies[proxies][1] >= self.maxerr:
            self._proxies.pop(proxies)
            self._badproxy.add(proxies)


def get(url=None, headers=None, verify=True, params=None, proxies={}, timeout=20, allow_redirects=True,
        errback=None, errNum=1, session=None, errfun=None, typer=0):
    if type(proxies) != type({}):
        proxiesstr_ = proxies.get()
        if proxiesstr_[:5] != "https":
            proxies_ = {"http": proxiesstr_}
        else:
            proxies_ = {"http": "http" + proxiesstr_[5:], "https": "http" + proxiesstr_[5:]}

    else:
        proxies_ = proxies
    requestData = {"AT": "GET", "url": url, "headers": headers, "verify": verify,"params":params, "proxies": proxies_,
                   "timeout": timeout, "allow_redirects": allow_redirects}
    if typer == 1:
        session = pycurlToRetb(session)
    elif session == None:
        session = requests.session()
    e = None
    for i in range(errNum):
        try:
            req = session.get(url=url, headers=headers, verify=verify, params=params, proxies=proxies_, timeout=timeout,
                              allow_redirects=allow_redirects)
            a = _request(url, req, session, requestData, errNum)
            if errfun != None:
                err = errfun(a)
                if err != True:
                    raise Exception(err)
            if type(proxies) != type({}):
                proxies.updata(proxiesstr_)
            return a
        except Exception as y:
            if type(proxies) != type({}):
                proxies.puterr(proxiesstr_)
                proxiesstr_ = proxies.get()
                if proxiesstr_[:5] != "https":
                    proxies_ = {"http": proxiesstr_}
                else:
                    proxies_ = {"http": "http" + proxiesstr_[5:], "https": "http" + proxiesstr_[5:]}
            e = y

    if errback != None:
        errback(_error(url, e, session, requestData, errNum))
    else:
        raise Exception(e)


def post(url=None, data=None, json=None, headers=None, verify=True, proxies={}, timeout=20, allow_redirects=True,
         errback=None, errNum=1, session=None, errfun=None, typer=0):
    if type(proxies) != type({}):
        proxiesstr_ = proxies.get()
        if proxiesstr_[:5] != "https":
            proxies_ = {"http": proxiesstr_}
        else:
            proxies_ = {"http": "http" + proxiesstr_[5:], "https": "http" + proxiesstr_[5:]}

    else:
        proxies_ = proxies

    requestData = {"AT": "GET", "url": url, "headers": headers, "verify": verify, "proxies": proxies_,
                   "timeout": timeout, "allow_redirects": allow_redirects}
    if typer == 1:
        session = pycurlToRetb(session)
    elif session == None:
        session = requests.session()
    e = None
    for i in range(errNum):
        try:
            req = session.post(url=url, data=data, json=json, headers=headers, verify=verify, proxies=proxies_,
                               timeout=timeout, allow_redirects=allow_redirects)

            a = _request(url, req, session, requestData, errNum)
            if errfun != None:
                err = errfun(a)
                if err != True:
                    raise Exception(err)

            if type(proxies) != type({}):
                proxies.updata(proxiesstr_)

            return a
        except Exception as y:
            if type(proxies) != type({}):
                proxies.puterr(proxiesstr_)
                proxiesstr_ = proxies.get()
                if proxiesstr_[:5] != "https":
                    proxies_ = {"http": proxiesstr_}
                else:
                    proxies_ = {"http": "http" + proxiesstr_[5:], "https": "http" + proxiesstr_[5:]}
            e = y

    if errback != None:
        errback(_error(url, e, session, requestData, errNum))
    else:
        raise Exception(e)




def cleanString(s):
    '''去除字符串中的多余字符'''
    return re.sub('\s+', ' ', s)


def getListdata_(data, key, listData):
    for i in data:
        if type(i) == type({}):
            getDictdata_(i, key, listData)


def getDictdata_(data, key, listData):
    if type(data) == type([]):
        getListdata_(data, key, listData)
    if type(data) == type({}):
        for k, v in data.items():
            if type(v) == type([]):
                getListdata_(v, key, listData)
            if type(v) == type({}):
                getDictdata_(v, key, listData)
            if k == key:
                listData.append(v)



def getDictdata(data, key):
    '''
    获取字典中一个键的值
    :param data: 传入字典
    :param key: 传入需要获取的健
    :return:
    '''
    myList = []
    getDictdata_(data, key, myList)
    return myList

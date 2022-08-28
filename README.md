README
# cyrequest文档
cyrequest可以实现自动试错，代理池管理的同步和异步请求的包，可以让我们能够更加简单的实现大批量请求


## 发送同步GET请求
```python
from cyrequest import cyRequest
req = cyRequest.get("http://www.baidu.com")
req.response.encoding = 'utf-8'
print(req.response.text)
```


## 通过requests的session发送get请求
```python
from cyrequest import cyRequest
import requests
s = requests.session()
req = cyRequest.get("http://www.baidu.com", session=s)
req.response.encoding = 'utf-8'
print(req.response.text)
```


## 发送同步GET请求并设置失败的callback
```python
from cyrequest import cyRequest


def errFun(a):
    # 输出报错
    print(a.error)
    # 输出请求的详细信息
    print(a.requestData)


req = cyRequest.get("http://www.baidu.com", errback=errFun)
req.response.encoding = 'utf-8'
print(req.response.text)
```

## 发送同步GET请求并设置重试次数
```python
from cyrequest import cyRequest

def errFun(a):
    # 输出报错
    print(a.error)
    # 输出请求的详细信息
    print(a.requestData)

req = cyRequest.get("http://www.baidu.com",
# 重试3次后失败的回调
 errback=errFun, 
# 设置重试3次， 3秒超时
errNum=3, timeout=3)
req.response.encoding = 'utf-8'
print(req.response.text)

## 发送同步GET请求并设置自定义报错
from cyrequest import cyRequest

def errFun(a):
    print(a.error)
    print(a.requestData)

def err(a):
    a.response.encoding = 'utf-8'
    if a.response.text.find("IP访问频繁稍后再试") != -1:
        # 判断返回的数据在是否包含该字符串然后返回自定义报错
        return "IP被封"
    # 返回True表示不报错，这样子就不会重试请求
    return True

req = cyRequest.get("http://www.baidu.com",
                     # 设置代理
                     proxies={"http":"http://127.0.0.1:8888"},
                     timeout=3, errback=errFun, errNum=3, errfun=err)
req.response.encoding = 'utf-8'
print(req.response.text)
```

## 发送同步POST请求
```python
from cyrequest import cyRequest

req = cyRequest.post("http://www.baidu.com", data={"cbb":"yhh"})
req.response.encoding = 'utf-8'
print(req.response.text)

```

## 通过requests的session发送POST请求
```python
from cyrequest import cyRequest
import requests
s = requests.session()
req = cyRequest.post("http://www.baidu.com", data={"cbb":"yhh"}, session=s)
req.response.encoding = 'utf-8'
print(req.response.text)
```

## 发送同步POST请求并设置失败的callback
```python
from cyrequest import cyRequest

def errFun(a):
    print(a.error)
    print(a.requestData)

req = cyRequest.post("http://www.baidu.com", data={"cbb":"yhh"}, errback=errFun)
req.response.encoding = 'utf-8'
print(req.response.text)
```


## 发送同步POST请求并设置重试次数
```python
from cyrequest import cyRequest

def errFun(a):
    print(a.error)
    print(a.requestData)

req = cyRequest.post("http://www.baidu.com", data={"cbb":"yhh"}, errback=errFun, errNum=3)
req.response.encoding = 'utf-8'
print(req.response.text)
```

## 发送同步POST请求并设置自定义报错
```python
from cyrequest import cyRequest

def err(a):
    a.response.encoding = 'utf-8'
    if a.response.text.find("IP访问频繁稍后再试") != -1:
        # 判断返回的数据在是否包含该字符串然后返回自定义报错
        return "IP被封"
    # 返回True表示不报错，这样子就不会重试请求
    return True

def errFun(a):
    print(a.error)
    print(a.requestData)

req = cyRequest.post("http://www.baidu.com", data={"cbb":"yhh"}, errback=errFun,errfun=err, errNum=3)
req.response.encoding = 'utf-8'
print(req.response.text)
```

## 发送异步get请求（无返回值）
```python
from cyrequest import cyRequest

def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)

s = cyRequest.cyRequest()

# 发送请求
s.get("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求"
      )
# 发送请求
s.get("https://cn.bing.com/",
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是必应首页的请求"
# 异步发送上面2个请求
s.advance()
```

## 发送异步post请求（无返回值）
```python
from cyrequest import cyRequest


def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)


s = cyRequest.cyRequest()


# 发送请求
s.post("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,data={"cbb":"yhh"},
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求"
      )
# 发送请求
s.post("https://cn.bing.com/",data={"cbb":"yhh"}
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是必应首页的请求"
# 异步发送上面2个请求
s.advance()
```

## 发送异步get请求（有返回值）
```python
from cyrequest import cyRequest


def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)


s = cyRequest.cyRequest()


# 发送请求
s.get("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求"
      )
# 发送请求
s.get("https://cn.bing.com/",
      # 设置请求成功后的回调，可以不设置
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback，可以不设置
      id="我是必应首页的请求"
# 异步发送上面2个请求
# 并且有返回值
for i in s.adyield():
    print(i.id)
    print(i.requestData)
```

## 发送异步post请求（有返回值）
```python
from cyrequest import cyRequest

def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)

s = cyRequest.cyRequest()

# 发送请求
s.post("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,data={"cbb":"yhh"},
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求"
      )
# 发送请求
s.post("https://cn.bing.com/",data={"cbb":"yhh"}
      # 设置请求成功后的回调，可以不设置
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback，可以不设置
      id="我是必应首页的请求"
页的请求"
# 异步发送上面2个请求
# 并且有返回值
for i in s.adyield():
    print(i.id)
    print(i.requestData)
```

## 发送异步请求设置重试次数
```python
from cyrequest import cyRequest

def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)
# 重试10次
s = cyRequest.cyRequest(errNum=10)

# 发送get请求
s.get("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求"
      )
# 发送post请求
s.post("https://cn.bing.com/",data={"cbb":"yhh"}
      # 设置请求成功后的回调，可以不设置
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback，可以不设置
      id="我是必应首页的请求"
# 异步发送上面2个请求
# 并且有返回值
for i in s.adyield():
    print(i.id)
    print(i.requestData)
```

## 发送异步请求设置最大异步数量
```python
from cyrequest import cyRequest


def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)
# 重试10次, 最大异步数量为10
s = cyRequest.cyRequest(errNum=10,max_workers=10)


# 发送get请求
s.get("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求"
      )
# 发送post请求
s.post("https://cn.bing.com/",data={"cbb":"yhh"}
      # 设置请求成功后的回调，可以不设置
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback，可以不设置
      id="我是必应首页的请求"
# 异步发送上面2个请求
# 并且有返回值
for i in s.adyield():
    print(i.id)
    print(i.requestData)
```

## 通过requests的session发送异步请求
```python
from cyrequest import cyRequest
import requests
session = requests.session()
def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)
# 重试10次, 最大异步数量为10
s = cyRequest.cyRequest(errNum=10,max_workers=10,session=session)

# 发送get请求
s.get("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求"
      )
# 发送post请求
s.post("https://cn.bing.com/",data={"cbb":"yhh"}
      # 设置请求成功后的回调，可以不设置
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback，可以不设置
      id="我是必应首页的请求"
# 异步发送上面2个请求
# 并且有返回值
for i in s.adyield():
    print(i.id)
    print(i.requestData)
```

## 代理池管理
同步代理设置和异步代理设置和requests的设置类似
```python
# 可以为这个实例下所有的请求设置代理，也可以单独设置
s = cyRequest.cyRequest(errNum=10,max_workers=10,session=session,
proxies={"http":"http://127.0.0.1:8888"})
cyrequest有代理池管理模块，该模块可以自动管理每个代理可同时被多少个request请求使用，错误多少次后删除并记录该代理
## 异步使用代理池管理
from cyrequest import cyRequest

def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)
# 创建一个代理池管理模块
proxiesList = cyRequest.cyProxy(
    # 初始化代理池
    proxyList=[
    "https://192.168.32.22:8090",
    # http代理
    "http://127.0.0.1:888",
    # https代理
        
    ], 
    # 最大有3个请求共同使用这个代理（默认3个）
    max=3,
    # 这个代理最大错误几次后会被舍弃
    maxerr=3
)

s = cyRequest.cyRequest(max_workers=10,  errNum=20)

# 发送请求
s.get("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求",
      # 设置代理
      proxies=proxiesList,
      
      timeout=4
      )

for i in s.adyield():
    print(i.id)
    print(i.requestData)


```
## 异步使用代理池管理，代理池自动获取代理（当代理数量不足会自动调用函数获取代理）
```python
from cyrequest import cyRequest

def sucess(a):
    print(a.response.text)
    print(a.requestData)
    print(a.id)

def getProxies():
    req = cyRequest.get("http://101.35.218.236:5010/get")
    # 下面返回 101.36.33.33:8080
    text = req.response.text
    # 设置https代理
    proxy = "https://"+text
    
    # 设置http代理
    # proxy = "http://" + text
    
    # 返回一个代理给线程池（可以返回多个）
    return [proxy]

proxiesList = cyRequest.cyProxy(
    # 设置获取代理的函数
    getProxy=getProxies,
    # 最大有3个请求共同使用这个代理（默认3个）
    max=3,
    # 这个代理最大错误几次后会被舍弃
    maxerr=3
)

s = cyRequest.cyRequest(max_workers=10,  errNum=20)

# 发送请求
s.get("http://www.baidu.com",
      # 设置请求成功后的回调
      callback=sucess,
      # 可以携带请求的一些信息，可传递到callback
      id="我是百度首页的请求",
      # 设置代理
      proxies=proxiesList,

      timeout=4
      )

for i in s.adyield():
    print(i.id)
    print(i.requestData)
```

## 还有更多模块正在开发哦，有什么意见可加q 2833844911 或者邮箱发给我哦（2833844911@qq.com）
作者：陈不不
b站：[https://space.bilibili.com/227452348](https://space.bilibili.com/227452348?spm_id_from=333.1007.0.0)

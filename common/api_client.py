import requests
import logging
logger=logging.getLogger(__name__)

class ApiClient:
    def __init__(self,base_url:str,token:str=""):
        self.base_url=base_url
        self.session=requests.session()
        if token!= "":
            self.session.headers.update({"Authorization":f"Bearer {token}"})


    def _request(self,method:str,path:str,**kwargs):
        resp=self.session.request(url=f"{self.base_url}{path}",
                              method=method,
                              **kwargs,
                              timeout=10)
        logger.info(f"发送{method}请求,请求路径{self.base_url}{path},请求内容{kwargs}")
        return resp
    

    def get(self,path:str,**kwargs):
        return self._request(method="GET",path=path,**kwargs)
    

    def post(self,path:str,**kwargs):
        return self._request(method="POST",path=path,**kwargs)
    
    def delete(self,path:str,**kwargs):
        return self._request(method="DELETE",path=path,**kwargs)
    
    def put(self,path:str,**kwargs):
        return self._request(method="PUT",path=path,**kwargs)

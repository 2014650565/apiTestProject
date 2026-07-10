import yaml

#读取yaml中对应键的值
def yaml_read(path,key=None):
    with open(path,mode="r",encoding="utf-8") as f:
        if key != None:
            return yaml.safe_load(f)[key]
        else:
            return yaml.safe_load(f)
    

#给yaml文件添加值
def yaml_write(path,data):
    with open(path,'a+',encoding="utf-8") as f:
        yaml.safe_dump(stream=f,data=data,allow_unicode=True)      #允许中文



def yaml_clean(path):
    with open(path,'w') as f:
        return
    

if __name__=='__main__':
    pass
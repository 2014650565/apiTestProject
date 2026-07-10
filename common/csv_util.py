import csv

#读取csv文件(跳过第一行)
def csv_read(path):
    with open(path,'r',encoding="utf-8") as f:
        return list(csv.reader(f))[1:]
    





if __name__=='__main__':
    pass
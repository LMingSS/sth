# FROM https://medium.com/%E7%A8%8B%E5%BC%8F%E4%B9%BE%E8%B2%A8/python-with-as-%E6%B5%81%E7%A8%8B%E6%8E%A7%E5%88%B6-bc5850dee667

import os
import json

string = '''{
    "facebook":{
        "old":{
            "USER":"user1",
            "PASSWORD":"pass1"},
        "new":{
            "USER":"user2",
            "PASSWORD":"pass2"
}
    },
    "aws":{
        "asia":{
            "ACCOUNT":"ac1",
            "PASSWORD":"pw1"
        },
        "southeast":{
            "ACCOUNT":"ac2",
            "PASSWORD":"pw2"
        }
    }
}'''
dic = eval(string)

with open("with.json", 'w') as f:
    json.dump(dic, f)
    
#%% 常見的讀取方式 1

fn = "with.json"
fp = os.path.join(os.getcwd(), fn)

with open(fp) as f01:
    data1 = f01.read()

print(type(data1))      # <class 'str'>
print(data1)

#   常見的讀取方式 2

f02 = open(fp)
data2 = f02.read()

f02.close()             # 不關會一直佔著記憶體

print(type(data2))      # <class 'str'>
print(data2)

#   檢查檔案是不是確實有被關閉

if f01.closed:
	print("\nf01 is closed")
else:
	print("f01 is still not closed")

if f02.closed:
	print("f02 is closed")
else:
	print("f02 is still not closed")

#%%

class Calculator(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):    # 進入
        print(f"You are now using calculator--{self.name}")
        return self

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def __exit__(self, type, value, traceback):     # 退出
        print(f"You are now exiting calculator-{self.name}, bye bye~~")

with Calculator("test1245") as c:
    add_result = c.add(4, 6)
    print(f"The adding result of 4 & 6 is {add_result}")
    sub_result = c.sub(9, 3)
    print(f"The subtract between of 9 & 3 is {sub_result}")

# You are now using calculator--test1245                # 進入
# The adding result of 4 & 6 is 10
# The subtract between of 9 & 3 is 6
# You are now exiting calculator-test1245, bye bye~~    # 退出


#%%

f = open(fp)
data = f.read()

print(type(f))      # <class '_io.TextIOWrapper'>
print(dir(f)) 
'''['_CHUNK_SIZE',
 '__class__',
 '__del__',
 '__delattr__',
 '__dict__',
 '__dir__',
 '__doc__',
 '__enter__',       <----------
 '__eq__',
 '__exit__',        <----------
 '__format__',
 '__ge__',
 '__getattribute__',
 '__getstate__',
 '__gt__',
 '__hash__',
 '__init__',
 '__init_subclass__',
 '__iter__',
 '__le__',
 '__lt__',
 '__ne__',
 '__new__',
 '__next__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 '_checkClosed',
 '_checkReadable',
 '_checkSeekable',
 '_checkWritable',
 '_finalizing',
 'buffer',
 'close',
 'closed',
 'detach',
 'encoding',
 'errors',
 'fileno',
 'flush',
 'isatty',
 'line_buffering',
 'mode',
 'name',
 'newlines',
 'read',
 'readable',
 'readline',
 'readlines',
 'reconfigure',
 'seek',
 'seekable',
 'tell',
 'truncate',
 'writable',
 'write',
 'write_through',
 'writelines']'''

f.close()
# 總結
# with as 就是為了 class 中的 __enter__() , __exit__() 而生的流程控制 

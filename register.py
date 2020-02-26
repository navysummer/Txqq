# --*-- coding:utf-8 --*--
import time
import hashlib
import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup,element
# from tkinter import filedialog
# from tx import Tx
try:
    import urlparse
except Exception as e:
    from urllib import parse as urlparse

class Register(object):
    def __init__(self, url='http://txqq789.com',pre='NavySummer'):
        self.url = url
        self.parsed_tuple = urlparse.urlparse(self.url)
        self.pre = pre
        self.headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Upgrade-Insecure-Requests":"1",
        "Host":self.parsed_tuple.netloc,
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
        self.title = '手机特讯网'
        self.root = Tk()
        self.root.title(self.title)
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        ww = 220
        wh = 105
        px = (self.sw-ww) / 2
        py = (self.sh-wh) / 2
        self.root.geometry("%dx%d+%d+%d" %(ww,wh,px,py))
        self.root.resizable(0,0)
        self.initWindow()
        self.root.mainloop()

    def initWindow(self):
        self.urlLabel = Label(self.root,text='地址')
        self.urlEntry = Entry(self.root)
        self.urlEntry.insert(0, "http://txqq789.com")
        self.timeLabel = Label(self.root,text='时间间隔(s)')
        self.timeEntry = Entry(self.root)
        self.timeEntry.insert(0, "5")
        self.numLabel = Label(self.root,text='账号数量')
        self.numEntry = Entry(self.root)
        self.numEntry.insert(0, "1")
        self.regBtn = Button(self.root,text='注册',command=self.getUserWindow)
        self.urlLabel.grid(row=0,column=0)
        self.urlEntry.grid(row=0,column=1)
        self.timeLabel.grid(row=1,column=0)
        self.timeEntry.grid(row=1,column=1)
        self.numLabel.grid(row=2,column=0)
        self.numEntry.grid(row=2,column=1)
        self.regBtn.grid(row=3,column=0,columnspan=2)


    def getUserWindow(self):
        self.url = self.urlEntry.get().strip()
        self.urlLabel.grid_forget()
        self.urlEntry.grid_forget()
        self.timeLabel.grid_forget()
        self.timeEntry.grid_forget()
        self.numLabel.grid_forget()
        self.numEntry.grid_forget()
        self.regBtn.grid_forget()
        self.root.title(self.title)
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        ww = 360
        wh = 325
        px = (self.sw-ww) / 2
        py = (self.sh-wh) / 2
        self.root.geometry("%dx%d+%d+%d" %(ww,wh,px,py))
        self.root.resizable(0,0)
        self.extendFrame = Frame(self.root)
        self.textFrame = Frame(self.root)
        self.scroll = Scrollbar(self.textFrame)
        self.info = Text(self.textFrame)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.scroll.config(command=self.info.yview)
        self.info.config(yscrollcommand=self.scroll.set)
        self.info.pack(side=LEFT, fill=Y)
        # self.buttonFrame.pack()
        self.extendFrame.pack()
        self.textFrame.pack()
        menu = Menu(self.root, tearoff=0)
        self.root.config(menu =menu)
        about = Menu(menu, tearoff=0)
        # menu.add_cascade(label="File", menu=fileBar)
        about.add_command(label="关于", command=self.about)
        menu.add_cascade(label="帮助", menu=about)
        second = float(self.timeEntry.get().strip())
        num = int(self.numEntry.get().strip())
        for i in range(num):
            name = self.getMd5(str(int(time.time())))
            self.register(name,2,18,'','ceshi123456','ceshi123456')
            self.info.config(state=NORMAL)
            hr = '\n------------------------------------------------\n'
            self.info.insert(END,hr)
            self.info.config(state=DISABLED)

    def getMd5(self,string):
        hl = hashlib.md5()
        hl.update(string.encode(encoding='utf-8'))
        return hl.hexdigest()[-12:]

    def about(self):
        messagebox.showinfo('关于','作者：海军\nQQ:1539920886')


    def register(self,name,sex,age,promo,passwd,vpass):
        url = '%s/login/regist.aspx'%(self.url)
        r = requests.get(url,headers=self.headers)
        self.cookies = r.cookies
        time.sleep(5)
        data = {
            "name":name,
            "sex":sex,
            "age":age,
            "promo":promo,
            "pass":passwd,
            "vpass":vpass,
            "act":"ok"
        }
        r = requests.post(url,cookies=self.cookies,data=data)
        # userinfo = r.text
        # print(r.status_code)
        soup = BeautifulSoup(r.text,'lxml')
        userinfo = str(soup.text)
        # print(userinfo)
        # if userinfo.find("你已经注册过了需要再注册请联系QQ1608503062！或QQ3030521413！") != -1:
        #     userinfo = '用户ID：%s\n密码:%s\n'%(name,passwd)
        # else:
        #     userinfo = '注册失败'
        self.info.config(state=NORMAL)
        self.info.insert(END,userinfo)
        self.info.config(state=DISABLED)

        # return userinfo


def main():
    Register()
    # reg=Register()
    # name='cjdididss'
    # sex=2
    # age=55
    # promo=''
    # passwd='ceshiseeee'
    # vpass='ceshiseeee'
    # user = reg.register(name,sex,age,promo,passwd,vpass)
    # print(user)

if __name__ == '__main__':
    main()




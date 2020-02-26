# --*-- coding:utf-8 --*--
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tx import Tx

class Shequ(object):
    def __init__(self):
        self.title = '手机特讯网'
        self.root = Tk()
        self.root.title(self.title)
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        ww = 170
        wh = 60
        px = (self.sw-ww) / 2
        py = (self.sh-wh) / 2
        self.root.geometry("%dx%d+%d+%d" %(ww,wh,px,py))
        self.root.resizable(0,0)
        self.GetUserWindow()
        self.root.mainloop()

    def GetUserWindow(self):
        self.urlLabel = Label(self.root,text='地址')
        self.urlEntry = Entry(self.root)
        self.urlEntry.insert(0, "http://txqq789.com")
        self.userBtn = Button(self.root,text='设置用户',command=self.getUser)
        self.urlLabel.grid(row=0,column=0)
        self.urlEntry.grid(row=0,column=1)
        self.userBtn.grid(row=1,column=0,columnspan=2)

    def getUser(self):
        filename =filedialog.askopenfilename()
        users = []
        with open(filename,'r') as f:
            lusers = f.readlines()
            try:
                users = [{'name':i.strip().split('=')[0],'passwd':''.join(i.strip().split('=')[1:])}for i in lusers]
            except Exception as e:
                pass
        if not users:
            messagebox.showerror('错误','%s文件里没有账号'%(filename))
        else:
            self.users = users
            self.operateWindow()

    def operateWindow(self):
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        ww = 360
        wh = 325
        px = (self.sw-ww) / 2
        py = (self.sh-wh) / 2
        self.root.geometry("%dx%d+%d+%d" %(ww,wh,px,py))
        self.root.resizable(0,0)
        self.urlLabel.grid_forget()
        self.urlEntry.grid_forget()
        self.userBtn.grid_forget()
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
        # menu.add_command(label="Undo", command=self.about)
        self.operate()

    def about(self):
        messagebox.showinfo('关于','作者：海军\nQQ:1539920886')

    def operate(self):
        for user in self.users:
            userId = user['name']
            passwd = user['passwd']
            status = self.wlogin(userId,passwd)
            # print(status)
            if status == 0:
                self.gohome()
                self.baoming()
            self.info.config(state=NORMAL)
            self.info.insert(END,'\n------------------------------------------------\n')
            self.info.config(state=DISABLED)
            self.tx.logout()
            time.sleep(5)



    def wlogin(self,user,passwd):
        url = self.urlEntry.get()
        self.tx = Tx(url,user,passwd,0)
        status = self.tx.status
        # print(user,passwd,status)
        self.info.config(state=NORMAL)
        if status == 0:
            self.tx.get_family_id()
            userinfo = '当前登录用户ID：%s\n当前登录用户名：%s\n当前登录用户家族ID：%s\n当前登录用户家族名称：%s\n'%(str(self.tx.userId),self.tx.username,str(self.tx.family_id),self.tx.family_name)
            self.info.insert(END,userinfo)
            self.info.config(state=DISABLED)
        else:
            userinfo = '当前登录用户ID：%s\n'%(user)
            self.info.insert(END,userinfo)
            self.info.config(state=DISABLED)
        return status


    def gohome(self):
        self.info.config(state=NORMAL)
        qiandaoStatus = self.tx.qiandao()
        self.info.insert(END,'\n签到信息：\n'+qiandaoStatus)
        treeStatus = self.tx.famiy_wee()
        self.info.insert(END,'\n守护树：\n'+treeStatus)
        caiStatus = self.tx.caishen()
        self.info.insert(END,'\n财神：\n'+caiStatus)
        self.info.config(state=DISABLED)

    def baoming(self):
        self.info.config(state=NORMAL)
        baomingStatus = self.tx.baoming()
        self.info.insert(END,'\n报名族斗：\n'+baomingStatus)
        self.info.config(state=DISABLED)




def main():
    Shequ()

if __name__ == '__main__':
    main()
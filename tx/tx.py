# --*-- coding:utf-8 --*--
import re
import requests
try:
    import urlparse
except Exception as e:
    from urllib import parse as urlparse
# from lxml import etree
from bs4 import BeautifulSoup,element

class Tx(object):
    def __init__(self,url="http://txqq789.com",user="",passwd="",login_type=0):
        self.url = url
        self.parsed_tuple = urlparse.urlparse(self.url)
        self.user = user
        self.passwd = passwd
        self.login_url = "%s/login/login.aspx"%(self.url)
        self.headers = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": self.parsed_tuple.netloc,
        # "Referer": self.login_url,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
        self.status = None
        self.family_id = None
        if login_type == 0:
            self.login(self.url,self.user,self.passwd)
        # else:
        #     other_login_url = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&response_type=code&client_id=101265654&redirect_uri=http://txqq789.com/api/qqlogin.aspx&state=88371|PdRfAueQa3cgtrWbBqOqsTbU5DTM|2|txqq789.com&scope=get_user_info'
        #     self.qq_login(other_login_url)


    def login(self,url,user,passwd):
        self._login_url = "%s/server/login.aspx?name=%s&pass=%s"%(self.url,self.user,self.passwd)
        r = requests.get(self._login_url,headers=self.headers)
        self.cookies = r.cookies
        status = int(r.text.split('{')[1].split('}')[0].split(':')[1].strip())
        self.status = status
        home_url = '%s/home/my_home.aspx'%(self.url)
        r = requests.get(home_url,cookies=self.cookies)
        soup = BeautifulSoup(r.text,'lxml')
        self.userId = soup.find('div',class_='header').find('a').text
        self.username = soup.find('div',class_='bar').next_sibling.next_sibling.text
        # print(status)
        # if status != 0:
        #     exit()
    def logout(self):
        logout_url = '%s/login/out.aspx'%(self.url)
        requests.get(logout_url,cookies=self.cookies)

    def qq_login(self,url):
        print(url)
        # r = requests.get(url,headers=self.headers,allow_redirects=False)
        r = requests.get(url)

    def family(self):
        # self.get_family_id()
        qiandaoStatus = self.qiandao()
        treeStatus = self.famiy_wee()
        caiStatus = self.caishen()
        return qiandaoStatus,treeStatus,caiStatus


    def get_family_id(self):
        hurl = '%s/bbs/my_family.aspx'%(self.url)
        r = requests.get(hurl,cookies=self.cookies)
        soup = BeautifulSoup(r.text,'lxml')
        info = urlparse.urlparse(r.url)
        params = urlparse.parse_qs(info.query)
        try:
            self.family_name = soup.find('div',class_='hengxian').next_sibling.text
            self.family_id = params['id'][0]
        except Exception as e:
            self.family_name = None
            self.family_id = None
        

        
    def qiandao(self):
        qurl = '%s/bbs/my_qid.aspx?id=%s'%(self.url,self.family_id)
        r = requests.get(qurl,cookies=self.cookies)
        a = BeautifulSoup(r.text,'lxml').find('div', align="center").find('a')
        if a:
            qdurl = '%s/bbs/my_qid_ok.aspx?id=%s'%(self.url,self.family_id)
            r = requests.get(qdurl,cookies=self.cookies)
        # print(r.text)
        soup = BeautifulSoup(r.text,'lxml')
        try:
            status = soup.find('div',align='center').find('div',class_='hotline21').find('b').text
        except Exception as e:
            status = '今日未签到'
        return status



    def famiy_wee(self):
        furl = '%s/bbs/famiy_wee.aspx?id=%s'%(self.url,self.family_id)
        r = requests.get(furl,cookies=self.cookies)
        soup = BeautifulSoup(r.text,'lxml')
        status = soup.find('div',class_='header').next_sibling.next_sibling.strip()
        return status

    def caishen(self):
        curl = '%s/bbs/family_wee.aspx?id=%s'%(self.url,self.family_id)
        r = requests.get(curl,cookies=self.cookies)
        soup = BeautifulSoup(r.text,'lxml')
        status = soup.find('div',class_='header').next_sibling.next_sibling.strip()
        return status

    def baoming(self):
        bmurl = '%s/bbs/family_cybm.aspx?bid=%s'%(self.url,self.family_id)
        r = requests.get(bmurl,cookies=self.cookies)
        soup = BeautifulSoup(r.text,'lxml')
        status = soup.find('div',class_='bar').next_sibling.strip()
        return status
    # def ledou(self,ltype=1):
    #     lurl = '%s/bbs/ld.aspx?bid=%s&bt=%s'%(self.url,self.family_id,ltype)
    #     r = requests.get(lurl,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     bar = soup.find('div',class_='bar')
    #     zdl = bar.next_sibling.next_sibling.next_sibling
    #     tlz = zdl.next_sibling.next_sibling.split('[')[0].strip()
    #     duixiang = [{'url':self.url+'/bbs/'+i.attrs['href'],'name':i.next_sibling}for i in soup.find_all('a') if i.text==u'\u6597\u4e00\u6597']
    #     # print(duixiang)
    #     ledou_info = {
    #         'zdl':zdl,
    #         'tlz':tlz,
    #         'duishou':duixiang
    #     }
    #     # print(ledou_info)
    #     return ledou_info

    # def jledou(self,url):
    #     r = requests.get(url,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     bar = soup.find('div',class_='bar')
    #     zdl = bar.next_sibling.next_sibling.next_sibling.next_sibling
    #     tlz = zdl.next_sibling.next_sibling
    #     rs = tlz.next_sibling.next_sibling.next_sibling.next_sibling
    #     result = '%s\n%s\n%s'%(zdl,tlz,rs)
    #     print(result)

    # def zudou(self):
    #     zurl = '%s/bbs/bu.aspx?bid=%s'%(self.url,self.family_id)
    #     r = requests.get(zurl,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     bar = soup.find('div',class_='bar')
    #     zdl = bar.next_sibling.next_sibling.next_sibling.next_sibling
    #     gxz = zdl.next_sibling.next_sibling.next_sibling
    #     duixiang = [{'durl':self.url+'/bbs/'+i.attrs['href'],'uurl':self.url+i.next_sibling.next_sibling.attrs['href'],'name':i.next_sibling.next_sibling.text}for i in soup.find_all('a') if i.text==u'\u6311\u6218']
    #     zudou_info = {
    #         'zdl':zdl,
    #         'gxz':gxz,
    #         'duixiang':duixiang
    #     }
    #     # print(zudou_info)
    #     return zudou_info

    # def radomZudou(self):
    #     rzurl = '%s/bbs/ii.aspx?bid=%s'%(self.url,self.family_id)
    #     r = requests.get(rzurl,cookies=self.cookies)
    #     info = urlparse.urlparse(r.url)
    #     params = urlparse.parse_qs(info.query)
    #     userid = params['id'][0]
    #     rsurl = '%s/bbs/profile.aspx?id=%s'%(self.url,str(userid))
    #     r = requests.get(rsurl,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     bar = soup.find('div',class_='bar')
    #     form = soup.find('form')
    #     result = get_content_between_tables(bar, form)
    #     # result = soup.find('div',class_='header').next_sibling
    #     # print(result)
    #     return result

    # def zudouduishou(self,url,page=1):
    #     zurl = url + '&page=' + str(page)
    #     r = requests.get(zurl,cookies=self.cookies)
    #     # print(r.text)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     duishoulist = soup.find('div',class_='list').find_all('div',class_='row')[:-1]
    #     dl = [{'name':i.find_all('a')[0].text,'uurl':self.url+i.find_all('a')[0].attrs['href'],'durl':self.url+'/'+i.find_all('a')[1].attrs['href']} for i in duishoulist]
    #     # print(dl)
    #     return dl


    # def get_zudou_jiazu(self,page=1):
    #     url = '%s/bbs/topic_tzjz.aspx'%(self.url)
    #     r = requests.get(url,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     jiazulist = [{'name':i.text,'url':self.url+'/bbs/'+i.attrs['href']}for i in soup.find('div',class_='list').find_all('a')]
    #     # print(jiazulist)
    #     return jiazulist

    # def search_tie(self,keyword):
    #     search_url = '%s/bbs/topic_search.aspx?id=4&re=&ge=&wd=%s'%(self.url,keyword)
    #     r = requests.get(search_url,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     return soup

    # def jzudou(self,url):
    #     r = requests.get(url,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')

    # def fruit(self):
    #     gurl = '%s/bbs/gs.aspx?bid=%s'%(self.url,self.family_id)
    #     r = requests.get(gurl,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     bar = soup.find('div',class_='bar')
    #     bfruit = bar.next_sibling.next_sibling.next_sibling
    #     pfruit = bfruit.next_sibling.next_sibling
    #     cfruit = pfruit.next_sibling.next_sibling
    #     fnum = {
    #         'bfruit':int(bfruit[-1]),
    #         'pfruit':int(pfruit[-1]),
    #         'cfruit':int(cfruit[-1])
    #     }
    #     print(fnum)

    # def each_fruit(self,oid,sl):
    #     eurl = '%s/bbs/gs_ok.aspx?bid=%s'%(self.url,self.family_id)
    #     data = {
    #         'oid':oid,
    #         'sl':sl
    #     }
    #     r = requests.post(eurl,cookies=self.cookies,data=data)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     bar = soup.find('div',class_='bar')
    #     status = bar.next_sibling.next_sibling.next_sibling
    #     print(status)

    # def huitie(self,tieId,content):
    #     hturl = '%s/wml/bbs/reply_add.aspx?id=%s'%(self.url,tieId)
    #     data = {
    #         'cont':content,
    #         'act':'ok'
    #     }
    #     r = requests.post(hturl,cookies=self.cookies,data=data)

    # def get_tiezi_list(self,lid,tid='',page=1):
    #     url = '%s/bbs/forum.aspx?id=%s&tid=%s&page=%s'%(self.url,lid,tid,page)
    #     r = requests.get(url,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     divs = soup.find_all('div')
    #     hengxian = soup.find('div',class_='hengxian')
    #     footer = soup.find('div',class_='footer')
    #     ih = divs.index(hengxian)
    #     it = divs.index(footer)
    #     tls = [{'title':div.find('a').text,'url':self.url+div.find('a').attrs['href'],'author':div.find('font').text} for div in divs[ih+1:it-1] if div.find('font')]
    #     print(tls)

    # def get_tiezi(self,tieId,page=1):
    #     url = '%s/wml/bbs/topic.aspx?id=%s'%(self.url,tieId)
    #     r = requests.get(url,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     title = soup.find('b',id="tdName").text
    #     content = soup.find('div',id="tdCont").text
    #     author = [a for a in soup.find_all('a') if a.find('font')][0].text
    #     if page != 1:
    #         htlurl = '%s/bbs/reply_list.aspx?id=%s&page=%s'%(self.url,tieId,page)
    #         r = requests.get(htlurl,cookies=self.cookies)
    #         soup = BeautifulSoup(r.text,'lxml')
    #     htielist = [div.text[:-4] for div in soup.find('div',class_='list').find_all('div')[:-1]]
    #     print(htielist)

    # def fatie(self,lid):
    #     fturl = '%s/wml/bbs/topic_add.aspx?id=%s'%(self.url,lid)
    #     data = {
    #         'name':name,
    #         'dtext':dtext,
    #         'act':'发表'
    #     }
    #     r = requests.post(fturl,cookies=self.cookies,data=data)

    # def get_chat_room(self,chat_room_id=4,page=1):
    #     url = '%s/bbs/chat/room.aspx?id=%s&page=%s'%(self.url,chat_room_id,page)
    #     r = requests.get(url,cookies=self.cookies)
    #     soup = BeautifulSoup(r.text,'lxml')
    #     divs = soup.find_all('div')
    #     chat_list = [div.text for div in divs if not div.attrs.has_key('class')]
    #     print(chat_list)

    # def chat(self,content1,chat_room_id=4):
    #     url = '%s/bbs/chat/room.aspx?id=%s'%(self.url,chat_room_id)
    #     data = {
    #         'content1':content1,
    #         'act':'发送传音'
    #     }
    #     r = requests.post(hturl,cookies=self.cookies,data=data)





# def main():
    # url = 'http://txqq789.com'
#     # not 
#     # user = '72355'
#     # passwd = '15399208862020'
#     # yes
#     # user = '72668'
#     # passwd = 'xia990722'
    # user = '72205'
    # passwd = '15399208862020'
    # tx = Tx(url,user,passwd,0)
    # tx.get_zudou_jiazu()
    # zurl = 'http://txqq789.com/bbs/family_jzld.aspx?bid=9868&sid=72205.KjIzz2H1IhlXbxBjq5ExL3'
    # tx.zudouduishou(zurl)
    # tx.get_family_id()
    # tx.ledou()


# if __name__ == '__main__':
#     main()


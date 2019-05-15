import requests
import json
import time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TestProp:
    def __init__(self):
        self.url = 'https://webcast-test.maopp.cn'
        self.header = {
            'sign':'082b14705d9254017df3839638758a495d67544b63d00498',
            'token':'mp_224_3.1.1_',
            'netType':'a',
            'userId':'4099886',
            'appVersion':'4.2',
            'Content-Type':'application/json;charset=utf-8',
            'equipNum':'bb'
        }
        self.dprop = {}
        self.httpsession = requests.session()

    def parseJson(self,s):
        try:
            d = json.loads(s)
        except Exception as e:
            print(str(e))
            return None
        return d

    def refresh(self,path,data):
        rurl = self.url + path
        param = data
        try:
            r = self.httpsession.post(rurl,data=param,headers=self.header,verify=False)
            rd = self.parseJson(r.text)
            if rd['code'] == 1000:
                return True
            else:
               print(str(rd['code']),rd['msg'])
        except Exception as e:
            print(str(e))    


    def getresult(self,path,data):
        rurl = self.url + path
        param = data
        try:
            r = self.httpsession.post(rurl,data=param,headers=self.header,verify=False)
            rd = self.parseJson(r.text)
            if rd['code'] == 1000:
                listd = rd['data']['shopList']
                for i in listd:
                    name = i['goodsName']
                    if name in self.dprop:
                        self.dprop[name] =self.dprop[name] +1
                    else:
                        self.dprop[name] = 1
            else:
                print(str(rd['code']),rd['msg'])
        except Exception as e:
            print(str(e))
    
    def count(self):
        return self.dprop

def main():
    p = TestProp()
    num = 0
    for i in range(100):
        if p.refresh('/tribe/refresh','{"amountId":6,"tribeId":12424286}'):
            num = num + 1
            p.getresult('/tribe/queryShopList','{"tribeId":12424286}')
    res = p.count()
    print ('一共刷新商店%d次' % (num*6))
    for k,v in res.items():
        print(k,':',str(v), '概率为：%.2f%%' % ((v/num)*100/6))

if __name__ == '__main__':
    t1 = time.time()
    main()
    t2 = time.time()
    print('use time %d' % (int(t2 - t1)))
    





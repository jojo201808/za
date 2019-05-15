import unittest
import requests
import pymysql
import time
import json

class Testbill(unittest.TestCase):
    #连接数据库,定义家族id，邀约用户userid，两个受邀用户的id,打赏用户userid
    #提交邀约订单的请求头，url，以及post的参数
    @classmethod
    def setUpClass(cls):
        cls.db = pymysql.connect(host='106.14.193.137',user='tester',password='^tJgfeoiKRe_ZWYO',db='bubble',port=6603)
        cls.cursor = cls.db.cursor()
        cls.inviteuser = '4118678'
        cls.beinviteuser = '728066'
        cls.family = '4546871'
        cls.beinviteuser2 ='4100610'
        cls.payuser = '237052'
        cls.tommowtime = time.strftime('%m-%d',time.localtime(time.time()+60*60*24))
        cls.prensentid1 = 16
        cls.presentcount1 = 2
        cls.presenttype1 = 2
        cls.header = {
            'sign':'082b14705d9254017df3839638758a495d67544b63d00498',
            'token':'mp_224_3.1.1_',
            'netType':'a',
            'userId':'4099886',
            'appVersion':'4.2',
            'Content-Type':'application/json;charset=utf-8',
            'equipNum':'bb'
        }
        cls.cmurl = 'https://api-test.maopp.cn/bubble-alalive/inviteAnchor/determine'  #发起邀约
        cls.cmdata = {
	        "anchorId":728066,
	        "time":"04-11",
	        "hourId":150,
	        "giftList":[{"giftId":"1","giftNum":"2"}]
        }
        cls.acurl = 'https://api-test.maopp.cn/bubble-alalive/inviteAnchor/handelInvite' #接收邀约
        cls.adata ={
            "orderId":390,
	        "type":1
        }
        cls.lcurl = 'https://api-test.maopp.cn/bubble-alalive/inviteAnchor/newList'  # 邀约列表信息
        cls.ldata = {
	        "currentPage":1,
	        "type":1
        }
        #送礼接口
        cls.rurl ='https://api-test.maopp.cn/bubble-alalive/virtualMonery/doLiveReward'
        cls.rdata ={
            "beUserId":728066,
	        "roomId":728066,
	        "presentId":16,
	        "presentCount":6,
	        "presentType":2,
	        "randomCode":"dd22d"
        }
        cls.httpsession = requests.session()
        

    #关闭数据库
    @classmethod
    def tearDownClass(cls):
        cls.db.close()
    
    #初始化数据,在每次用例执行之前调用，作为准备数据1
    #删除mp_bill_record19_04年4月份数据，以及mp_bill_record中相应的数据（避免出现脏数据）
    #包括邀约用户和被邀约用户的所有账单
    def initial_db(self):
        sql1 = 'UPDATE mp_bill_record_19_04 set is_delete=1 \
        WHERE user_id=%s or user_id=%s or common_id=%s or common_id=%s;'\
        % (self.beinviteuser,self.beinviteuser2,self.beinviteuser,self.beinviteuser2)
        sql2 = 'UPDATE mp_bill_record set is_delete=1 \
        WHERE user_id=%s or user_id=%s or common_id=%s or common_id=%s;'\
        % (self.beinviteuser,self.beinviteuser2,self.beinviteuser,self.beinviteuser2)
        sql3 = 'UPDATE mp_user_wallet set bubble_amount=1000000,soap_amount=0 \
        WHERE user_id=%s or user_id=%s;' \
        % (self.inviteuser,self.payuser)
        sql4 ='UPDATE mp_user_wallet set soap_amount=0 \
        WHERE user_id=%s or user_id=%s;'\
        % (self.beinviteuser,self.beinviteuser2)
        sql5 = 'UPDATE mp_live_invite_bill_record set is_delete=1 \
        WHERE actor_id=%s or actor_id=%s;' % (self.beinviteuser,self.beinviteuser2)
        sql6 = 'UPDATE mp_live_invite_order set is_delete=1 \
        WHERE anchor_id=%s or anchor_id=%s;' % (self.beinviteuser,self.beinviteuser2)
        try:
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            self.cursor.execute(sql3)
            self.cursor.execute(sql4)
            self.cursor.execute(sql5)
            self.cursor.execute(sql6)
            self.db.commit()
            return 1000
        except Exception as e:
            print('初始化数据错误',e)
            self.db.rollback()

    #json转化
    def parseJson(self,s):
        try:
            d = json.loads(s)
        except Exception as e:
            print('json转换错误',str(e))
            return None
        return d
    
    #提交邀约订单2条，并且修改接收邀约订单，修改邀约订单数据中的时间，
    def invitebill(self,actorid):
        header = self.header
        header['userId'] = self.inviteuser
        param = self.cmdata
        param['time'] = self.tommowtime
        param['anchorId'] = actorid
        r =self.httpsession.post(self.cmurl,data=json.dumps(param),headers=header) #提交邀约请求
        rd = self.parseJson(r.text)
        if rd['code'] == 1000:
            #返回code码
            return rd['code']
        else:
            print('邀约失败',rd['error'])
            
            
    #获取邀约成功的订单id
    def getorder(self,userid):
        header = self.header
        header['userId'] = userid
        r = self.httpsession.post(self.lcurl,data=json.dumps(self.ldata),headers=header)
        rd = self.parseJson(r.text)
        if rd['code'] == 1000:
            order = rd['data'][0]['orderId']
            return order
        else:
            print('获取邀约订单id失败',rd['code'])

    #处理邀约订单
    def dealorder(self,order,userid):
        header = self.header
        header['userId'] = userid
        adata = self.adata
        adata['orderId'] = order
        r = self.httpsession.post(self.acurl,data=json.dumps(adata),headers=header)
        rd = self.parseJson(r.text)
        if rd['code'] == 1000:
            #返回code码
            return rd['code']
        else:
            print('接收邀约失败',rd['code'])
    
    #修改订单时间
    def changetime(self,order,ctime):
        order,ctime = order,ctime
        sql = 'UPDATE mp_live_invite_order set invite_date="%s" WHERE id=%d' % (ctime,order)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print('修改订单时间失败',e)
    
    #送礼
    def cost(self,userid,presentid,presentcount,presenttype):
        userid,roomid,prensentid,presentcount,presenttype = userid,userid,presentid,presentcount,presenttype
        rdata = self.rdata
        rdata['beUserId'] = userid
        rdata['roomId'] = roomid
        rdata['presentId'] = prensentid
        rdata['presentCount'] = presentcount
        rdata['presentType'] = presenttype
        header = self.header
        header['userId'] = self.payuser
        r = self.httpsession.post(self.rurl,data=json.dumps(rdata),headers=header)
        rd = self.parseJson(r.text)
        if rd['code'] == 1000:
            return rd['code']
        else:
            print('送礼失败',rd['code'])

    #修改mp_live_invite_bill_record里的送礼时间
    def dealbill(self,userid,orderid,ctime):
        userid,orderid,ctime = userid,orderid,ctime
        sql = 'UPDATE mp_live_invite_bill_record \
            set doReward_date= "%s",order_id=%s \
            WHERE is_delete=0 and actor_id=%s' \
            % (ctime,orderid,userid)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1000
        except Exception as e:
            print('修改打赏账单数据失败',e)
    
    #结算账单
    def banlance(self):
        header = {
            'content-type':'application/json; charset=utf-8',
            'Cookie':'JSESSIONID=A2E1E72D2466370B32EDA0CC808B4AF4'
        }
        url = 'https://admin-test.maopp.cn/api/live/invite/dealInviteBill'
        r = self.httpsession.post(url,data='{}',headers=header)
        rd = self.parseJson(r.text)
        if rd['code'] == 1000:
            return rd['code']
        else:
            print('结算失败',rd['code'])


    #有家族，无区域代理，数据准备
    def beforetest01(self):
        code = self.initial_db()  #初始化数据库
        userid = self.beinviteuser
        order2,ctime = 0,0
        if code == 1000:
            code = self.invitebill(userid)  #邀约主播
            if code == 1000:  #邀约成功
                order1 = self.getorder(userid)
                code = self.dealorder(order1,userid)  #处理邀约主播
                if code == 1000:
                    ctime = time.strftime('%Y-%m-%d',time.localtime(time.time()))  #获得今天的时间
                    self.changetime(order1,ctime)
            code = self.invitebill(userid)
            if code == 1000:
                order2 = self.getorder(userid) 
                code = self.dealorder(order2,userid)
                if code == 1000:
                    ctime = time.strftime('%Y-%m-%d',time.localtime(time.time()-60*60*24))
                    self.changetime(order2,ctime)
        code = self.cost(userid,self.prensentid1,self.presentcount1,self.presenttype1)
        if code == 1000:
            code = self.dealbill(userid,order2,ctime)
            if code == 1000:
                code = self.banlance()
                if code == 1000:
                    return code
    

    #有家族，无区域代理，断言账单验证
    def test_01(self):
        code = self.beforetest01()
        self.assertEqual(code,1000,'验证失败')
        self.assertEqual(code,1000,'验证失败')




if __name__ == '__main__':
    unittest.main()
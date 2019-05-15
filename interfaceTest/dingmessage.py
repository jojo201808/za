import requests
import json

def dingmessage():
# 请求的URL，WebHook地址
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=1373ad119e167a1c8c0f0c6b837c2ab17b5638a07dae2fbf2758e118ec08021e"
#构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
        }
#构建请求数据
    message ={

        "msgtype": "text",
        "text": {
            "content": '接口自动化测试执行啦！详情见邮件！'
        },
        "at": {

            "isAtAll": False
        }

    }
#对请求的数据进行json封装
    message_json = json.dumps(message)
#发送请求
    info = requests.post(url=webhook,data=message_json,headers=header)
#打印返回的结果
    print(info.text)

if __name__=="__main__":
    dingmessage()
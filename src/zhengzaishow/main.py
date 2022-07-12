import base64
from collections import namedtuple
from pprint import pprint

import requests
from Crypto.Cipher import AES


class ZhengZaiShow:

    def get(self, url, params=None):
        response = requests.get(url, params=params, headers=self.headers, cookies=self.cookies)
        return self.resolve_response(response)

    @staticmethod
    def resolve_response(response):
        data = response.json()
        if data["success"]:
            return data
        else:
            raise ConnectionError(data)

    def __init__(self):
        self.shows = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://m.zhengzai.tv",
            "Sec-Fetch-Site": "same-site",
        }
        self.cookies = {
            "zztvCity": "%E4%B8%8A%E6%B5%B7",
            "provinceName": "%E4%B8%8A%E6%B5%B7%E5%B8%82",
            "nowCity": "%E4%B8%8A%E6%B5%B7%E5%B8%82",
            "Longitude": "121.406417",
            "Latitude": "31.279987",
        }

    def send_code(self, phone: int):
        """
        GET
        :return:
        """
        uri = "https://adam.zhengzai.tv/adam/send"
        response = self.get(uri, params={"mobile": phone})
        print(response)
        return response

    def login(self, phone: int, code: int):
        """
        POST
        https://adam.zhengzai.tv/adam/login/sms
        :param mobile=15192748090&code=159089
        :return: {
        "code":"0",
        "message":None,
        "data":
        {
        "token":"eyJhbGciOiJIUzI1NiJ9..4N2p3snkvMuG5IFYAIVTA2leEG5EIPzkv4dYOexWwoY",
        "userInfo":{"uid":"1326917","mobile":"151****8090","passwd":None,"nickname":"PONY","state":1,"sex":{"val":"MS00","desc":"保密"},"birthday":None,"area":"上海市 上海城区 黄浦区","signature":"别看了，赶紧冲","avatar":"http://pic.zhengzai.tv/202008/4E/7D/1598671098959_04DD59987152BCF56544D7909C505470.jpg","background":"http://pic.zhengzai.tv/default/background.png","tagMe":None,"createAt":"2020-08-29 11:17:34","updatedAt":"2021-10-08 20:51:38","closedAt":None,"isComplete":1,"rongCloudToken":"GwaCX355L3nKhm68RaduEVkrQdBid64OMQEaKX7YEzo=@zpqb.cn.rongnav.com;zpqb.cn.rongcfg.com","qrCode":"21122348090","stageMarker":11,"province":"山东","city":"青岛","county":None},"userMemberVo":{"memberId":"1","memberNo":"0003329","state":1,"expiryAt":"2023-01-04 23:59:59","createdAt":"2020-10-22 23:35:59","updatedAt":"2022-01-04 14:40:15"},"wechatOpenid":None,"wechatUnionid":None},"success":True}

        eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMzI2OTE3IiwiY19hdCI6IjIwMjAwODI5MTExNzM0IiwibW9iaWxlIjoiMTUxOTI3NDgwOTAiLCJuaWNrbmFtZSI6IlBPTlkiLCJ0eXBlIjoidXNlciIsImV4cCI6MTY2MDIxNTIzNiwiaWF0IjoxNjU3NjIzMjM2fQ.bgj-cqKlXoyfkuSFtfJO6CU3bAy3s3wFv-_ZuiweMHE

        将token写到cookie中

        json
        {"message":"Required String parameter 'mobile' is not present","code":"2","data":None}
        data
        {"message":"Required String parameter 'mobile' is not present","code":"2","data":None}
        params
        {"code":"10004","message":"请输入正确验证码","data":None,"success":false}

        """
        uri = "https://adam.zhengzai.tv/adam/login/sms"
        response = requests.post(uri, params={"mobile": str(phone), "code": code}, headers=self.headers)
        res = response.json()
        print('=' * 10)
        print(res)
        print('=' * 10)
        success = res.get("success")

    def set_cookies(self, res: dict):
        """
        eyJhbGciOiJIUzI1NiJ9..LV7b8Avb2KjDI7dXDy582AB645NHeWH556KI8tKbtAY
        :param token:
        :return:
        """
        token = res.get("data", {}).get("token")
        nickname = res.get("data", {}).get("userInfo", {}).get("nickname")
        uid = res.get("data", {}).get("userInfo", {}).get("uid")
        stage_marker = res.get("data", {}).get("userInfo", {}).get("stageMarker")
        self.cookies["nick_name"] = nickname
        self.cookies["user_info"] = token
        self.cookies["cookie_user_auth"] = token
        self.cookies["userid"] = uid
        self.cookies["stageMarker"] = stage_marker

    def list_show(self, adcode: int):
        """
        GET
        ?adCode=310100&page=1&size=20&days=0&orderBy=timeStart&sort=ASC
        :return:
        {
            "code": "0", "message": None,
            "data": {"total": 0, "is_native": 1, "recommend": 7,
                     "list": [
                         {
                             "mid": 1577, "performancesId": "915819828306862082872056",
                             "title": "「抢你的爱」旋转保龄歌舞团2022巡回大联欢-上海站",
                             "imgPoster": "https://img.zhengzai.tv/other/2022/03/04/6601082daac04465a6a917856435ba12.jpg",
                             "payCountdownMinute": 5,
                             "approvalUrl": "https://img.zhengzai.tv/other/2022/03/04/1a427343ce4544af819afe075f18abe1.png?x-oss-process=image/resize,s_200",
                             "type": 103,
                             "timeStart": "2022-05-07 20:00:00",
                             "timeEnd": "2022-05-07 22:30:00",
                             "stopSellTime": "2022-05-07 22:30:00",
                             "price": "122.22起",
                             "sellTime": "2022-03-07 12:00:00",
                             "sellMemberTime": "2022-03-07 11:55:00",
                             "cityId": 310100, "cityName": "上海",
                             "fieldId": "868",
                             "fieldName": "育音堂音乐公园  ", "longitude": "121.422371", "latitude": "31.219243",
                             "diffDistance": None,
                             "projectId": "0",
                             "roadShowId": "923879484523642884592584",
                             "details": None,
                             "noticeImage": None,
                             "isRecommend": 0, "appStatus": 6, "statusSell": 1, "isMember": 0, "isLackRegister": 1,
                             "isTrueName": 0,
                             "limitCount": 0, "limitCountMember": 1, "isExclusive": 0, "isDiscount": 0, "isAdvance": 0,
                             "sysDamai": 0,
                             "message": "", "notice": "", "isShow": 1, "ticketTimeList": None, "agentName": None,
                             "createdAt": "2022-03-08 13:10:18", "isCanRefund": 0, "isOpenRefundPresent": 0,
                             "refundOpenTime": None,
                             "refundCloseTime": None, "isTransfer": 0, "transferStartTime": None,
                             "transferEndTime": None,
                             "isRefundPoundage": 0, "isRefundVoucher": 0, "isRefundExpress": 0, "isBackPaperTicket": 1,
                             "isRefundExpressNew": 1, "auditStatus": 1, "rejectTxt": "", "merchantId": "1120839",
                             "fieldAuditStatus": 0}
                     ]
                     },
            "success": True
        }
        """
        params = {
            "adCode": adcode,
            "page": 1,
            "size": 20,
            "days": 0,
            "orderBy": "timeStart",
            "sort": "ASC",
        }
        uri = "https://kylin.zhengzai.tv/kylin/performance/localList"
        response = self.get(uri, params=params)
        print('=' * 100)
        pprint(response["data"])
        print('=' * 100)
        self.shows = response["data"]["list"]

    def get_show_space(self, road_show_id: int):
        """
        jip
        :return:
        """
        d = {"code": "0", "message": None, "data": [
            {"mid": 1577, "performancesId": "915819828306862082872056", "title": "「抢你的爱」旋转保龄歌舞团2022巡回大联欢-上海站",
             "imgPoster": "https://img.zhengzai.tv/other/2022/03/04/6601082daac04465a6a917856435ba12.jpg",
             "payCountdownMinute": 5,
             "approvalUrl": "https://img.zhengzai.tv/other/2022/03/04/1a427343ce4544af819afe075f18abe1.png?x-oss-process=image/resize,s_200",
             "type": 103, "timeStart": "2022-05-07 20:00:00", "timeEnd": "2022-05-07 22:30:00",
             "stopSellTime": "2022-05-07 22:30:00", "price": "122.22起", "sellTime": "2022-03-07 12:00:00",
             "sellMemberTime": "2022-03-07 11:55:00", "cityId": 310100, "cityName": "上海", "fieldId": "868",
             "fieldName": "育音堂音乐公园  ", "longitude": "121.422371", "latitude": "31.219243", "diffDistance": None,
             "projectId": "0", "roadShowId": "923879484523642884592584",
             "isRecommend": 0, "appStatus": 6, "statusSell": 1, "isMember": 0, "isLackRegister": 1, "isTrueName": 0,
             "limitCount": 0, "limitCountMember": 1, "isExclusive": 0, "isDiscount": 0, "isAdvance": 0, "sysDamai": 0,
             "message": "", "notice": "", "isShow": 1, "ticketTimeList": [
                {"mid": 1759, "ticketTimesId": "915819828558520328708909", "title": "2022-05-07 00:00", "type": 1,
                 "performanceId": "915819828306862082872056", "timeId": "915819828558520328708909",
                 "useStart": "2022-05-07 00:00:00", "useEnd": "2022-05-07 00:00:00", "ticketList": [
                    {"mid": 3957, "ticketsId": "915819828768235523792821", "timeId": "915819828558520328708909",
                     "title": "预售单人票", "type": 1, "price": 122.22, "priceExpress": 0.00, "memberPrice": 122.22,
                     "discountPrice": 122.22, "describes": "", "describeExpress": "",
                     "describeElectronic": "电子票下单后无法更改为快递票。门票不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。请确认个人信息填写正确，成功购票后无法修改。演出当日可至演出现场凭身份证原件兑换纸质票入场",
                     "timeStart": "2022-03-07 12:00:00", "timeEnd": "2022-05-07 00:00:00",
                     "memberTimeStart": "2022-03-07 11:55:00", "timeEndExpress": "2030-01-01 12:00:00",
                     "useStart": "2022-05-07 00:00:00", "useEnd": "2022-05-07 00:00:00", "saleRemindMinute": 60,
                     "isStudent": 0, "isElectronic": 1, "isExpress": 0, "sysDamai": 0, "counts": 1, "status": 6,
                     "statusExchange": 7, "isLackRegister": 1, "expressType": 0, "isTrueName": 0, "limitCount": 0,
                     "limitCountMember": 1, "isExclusive": 0, "isMember": 1, "isMemberStatus": None, "isAgent": 0,
                     "isShowCode": 1, "qrCodeShowTime": "2022-03-04 15:44:51", "advanceMinuteMember": 5,
                     "totalGeneral": 150, "totalExchange": 0},
                    {"mid": 3958, "ticketsId": "915819829355438088315113", "timeId": "915819828558520328708909",
                     "title": "预售双人票", "type": 1, "price": 222.22, "priceExpress": 0.00, "memberPrice": 222.22,
                     "discountPrice": 222.22, "describes": "", "describeExpress": "",
                     "describeElectronic": "电子票下单后无法更改为快递票。门票不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。请确认个人信息填写正确，成功购票后无法修改。演出当日可至演出现场凭身份证原件兑换纸质票入场",
                     "timeStart": "2022-03-07 12:00:00", "timeEnd": "2022-05-07 00:00:00",
                     "memberTimeStart": "2022-03-07 11:55:00", "timeEndExpress": "2030-01-01 12:00:00",
                     "useStart": "2022-05-07 00:00:00", "useEnd": "2022-05-07 00:00:00", "saleRemindMinute": 60,
                     "isStudent": 0, "isElectronic": 1, "isExpress": 0, "sysDamai": 0, "counts": 1, "status": 6,
                     "statusExchange": 7, "isLackRegister": 0, "expressType": 0, "isTrueName": 0, "limitCount": 0,
                     "limitCountMember": 1, "isExclusive": 0, "isMember": 1, "isMemberStatus": None, "isAgent": 0,
                     "isShowCode": 1, "qrCodeShowTime": "2022-03-04 15:44:51", "advanceMinuteMember": 5,
                     "totalGeneral": 50, "totalExchange": 0},
                    {"mid": 3959, "ticketsId": "915819829061836801014523", "timeId": "915819828558520328708909",
                     "title": "现场票", "type": 1, "price": 150.00, "priceExpress": 0.00, "memberPrice": 150.00,
                     "discountPrice": 150.00, "describes": "", "describeExpress": "",
                     "describeElectronic": "电子票下单后无法更改为快递票。门票不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。请确认个人信息填写正确，成功购票后无法修改。演出当日可至演出现场凭身份证原件兑换纸质票入场",
                     "timeStart": "2022-03-07 12:00:00", "timeEnd": "2022-05-07 22:30:00",
                     "memberTimeStart": "2022-03-07 11:55:00", "timeEndExpress": "2030-01-01 12:00:00",
                     "useStart": "2022-05-07 00:00:00", "useEnd": "2022-05-07 00:00:00", "saleRemindMinute": 60,
                     "isStudent": 0, "isElectronic": 1, "isExpress": 0, "sysDamai": 0, "counts": 1, "status": 6,
                     "statusExchange": 7, "isLackRegister": 1, "expressType": 0, "isTrueName": 0, "limitCount": 0,
                     "limitCountMember": 1, "isExclusive": 0, "isMember": 1, "isMemberStatus": None, "isAgent": 0,
                     "isShowCode": 1, "qrCodeShowTime": "2022-03-04 15:44:51", "advanceMinuteMember": 5,
                     "totalGeneral": 50, "totalExchange": 0}]}], "agentName": None, "createdAt": "2022-03-08 13:10:18",
             "isCanRefund": 0, "isOpenRefundPresent": 0, "refundOpenTime": None, "refundCloseTime": None,
             "isTransfer": 0, "transferStartTime": None, "transferEndTime": None, "isRefundPoundage": 0,
             "isRefundVoucher": 0, "isRefundExpress": 0, "isBackPaperTicket": 1, "isRefundExpressNew": 1,
             "auditStatus": 1, "rejectTxt": "", "merchantId": "1120839", "fieldAuditStatus": 0},
        ], "success": True}
        uri = f"https://kylin.zhengzai.tv/kylin/performance/roadList/{road_show_id}"
        response = self.get(uri)

        #  获取站点
        spaces = namedtuple("city", [])
        for data in spaces:
            pass

        # 获取票种

    def get_show_detail(self, preformances_id):
        """
        根据演出的ID获取演出票类型及其价格
        :param preformances_id:
        :return:
        {
    "code": "0",
    "message": null,
    "data": {
        "ticketTimesList": [
            {
                "mid": 2100,
                "ticketTimesId": "1368976800792535041612431",
                "title": "2022-07-24 00:00",
                "type": 1,
                "performanceId": "1368976800498933765198948",
                "timeId": "1368976800792535041612431",
                "useStart": "2022-07-24 00:00:00",
                "useEnd": "2022-07-24 00:00:00",
                "ticketList": [
                    {
                        "mid": 4719,
                        "ticketsId": "1368976801002250246812316",
                        "timeId": "1368976800792535041612431",
                        "title": "预售票",
                        "type": 1,
                        "price": 120.00,
                        "priceExpress": 0.00,
                        "memberPrice": 120.00,
                        "discountPrice": 120.00,
                        "describes": "",
                        "describeExpress": "",
                        "describeElectronic": "身份证电子票下单后不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。电子票需身份证实名购票，请务必准确填写信息，下单后无法更改。演出当日购票人须持本人身份证原件入场。",
                        "timeStart": "2022-07-07 19:00:00",
                        "timeEnd": "2022-07-24 00:00:00",
                        "memberTimeStart": "2022-07-07 18:55:00",
                        "timeEndExpress": "2022-07-07 18:28:40",
                        "useStart": "2022-07-24 00:00:00",
                        "useEnd": "2022-07-24 00:00:00",
                        "saleRemindMinute": 60,
                        "isStudent": 0,
                        "isElectronic": 1,
                        "isExpress": 0,
                        "sysDamai": 0,
                        "counts": 1,
                        "status": 6,
                        "statusExchange": 7,
                        "isLackRegister": 0,
                        "expressType": 0,
                        "isTrueName": 1,
                        "limitCount": 0,
                        "limitCountMember": 1,
                        "isExclusive": 0,
                        "isMember": 1,
                        "isMemberStatus": 1,
                        "isAgent": 0,
                        "isShowCode": 1,
                        "qrCodeShowTime": "2022-07-24 18:00:00",
                        "advanceMinuteMember": 5,
                        "totalGeneral": 100,
                        "totalExchange": 0
                    },
                    {
                        "mid": 4720,
                        "ticketsId": "1368976801295851523466360",
                        "timeId": "1368976800792535041612431",
                        "title": "现场票",
                        "type": 1,
                        "price": 150.00,
                        "priceExpress": 0.00,
                        "memberPrice": 150.00,
                        "discountPrice": 150.00,
                        "describes": "",
                        "describeExpress": "",
                        "describeElectronic": "身份证电子票下单后不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。电子票需身份证实名购票，请务必准确填写信息，下单后无法更改。演出当日购票人须持本人身份证原件入场。",
                        "timeStart": "2022-07-24 00:00:00",
                        "timeEnd": "2022-07-17 21:30:00",
                        "memberTimeStart": "2022-07-23 23:55:00",
                        "timeEndExpress": "2022-07-07 18:28:40",
                        "useStart": "2022-07-24 00:00:00",
                        "useEnd": "2022-07-24 00:00:00",
                        "saleRemindMinute": 60,
                        "isStudent": 0,
                        "isElectronic": 1,
                        "isExpress": 0,
                        "sysDamai": 0,
                        "counts": 1,
                        "status": 9,
                        "statusExchange": 7,
                        "isLackRegister": 0,
                        "expressType": 0,
                        "isTrueName": 1,
                        "limitCount": 0,
                        "limitCountMember": 1,
                        "isExclusive": 0,
                        "isMember": 1,
                        "isMemberStatus": 0,
                        "isAgent": 0,
                        "isShowCode": 1,
                        "qrCodeShowTime": "2022-07-24 18:00:00",
                        "advanceMinuteMember": 5,
                        "totalGeneral": 50,
                        "totalExchange": 0
                    }
                ]
            }
        ],
        "performancesInfo": {
            "city_name": "杭州市",
            "title": "2022黑撒乐队“孩子们的理想”巡演 杭州站",
            "appStatus": 6,
            "field_name": "酒球会  "
        }
    },
    "success": true
}
        """
        """
        Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMzI2OTE3IiwiY19hdCI6IjIwMjAwODI5MTExNzM0IiwibW9iaWxlIjoiMTUxOTI3NDgwOTAiLCJuaWNrbmFtZSI6IlBPTlkiLCJ0eXBlIjoidXNlciIsImV4cCI6MTY2MDIyMDIzMywiaWF0IjoxNjU3NjI4MjMzfQ.1bBjCflIfw6dCo07sXNfTIMwJA2PqQROA306cn835g8
        """
        uri = f"https://kylin.zhengzai.tv/kylin/performance/partner/{preformances_id}"
        params = {
            "isAgent": 0
        }
        response = self.get(uri, params=params)
        print('=' * 100)
        pprint(response["data"])

    def pay(self):
        """
        https://kylin.zhengzai.tv/kylin/performance/payDetail?performancesId=915819828306862082872056&ticketsId=915819828768235523792821
        :return:
        """
        pass

    def ase_encode(self, data: str):
        """
        Encode the data in the object to a string.

        Returns:
            str: The encoded data.
        """
        # data = '{"number":1,"ticketId":"915819828768235523792821","isElectronic":1,"isExpress":0,"deviceFrom":"wap","actual":122.22,"performanceId":"915819828306862082872056","timeId":"915819828558520328708909","returnUrl":"https://m.zhengzai.tv/pay/status?order_type=ticket&order_id=","showUrl":"https://m.zhengzai.tv/pay/status?order_type=ticket&order_id=","expressType":0,"agentId":0,"payType":"alipay"}'
        key = base64.b64decode("XjjkaLnlzAFbR399IP4kdQ==")

        def add_to_16(text):
            while len(text) % 16 != 0:
                text += '\0'
            return text

        def encrypt(data, password):
            bs = AES.block_size
            pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
            cipher = AES.new(password)
            data = cipher.encrypt(pad(data))
            return data

        password = add_to_16(key)
        encrypt_data = encrypt(data, password)
        encrypt_data = base64.b64encode(encrypt_data)
        return encrypt_data

    def encode_sign(self):
        """
        t:
            actual: 122.22
            agentId: 0
            deviceFrom: "wap"
            expressType: 0
            isElectronic: 1
            isExpress: 0
            number: 1
            payType: "alipay"
            performanceId: "915819828306862082872056"
            returnUrl: "https://m.zhengzai.tv/pay/status?order_type=ticket&order_id="
            showUrl: "https://m.zhengzai.tv/pay/status?order_type=ticket&order_id="
            ticketId: "915819828768235523792821"
            timeId: "915819828558520328708909"
        e: {"number":1,"ticketId":"915819828768235523792821","isElectronic":1,"isExpress":0,"deviceFrom":"wap","actual":122.22,"performanceId":"915819828306862082872056","timeId":"915819828558520328708909","returnUrl":"https://m.zhengzai.tv/pay/status?order_type=ticket&order_id=","showUrl":"https://m.zhengzai.tv/pay/status?order_type=ticket&order_id=","expressType":0,"agentId":0,"payType":"alipay"}
        i: 1647776380985
        n:
         HGGFm1DHHYnRZHgvB25eSHcpZKSQCQNai0CY6GWxmtG72e0WE0yZBX9DsluZ4OYYXxEhZLR5qOkNHz/KnrLmBmRMvZqdtPZs5eEyRuwLviJwvWosyNTQ8DWreSeFd6H6QMLvN7BwoY50oeKHrj8rqJex5m65mp0QbNoibV8pxtAlTgHzPnAh3M3c6VjfX+8ofz47eSn85vhNiYKhF9Cc8tAcdWIdHa7VBKvy38A1yX0UELdof0hchnowjwsFu5wr67HKt4f/q31AaoT+CG/H+OuW8mJxQZKqbDeoVQerml70xyGeDb/uqiREKcak20eo8E00cDZxK524lPjoptsUB13B5Q7/f7Jf78ZoVnKOVKfzoB9RChMrsGpZu46NI2+rdKkc/ZSJz2NrxT4dsmf57YhBvoElvM5zTMSvyrQxjh65RDWufD4ozxeSNuNHYG1T8wpkB8a7oqjpjiRRwdojDmkSOZxGdz+zQSSE+ULz7q1Uf4hOxhaTzgdmC8iWOGL8JBUg8sghrcmRWxSldE9RxA==
        function(t) {
            var e = p()(t)
              , n = m.a.AES.encrypt(e, m.a.enc.Base64.parse("XjjkaLnlzAFbR399IP4kdQ=="), {
                mode: m.a.mode.ECB,
                padding: m.a.pad.Pkcs7,
                length: 128
            }).toString()
              , i = (new Date).getTime();
            return {
                sign: m.a.SHA1(n + i + "QGZUanpSaSy9DEPQFVULJQ==").toString(),
                encryptedData: n,
                timestamp: i
            }
        }
        :return:
        """

        pass

    def order(self):
        """
        https://order.zhengzai.tv/order/order/pre
        {"sign":"34fbce6df0c152cee7fd78853550c119f78c43d1",
        "encryptedData":"HGGFm1DHHYnRZHgvB25eSHcpZKSQCQNai0CY6GWxmtG72e0WE0yZBX9DsluZ4OYYXxEhZLR5qOkNHz/KnrLmBmRMvZqdtPZs5eEyRuwLviJwvWosyNTQ8DWreSeFd6H6QMLvN7BwoY50oeKHrj8rqJex5m65mp0QbNoibV8pxtAlTgHzPnAh3M3c6VjfX+8ofz47eSn85vhNiYKhF9Cc8tAcdWIdHa7VBKvy38A1yX0UELdof0hchnowjwsFu5wr67HKt4f/q31AaoT+CG/H+OuW8mJxQZKqbDeoVQerml70xyGeDb/uqiREKcak20eo8E00cDZxK524lPjoptsUB13B5Q7/f7Jf78ZoVnKOVKfzoB9RChMrsGpZu46NI2+rdKkc/ZSJz2NrxT4dsmf57YhBvoElvM5zTMSvyrQxjh65RDWufD4ozxeSNuNHYG1T8wpkB8a7oqjpjiRRwdojDmkSOZxGdz+zQSSE+ULz7q1Uf4hOxhaTzgdmC8iWOGL8JBUg8sghrcmRWxSldE9RxA==",
        "timestamp":1647166991860}
        :return:
        {"code":"0","message":null,"data":{"code":"PAY202203131823155610286101","orderCode":"94860877108707328191906930","status":null,"orderId":"948608771087073281913006","payType":"alipay","showUrl":"https://m.zhengzai.tv/pay/status?order_type=ticket&order_id=948608771087073281913006","returnUrl":"https://m.zhengzai.tv/pay/status?order_type=ticket&order_id=948608771087073281913006","price":122.22,"payData":{"appId":null,"nonceStr":null,"timeStamp":null,"partnerId":null,"prepayId":null,"sign":null,"mwebUrl":null,"paySign":null,"signType":null,"redirectUrl":"https://openapi.alipay.com/gateway.do?alipay_sdk=alipay-sdk-java-dynamicVersionNo&app_id=2019082866535131&biz_content=%7B%22body%22%3A%22%E6%AD%A3%E5%9C%A8%E7%8E%B0%E5%9C%BA%22%2C%22out_trade_no%22%3A%22PAY202203131823155610286101%22%2C%22product_code%22%3A%22QUICK_WAP_PAY%22%2C%22subject%22%3A%22%E6%AD%A3%E5%9C%A8%E7%8E%B0%E5%9C%BA%22%2C%22timeout_express%22%3A%225m%22%2C%22total_amount%22%3A%22122.22%22%7D&charset=utf-8&format=json&method=alipay.trade.wap.pay&notify_url=https%3A%2F%2Fdragon.zhengzai.tv%2Fdragon%2Fnotify%2Falipay%2Fwap&sign=CQV9aVHWsVbOlMTwwK%2F3ZktSjvpKnv75ods%2FGBO611fWp1vMOJfDfjiRXbezQglQwNT8ynrp2I9Sm1f1q2BCy4lbEf8231L86uZBxI5kGJ1BCnAwJcr6OFnmYNi8j4iPILejoPmnu7sblYYKgOFL42i8rn404N1Igws81ka71xgFHBynJav6L7fwLzSknhGXdlyqAiWAx6JJYEZ4uJiobYbGpc1YPj8oKkPhwxY4n7H4INW5qVx6%2BBWzOZyXtQGOSMdW5eIxsa%2F36k3JDBXIVwxgOBdnbgtwjShCYAZ5UAPd%2F7OKel6mvwTYzm2b0NTOYZT5h34yxb6MqgFl8tVl8A%3D%3D&sign_type=RSA2&timestamp=2022-03-13+18%3A23%3A15&version=1.0","orderStr":null,"orderId":"","orderToken":"","package":null}},"success":true}
        """


if __name__ == '__main__':
    zhengzai = ZhengZaiShow()
    # zhengzai.send_code(15192748090)
    # zhengzai.login(15192748090, 190194)
    zhengzai.list_show(330100)

    pass

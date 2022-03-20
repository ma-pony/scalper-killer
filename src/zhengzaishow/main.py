import requests
from collections import namedtuple
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
        self.show_list = []
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
        self.show_list = response["data"]["list"]

    def get_show_space(self, road_show_id: int):
        """

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
             "details": "<p style=\"text-align: center;\"><strong style=\"color: rgb(255, 76, 65);\"><em>旋转保龄歌舞团</em></strong></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 76, 65);\"><em>「抢你的爱」</em></strong></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 76, 65);\"><em>2022巡回大联欢</em></strong></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">4月8日&nbsp;&nbsp;合肥&nbsp;ON THE WAY</p><p style=\"text-align: center;\">4月9日&nbsp;苏州&nbsp;&nbsp;MAOLivehouse苏州</p><p style=\"text-align: center;\">4月10日&nbsp;&nbsp;宁波&nbsp;灯塔音乐现场（集盒）</p><p style=\"text-align: center;\">5月6日&nbsp;&nbsp;杭州&nbsp;MAOLivehouse杭州</p><p style=\"text-align: center;\">5月7日&nbsp;上海&nbsp;&nbsp;育音堂音乐公园</p><p style=\"text-align: center;\">5月8日&nbsp;南京&nbsp;&nbsp;欧拉艺术空间</p><p style=\"text-align: center;\">6月10日&nbsp;青岛&nbsp;&nbsp;SO.DOWNTOWN</p><p style=\"text-align: center;\">6月11日&nbsp;&nbsp;济南&nbsp;雀跃之地</p><p style=\"text-align: center;\">6月12日&nbsp;&nbsp;太原&nbsp;&nbsp;TheBoo</p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 169, 0);\"><em>历时12个月</em></strong></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 169, 0);\"><em>覆盖22站&nbsp;</em></strong></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 169, 0);\"><em>阵容再升级</em></strong></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\"><img src=\"//:0\"><img src=\"//:0\"><img src=\"https://img.zhengzai.tv/other/2022/03/06/7d48581d403647349353e23298867fee.jpg\"></p><p style=\"text-align: right;\"><span style=\"color: rgb(136, 136, 136);\">插画：擦主席  </span></p><p style=\"text-align: right;\"><span style=\"color: rgb(136, 136, 136);\">海报设计：MVM design label _</span></p><p><br></p><p><br></p><p>去年的这个时间，旋转保龄带来了他们第四张录音室专辑《强尼的爱》。起源于50年代的Rockabilly仍是旋转保龄的标配，但已不再是旋转保龄的全部：从Psychobilly，到热烈欢脱的Ska；从让人无法自已开始扭脚摇摆的Swing到轻盈愉悦的乡村摇滚、蓝草音乐……几乎所有根源摇滚乐的分支流派都可以在这张专辑里寻到踪迹。</p><p><br></p><p><img src=\"https://img.zhengzai.tv/other/2022/03/06/c248d0645ed34629bc63087d39782eb4.jpeg\"></p><p><br></p><p><br></p><p>完成阵容升级的旋转保龄<strong>今时不同往日</strong>：在新专辑的录制和此后的现场中，旋转保龄加入了包含一支小号、一支长号以及两把萨克斯的豪华管乐组。<strong>几位铜管乐手的加入，让他们的音乐呈现出更加丰满、立体的层次感</strong>，每一首出自不同经历与表达维度的作品，都得以在截然不同的编配方式中，各自呈现出分明的样貌。</p><p><img src=\"//:0\"></p><p><img src=\"//:0\"><img src=\"https://img.zhengzai.tv/other/2022/03/06/153b8c4054e04923ac42c4c43a30dbfe.jpeg\"></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">本次「抢你的爱」2022巡回大联欢，旋转保龄邀请前复古摇滚地下传奇「DH &amp; CHINESE HELLCATS」的主唱王卉加入巡演，继加入管乐组之后，旋转保龄正式升级为「双主唱」阵容！</p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">\uD83C\uDF89</p><p style=\"text-align: center;\">岂止是梦幻联动</p><p style=\"text-align: center;\">这简直是双厨狂喜</p><p style=\"text-align: center;\"><img src=\"\"></p><p style=\"text-align: center;\"><img src=\"//:0\"><img src=\"\"><img src=\"\"><img src=\"https://img.zhengzai.tv/other/2022/03/06/1ef50cdb7f3b4c12af4daa74dd2015c0.png\"></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">空前绝后的强大阵容，必将带来中国复古摇滚的最强现场体验！耗时12个月、覆盖全国22个城市......「抢你的爱」2022巡回大联欢，注定成为一场中国复古文化爱好者的圆梦之旅！</p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">我的❤️</p><p style=\"text-align: center;\">从来不会招手即停</p><p style=\"text-align: center;\">你的❤️</p><p style=\"text-align: center;\">一定要亲手去抢</p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\"><strong>复古爱人们</strong></p><p style=\"text-align: center;\"><strong>\uD83D\uDC4A</strong></p><p style=\"text-align: center;\"><strong>现场见 </strong></p><p style=\"text-align: center;\"><br></p>",
             "noticeImage": "[{\"mid\":1,\"buyNoticeId\":\"1\",\"title\":\"门票不退不换\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c45722882a13.png\",\"message\":\"门票为有价证券，并非商品，一经售出不予退换。因“不可抗力”导致的演出取消或延期除外。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-01-29T13:51:42\",\"updatedAt\":\"2019-01-29T13:51:42\"},{\"mid\":2,\"buyNoticeId\":\"2\",\"title\":\"仅设站席\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c456e93db0b9.png\",\"message\":\"本场演出不设座位，均为站席观演。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-01-29T13:51:42\",\"updatedAt\":\"2019-01-29T13:51:42\"},{\"mid\":3,\"buyNoticeId\":\"3\",\"title\":\"禁止个人票务买卖\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c456e5c27644.png\",\"message\":\"为防止不法分子利用票务转让诈骗钱款，建议广大乐迷不要进行个人间票务买卖，不要轻易相信来源不明的转票，以免自身利益受到侵害。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-01-29T13:51:42\",\"updatedAt\":\"2019-01-29T13:51:42\"},{\"mid\":6,\"buyNoticeId\":\"6\",\"title\":\"电子票\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c456d9482fb9.png\",\"message\":\"凭订单二维码或手机号兑票入场，二维码或手机号请勿泄露，以免影响入场。个人原因导致的信息泄露，主办方/平台方不承担任何责任。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-01-29T13:51:42\",\"updatedAt\":\"2019-01-29T13:51:42\"},{\"mid\":9,\"buyNoticeId\":\"9\",\"title\":\"购买官方门票\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/06/17/5d0764a613742.png\",\"message\":\"请通过官方平台【正在现场】购买门票。通过个人转让购买的门票，若遇到假票、一票多卖等情况，导致的损失，主办方/平台方不承担任何责任。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-06-17T18:06:06\",\"updatedAt\":\"2019-06-17T18:06:06\"},{\"mid\":11,\"buyNoticeId\":\"11\",\"title\":\"现场票\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/06/17/5d07647eaa55f.png\",\"message\":\"每场现场票数量由场地方决定，具体请到现场询问。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-06-17T18:06:06\",\"updatedAt\":\"2019-06-17T18:06:06\"},{\"mid\":15,\"buyNoticeId\":\"15\",\"title\":\"门票不退不换\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c45722882a13.png\",\"message\":\"门票为有价证券，并非商品，不适用无理由退换。因“不可抗力”导致的演出取消或延期除外。\",\"status\":1,\"sort\":0,\"createdAt\":\"2021-10-11T11:31:58\",\"updatedAt\":\"2021-10-11T11:32:00\"}]",
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

    def pay(self):
        """
        https://kylin.zhengzai.tv/kylin/performance/payDetail?performancesId=915819828306862082872056&ticketsId=915819828768235523792821
        :return:
        {"code":"0","message":null,"data":{"performanceInfo":{"mid":1577,"performancesId":"915819828306862082872056","title":"「抢你的爱」旋转保龄歌舞团2022巡回大联欢-上海站","imgPoster":"https://img.zhengzai.tv/other/2022/03/04/6601082daac04465a6a917856435ba12.jpg","payCountdownMinute":5,"approvalUrl":"https://img.zhengzai.tv/other/2022/03/04/1a427343ce4544af819afe075f18abe1.png?x-oss-process=image/resize,s_200","type":103,"timeStart":"2022-05-07 20:00:00","timeEnd":"2022-05-07 22:30:00","stopSellTime":"2022-05-07 22:30:00","price":"122.22起","sellTime":"2022-03-07 12:00:00","sellMemberTime":"2022-03-07 11:55:00","cityId":310100,"cityName":"上海","fieldId":"868","fieldName":"育音堂音乐公园  ","longitude":"121.422371","latitude":"31.219243","diffDistance":null,"projectId":"0","roadShowId":"923879484523642884592584","details":"<p style=\"text-align: center;\"><strong style=\"color: rgb(255, 76, 65);\"><em>旋转保龄歌舞团</em></strong></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 76, 65);\"><em>「抢你的爱」</em></strong></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 76, 65);\"><em>2022巡回大联欢</em></strong></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">4月8日&nbsp;&nbsp;合肥&nbsp;ON THE WAY</p><p style=\"text-align: center;\">4月9日&nbsp;苏州&nbsp;&nbsp;MAOLivehouse苏州</p><p style=\"text-align: center;\">4月10日&nbsp;&nbsp;宁波&nbsp;灯塔音乐现场（集盒）</p><p style=\"text-align: center;\">5月6日&nbsp;&nbsp;杭州&nbsp;MAOLivehouse杭州</p><p style=\"text-align: center;\">5月7日&nbsp;上海&nbsp;&nbsp;育音堂音乐公园</p><p style=\"text-align: center;\">5月8日&nbsp;南京&nbsp;&nbsp;欧拉艺术空间</p><p style=\"text-align: center;\">6月10日&nbsp;青岛&nbsp;&nbsp;SO.DOWNTOWN</p><p style=\"text-align: center;\">6月11日&nbsp;&nbsp;济南&nbsp;雀跃之地</p><p style=\"text-align: center;\">6月12日&nbsp;&nbsp;太原&nbsp;&nbsp;TheBoo</p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 169, 0);\"><em>历时12个月</em></strong></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 169, 0);\"><em>覆盖22站&nbsp;</em></strong></p><p style=\"text-align: center;\"><strong style=\"color: rgb(255, 169, 0);\"><em>阵容再升级</em></strong></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\"><img src=\"//:0\"><img src=\"//:0\"><img src=\"https://img.zhengzai.tv/other/2022/03/06/7d48581d403647349353e23298867fee.jpg\"></p><p style=\"text-align: right;\"><span style=\"color: rgb(136, 136, 136);\">插画：擦主席  </span></p><p style=\"text-align: right;\"><span style=\"color: rgb(136, 136, 136);\">海报设计：MVM design label _</span></p><p><br></p><p><br></p><p>去年的这个时间，旋转保龄带来了他们第四张录音室专辑《强尼的爱》。起源于50年代的Rockabilly仍是旋转保龄的标配，但已不再是旋转保龄的全部：从Psychobilly，到热烈欢脱的Ska；从让人无法自已开始扭脚摇摆的Swing到轻盈愉悦的乡村摇滚、蓝草音乐……几乎所有根源摇滚乐的分支流派都可以在这张专辑里寻到踪迹。</p><p><br></p><p><img src=\"https://img.zhengzai.tv/other/2022/03/06/c248d0645ed34629bc63087d39782eb4.jpeg\"></p><p><br></p><p><br></p><p>完成阵容升级的旋转保龄<strong>今时不同往日</strong>：在新专辑的录制和此后的现场中，旋转保龄加入了包含一支小号、一支长号以及两把萨克斯的豪华管乐组。<strong>几位铜管乐手的加入，让他们的音乐呈现出更加丰满、立体的层次感</strong>，每一首出自不同经历与表达维度的作品，都得以在截然不同的编配方式中，各自呈现出分明的样貌。</p><p><img src=\"//:0\"></p><p><img src=\"//:0\"><img src=\"https://img.zhengzai.tv/other/2022/03/06/153b8c4054e04923ac42c4c43a30dbfe.jpeg\"></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">本次「抢你的爱」2022巡回大联欢，旋转保龄邀请前复古摇滚地下传奇「DH &amp; CHINESE HELLCATS」的主唱王卉加入巡演，继加入管乐组之后，旋转保龄正式升级为「双主唱」阵容！</p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">\uD83C\uDF89</p><p style=\"text-align: center;\">岂止是梦幻联动</p><p style=\"text-align: center;\">这简直是双厨狂喜</p><p style=\"text-align: center;\"><img src=\"\"></p><p style=\"text-align: center;\"><img src=\"//:0\"><img src=\"\"><img src=\"\"><img src=\"https://img.zhengzai.tv/other/2022/03/06/1ef50cdb7f3b4c12af4daa74dd2015c0.png\"></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">空前绝后的强大阵容，必将带来中国复古摇滚的最强现场体验！耗时12个月、覆盖全国22个城市......「抢你的爱」2022巡回大联欢，注定成为一场中国复古文化爱好者的圆梦之旅！</p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\">我的❤️</p><p style=\"text-align: center;\">从来不会招手即停</p><p style=\"text-align: center;\">你的❤️</p><p style=\"text-align: center;\">一定要亲手去抢</p><p style=\"text-align: center;\"><br></p><p style=\"text-align: center;\"><strong>复古爱人们</strong></p><p style=\"text-align: center;\"><strong>\uD83D\uDC4A</strong></p><p style=\"text-align: center;\"><strong>现场见 </strong></p><p style=\"text-align: center;\"><br></p>","noticeImage":"[{\"mid\":1,\"buyNoticeId\":\"1\",\"title\":\"门票不退不换\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c45722882a13.png\",\"message\":\"门票为有价证券，并非商品，一经售出不予退换。因“不可抗力”导致的演出取消或延期除外。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-01-29T13:51:42\",\"updatedAt\":\"2019-01-29T13:51:42\"},{\"mid\":2,\"buyNoticeId\":\"2\",\"title\":\"仅设站席\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c456e93db0b9.png\",\"message\":\"本场演出不设座位，均为站席观演。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-01-29T13:51:42\",\"updatedAt\":\"2019-01-29T13:51:42\"},{\"mid\":3,\"buyNoticeId\":\"3\",\"title\":\"禁止个人票务买卖\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c456e5c27644.png\",\"message\":\"为防止不法分子利用票务转让诈骗钱款，建议广大乐迷不要进行个人间票务买卖，不要轻易相信来源不明的转票，以免自身利益受到侵害。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-01-29T13:51:42\",\"updatedAt\":\"2019-01-29T13:51:42\"},{\"mid\":6,\"buyNoticeId\":\"6\",\"title\":\"电子票\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c456d9482fb9.png\",\"message\":\"凭订单二维码或手机号兑票入场，二维码或手机号请勿泄露，以免影响入场。个人原因导致的信息泄露，主办方/平台方不承担任何责任。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-01-29T13:51:42\",\"updatedAt\":\"2019-01-29T13:51:42\"},{\"mid\":9,\"buyNoticeId\":\"9\",\"title\":\"购买官方门票\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/06/17/5d0764a613742.png\",\"message\":\"请通过官方平台【正在现场】购买门票。通过个人转让购买的门票，若遇到假票、一票多卖等情况，导致的损失，主办方/平台方不承担任何责任。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-06-17T18:06:06\",\"updatedAt\":\"2019-06-17T18:06:06\"},{\"mid\":11,\"buyNoticeId\":\"11\",\"title\":\"现场票\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/06/17/5d07647eaa55f.png\",\"message\":\"每场现场票数量由场地方决定，具体请到现场询问。\",\"status\":1,\"sort\":0,\"createdAt\":\"2019-06-17T18:06:06\",\"updatedAt\":\"2019-06-17T18:06:06\"},{\"mid\":15,\"buyNoticeId\":\"15\",\"title\":\"门票不退不换\",\"imgUrl\":\"http://img-zhengzai-tv.oss-cn-hangzhou.aliyuncs.com/partner/2019/01/21/5c45722882a13.png\",\"message\":\"门票为有价证券，并非商品，不适用无理由退换。因“不可抗力”导致的演出取消或延期除外。\",\"status\":1,\"sort\":0,\"createdAt\":\"2021-10-11T11:31:58\",\"updatedAt\":\"2021-10-11T11:32:00\"}]","isRecommend":0,"appStatus":6,"statusSell":1,"isMember":0,"isLackRegister":1,"isTrueName":0,"limitCount":0,"limitCountMember":1,"isExclusive":0,"isDiscount":0,"isAdvance":0,"sysDamai":0,"message":"购买","notice":"","isShow":1,"ticketTimeList":[{"mid":1759,"ticketTimesId":"915819828558520328708909","title":"2022-05-07 00:00","type":1,"performanceId":"915819828306862082872056","timeId":"915819828558520328708909","useStart":"2022-05-07 00:00:00","useEnd":"2022-05-07 00:00:00","ticketList":[{"mid":3957,"ticketsId":"915819828768235523792821","timeId":"915819828558520328708909","title":"预售单人票","type":1,"price":122.22,"priceExpress":0.00,"memberPrice":122.22,"discountPrice":122.22,"describes":"","describeExpress":"","describeElectronic":"电子票下单后无法更改为快递票。门票不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。请确认个人信息填写正确，成功购票后无法修改。演出当日可至演出现场凭身份证原件兑换纸质票入场","timeStart":"2022-03-07 12:00:00","timeEnd":"2022-05-07 00:00:00","memberTimeStart":"2022-03-07 11:55:00","timeEndExpress":"2030-01-01 12:00:00","useStart":"2022-05-07 00:00:00","useEnd":"2022-05-07 00:00:00","saleRemindMinute":60,"isStudent":0,"isElectronic":1,"isExpress":0,"sysDamai":0,"counts":1,"status":6,"statusExchange":7,"isLackRegister":1,"expressType":0,"isTrueName":0,"limitCount":0,"limitCountMember":1,"isExclusive":0,"isMember":1,"isMemberStatus":1,"isAgent":0,"isShowCode":1,"qrCodeShowTime":"2022-03-04 15:44:51","advanceMinuteMember":5,"totalGeneral":150,"totalExchange":0},{"mid":3958,"ticketsId":"915819829355438088315113","timeId":"915819828558520328708909","title":"预售双人票","type":1,"price":222.22,"priceExpress":0.00,"memberPrice":222.22,"discountPrice":222.22,"describes":"","describeExpress":"","describeElectronic":"电子票下单后无法更改为快递票。门票不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。请确认个人信息填写正确，成功购票后无法修改。演出当日可至演出现场凭身份证原件兑换纸质票入场","timeStart":"2022-03-07 12:00:00","timeEnd":"2022-05-07 00:00:00","memberTimeStart":"2022-03-07 11:55:00","timeEndExpress":"2030-01-01 12:00:00","useStart":"2022-05-07 00:00:00","useEnd":"2022-05-07 00:00:00","saleRemindMinute":60,"isStudent":0,"isElectronic":1,"isExpress":0,"sysDamai":0,"counts":1,"status":6,"statusExchange":7,"isLackRegister":0,"expressType":0,"isTrueName":0,"limitCount":0,"limitCountMember":1,"isExclusive":0,"isMember":1,"isMemberStatus":1,"isAgent":0,"isShowCode":1,"qrCodeShowTime":"2022-03-04 15:44:51","advanceMinuteMember":5,"totalGeneral":50,"totalExchange":0},{"mid":3959,"ticketsId":"915819829061836801014523","timeId":"915819828558520328708909","title":"现场票","type":1,"price":150.00,"priceExpress":0.00,"memberPrice":150.00,"discountPrice":150.00,"describes":"","describeExpress":"","describeElectronic":"电子票下单后无法更改为快递票。门票不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。请确认个人信息填写正确，成功购票后无法修改。演出当日可至演出现场凭身份证原件兑换纸质票入场","timeStart":"2022-03-07 12:00:00","timeEnd":"2022-05-07 22:30:00","memberTimeStart":"2022-03-07 11:55:00","timeEndExpress":"2030-01-01 12:00:00","useStart":"2022-05-07 00:00:00","useEnd":"2022-05-07 00:00:00","saleRemindMinute":60,"isStudent":0,"isElectronic":1,"isExpress":0,"sysDamai":0,"counts":1,"status":6,"statusExchange":7,"isLackRegister":1,"expressType":0,"isTrueName":0,"limitCount":0,"limitCountMember":1,"isExclusive":0,"isMember":1,"isMemberStatus":1,"isAgent":0,"isShowCode":1,"qrCodeShowTime":"2022-03-04 15:44:51","advanceMinuteMember":5,"totalGeneral":50,"totalExchange":0}]}],"agentName":null,"createdAt":"2022-03-08 13:10:18","isCanRefund":0,"isOpenRefundPresent":0,"refundOpenTime":null,"refundCloseTime":null,"isTransfer":0,"transferStartTime":null,"transferEndTime":null,"isRefundPoundage":0,"isRefundVoucher":0,"isRefundExpress":0,"isBackPaperTicket":1,"isRefundExpressNew":1,"auditStatus":1,"rejectTxt":"","merchantId":"1120839","fieldAuditStatus":0},"ticketInfo":{"mid":3957,"ticketsId":"915819828768235523792821","timeId":"915819828558520328708909","title":"预售单人票","type":1,"price":122.22,"priceExpress":0.00,"memberPrice":122.22,"discountPrice":122.22,"describes":"","describeExpress":"","describeElectronic":"电子票下单后无法更改为快递票。门票不可退票不可转让，因“不可抗力”导致的演出取消或延期除外。请确认个人信息填写正确，成功购票后无法修改。演出当日可至演出现场凭身份证原件兑换纸质票入场","timeStart":"2022-03-07 12:00:00","timeEnd":"2022-05-07 00:00:00","memberTimeStart":"2022-03-07 11:55:00","timeEndExpress":"2030-01-01 12:00:00","useStart":"2022-05-07 00:00:00","useEnd":"2022-05-07 00:00:00","saleRemindMinute":60,"isStudent":0,"isElectronic":1,"isExpress":0,"sysDamai":0,"counts":1,"status":6,"statusExchange":7,"isLackRegister":1,"expressType":0,"isTrueName":0,"limitCount":0,"limitCountMember":1,"isExclusive":0,"isMember":1,"isMemberStatus":1,"isAgent":0,"isShowCode":1,"qrCodeShowTime":"2022-03-04 15:44:51","advanceMinuteMember":5,"totalGeneral":150,"totalExchange":0},"expressModuleList":null},"success":true}
        """
        pass

    def encode_sign(self):
        """
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
    # zhengzai.login(15192748090, 595886)
    # zhengzai.show_list(310100)

    pass

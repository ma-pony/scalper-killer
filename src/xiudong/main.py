# 1. 登录获取token
# 2. 获取账户信息
# 3. 获取演出信息
# 4. 获取开售时间及限制


class XiuDongUser:

    def get_phone(self):
        pass

    def get_code(self):
        pass

    def click_get_code(self):
        pass

    def image_captcha(self):
        """
        https://wap.showstart.com/api/hw/000000000000
        request: {"data":"RdKnoWKXGxZP0zYw1ohcYqf4WtmU8a2fRA6A41UwPJb3SM5VDT+4EWNFFqFZqGlxM8ojGexamSLkMvsRc2icH3PtO/a9aE6mIU3P1CFkxYwTydzpznvUifGb4uCLOy+vhQybxC42n+qUW6EdtmivobqXfJ5tzxX859+xqX9W7s48FjDQQX55HIYFoVoK+/JliMTa+ufrbcQCB5RseP5zQtRRRKUhEEW6yBS5JcdmIVvCrAortrJSayKk2jEA1mRisszvleGPL5WrbnoMUad5bayHLhFHjAoydjztkQjaVaY=","sign":"585f72173e9b1362e135cb151dcaf362","appid":"wap","terminal":"wap","version":"997"}
        response: {"status":200,"state":"1","result":{"appLogin":1,"appPassword":1,"appTelephone":1,"wapLogin":1,"wapLogout":1,"wapRefund":1,"suduLogin":1,"suduRegister":1,"suduTelephone":1,"suduAccount":1,"adminLogin":1},"traceId":"c671b0d4d9bbb873c84bce96cfdd1e49-2"}
        https://t.captcha.qq.com/cap_union_new_verify
        request: {"status":200,"state":"1","result":{"appLogin":1,"appPassword":1,"appTelephone":1,"wapLogin":1,"wapLogout":1,"wapRefund":1,"suduLogin":1,"suduRegister":1,"suduTelephone":1,"suduAccount":1,"adminLogin":1},"traceId":"c671b0d4d9bbb873c84bce96cfdd1e49-2"}
        https://wap.showstart.com/api/hw/000000000000
        request: {"status":200,"state":"1","result":{"appLogin":1,"appPassword":1,"appTelephone":1,"wapLogin":1,"wapLogout":1,"wapRefund":1,"suduLogin":1,"suduRegister":1,"suduTelephone":1,"suduAccount":1,"adminLogin":1},"traceId":"c671b0d4d9bbb873c84bce96cfdd1e49-2"}
        response: {"status":200,"state":"1","traceId":"8a3eb7c3df5c55fed44de5fa33d7e210-2"}
        :return:
        """

        pass

    def login(self):
        pass


class XiuDongShow:
    pass


class BuyTicket:
    pass

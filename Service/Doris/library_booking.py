import re
import time

from SmartDjango import E
from aip import AipOcr

import requests

from Model.Base.Config.models import Config, CI

LB_HOST = "http://libwx2.zjgsu.edu.cn:85"
WEB_URI = LB_HOST + "/home/book/more/lib/11/type/4"
LOGIN_URI = LB_HOST + "/api.php/login"
CAPTCHA_URI = LB_HOST + "/api.php/check"
BOOKING_URI = LB_HOST + "/api.php/activities/%s/application2?mobile=%s"


bd_app_id = Config.get_value_by_key(CI.LibBooking_BD_APP_ID)
bd_app_key = Config.get_value_by_key(CI.LibBooking_BD_APP_KEY)
bd_app_secret = Config.get_value_by_key(CI.LibBooking_BD_APP_SECRET)

replace_table = {
    "o": 0, "O": 0, "。": 0,
    "I": 1, "l": 1,
    "z": 2, "Z": 2,
    "A": 4,
    "s": 5, "S": 5, "与": 5,
    "G": 6, "b": 6,
    ">": 7,
    "e": 8,
    "q": 9,
}

client = AipOcr(bd_app_id, bd_app_key, bd_app_secret)


@E.register()
class LibraryBookingServiceError:
    RETRY_TIME_EXPIRE = E("请再试一次")
    PASSWORD_INCORRECT = E("登录密码不正确")
    ABNORMAL = E("系统异常")
    BOOK_FAIL = E("")


class LibraryBookingService:
    @staticmethod
    def recognize_captcha(session):
        retry_time = 5
        captcha = ''
        recognized = False

        while retry_time:
            retry_time -= 1
            time.sleep(1)
            recognized = True

            try:
                with session.get(CAPTCHA_URI, headers={"Referer": WEB_URI}) as r:
                    image = r.content

                result = client.basicGeneral(image, {})
                result = result["words_result"][0]["words"]
            except Exception:
                result = ''

            if len(result) != 4:
                recognized = False
                continue

            captcha = ''
            for digit in result:
                if digit in "1234567890":
                    captcha += digit
                elif digit in replace_table:
                    captcha += str(replace_table[digit])
                else:
                    recognized = False
                    continue

            break

        if not recognized:
            raise LibraryBookingServiceError.RETRY_TIME_EXPIRE

        return captcha

    @classmethod
    def book(cls, student_id, password, phone):
        session = requests.Session()

        retry_time = 3
        while retry_time:
            retry_time -= 1

            try:
                captcha = cls.recognize_captcha(session)
            except E as err:
                if retry_time:
                    continue
                else:
                    raise err

            with session.post(LOGIN_URI, data={
                "username": student_id,
                "password": password,
                "verify": captcha
            }, headers={"Referer": WEB_URI}) as r:
                result = r.json()

            if result["msg"] == "验证码错误，请重新输入":
                continue
            if result["msg"] == "登录密码不正确":
                raise LibraryBookingServiceError.PASSWORD_INCORRECT
            if result["msg"] != "登陆成功":
                raise LibraryBookingServiceError.ABNORMAL(append_message=result["msg"])

            break

        with session.get(WEB_URI) as r:
            html = r.content.decode()
        act_id = re.search(
            '<a href="/book/notice/act_id/(\d+)/type/4/lib/11">', html, flags=re.S).group(1)

        with session.get(BOOKING_URI % (act_id, phone)) as r:
            result = r.json()
        if result["msg"] == '申请成功':
            username = result['data']['list']['applicantName']
            if username == '陈艳萍':
                username = '猪猪🐷'
            return username + result['msg']
        else:
            raise LibraryBookingServiceError.BOOK_FAIL(append_message=result["msg"])

    @staticmethod
    def view_remain():
        with requests.get(WEB_URI) as r:
            html = r.content.decode()
        remain = re.search('剩余预约<b> (\d+) </b>人', html, flags=re.S)
        if remain:
            return int(remain.group(1))
        else:
            return 0

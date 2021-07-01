import re

import requests
# from SmartDjango import E


NC_HOST = 'https://nco.zjgsu.edu.cn'
LOGIN_URI = NC_HOST + '/login'
MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) ' \
                    'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 ' \
                    'Mobile/15E148 Safari/604.1'
HEADERS = {"User-Agent": MOBILE_USER_AGENT}


# @E.register()
# class NcovClockinServiceError:
#     pass


class NcovClockinService:
    @staticmethod
    def login(student_id, password):
        session = requests.Session()
        with session.get(NC_HOST, headers=HEADERS) as r:
            html = r.content.decode()

        uuid = re.search(
            'var uuid = "(.*?)";', html, flags=re.S).group(1)
        session.cookies.set('_ncov_uuid', uuid)

        with session.post(LOGIN_URI, data={
            "name": student_id,
            "psswd": password,
        }, headers=HEADERS) as r:
            _ = r.content.decode()

        print(session.cookies)


NcovClockinService.login('1707090212', 'yunzhanyi2020')

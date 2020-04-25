from SmartDjango import P, Analyse

from Base.handler import BaseHandler
from Service.Doris.library_booking import LibraryBookingService


class LibraryBooking(BaseHandler):
    APP_NAME = '图书馆一键预约'
    APP_DESC = '浙江工商大学疫情期间的图书馆便捷预约'

    BODY = [
        P('id', '一卡通号'),
        P('password', '密码').default('000'),
        P('phone', '电话号码'),
    ]

    @staticmethod
    @Analyse.r(b=BODY)
    def run(r):
        student_id = r.d.id
        password = r.d.password
        phone = r.d.phone
        return LibraryBookingService.book(str(student_id), password, phone)


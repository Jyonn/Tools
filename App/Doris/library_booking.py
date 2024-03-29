import datetime

from SmartDjango import P, Analyse

from Base.handler import BaseHandler
from Service.Doris.library_booking import LibraryBookingService


class LibraryBooking(BaseHandler):
    APP_NAME = '图书馆一键预约'
    APP_DESC = '浙江工商大学疫情期间的图书馆便捷预约'

    BODY = [
        P('id', '一卡通号').default(None),
        P('password', '密码').default('000'),
        P('phone', '电话号码').default(None),
        P('view_only').default(False),
        P('list_date').default(False),
        P('date').default(False),
    ]

    @staticmethod
    @Analyse.r(b=BODY)
    def run(r):
        student_id = r.d.id
        password = r.d.password
        phone = r.d.phone
        view_only = r.d.view_only
        list_date = r.d.list_date
        date = r.d.date

        if list_date:
            return LibraryBookingService.list_date()
        if not date:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        if view_only:
            return LibraryBookingService.view_remain(date)
        return LibraryBookingService.book(date, str(student_id), password, phone)


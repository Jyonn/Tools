import datetime

from smartdjango import Validator, analyse

from Base.handler import BaseHandler
from Service.Doris.library_booking import LibraryBookingService


class LibraryBooking(BaseHandler):
    APP_NAME = '图书馆一键预约'
    APP_DESC = '浙江工商大学疫情期间的图书馆便捷预约'

    BODY = [
        Validator('id', '一卡通号').default(None).null(),
        Validator('password', '密码').default('000').null(),
        Validator('phone', '电话号码').default(None).null(),
        Validator('view_only').default(False).null(),
        Validator('list_date').default(False).null(),
        Validator('date').default(False).null(),
    ]

    @staticmethod
    @analyse.json(*BODY)
    def run(request):
        student_id = request.json.id
        password = request.json.password
        phone = request.json.phone
        view_only = request.json.view_only
        list_date = request.json.list_date
        date = request.json.date

        if list_date:
            return LibraryBookingService.list_date()
        if not date:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
        if view_only:
            return LibraryBookingService.view_remain(date)
        return LibraryBookingService.book(date, str(student_id), password, phone)


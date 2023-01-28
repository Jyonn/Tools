import datetime

import requests
from django import views

from Model.Base.Config.models import Config, CI
from Model.Network.VPNNet.models import Record, VPNNetError, Session
from dev.Network.VPNNet.base import CHECK_INTERVAL, LOGIN_URL, EMAIL, PASSWORD, LOG_URL


class UpdateView(views.View):
    @staticmethod
    def get(_):
        last_check = int(Config.get_value_by_key(CI.VPNNET_LAST_CHECK) or 0)
        now = datetime.datetime.now()
        now_ts = int(now.timestamp())
        if now_ts - last_check < CHECK_INTERVAL:
            return VPNNetError.INTERVAL_NOT_REACHED

        Config.update_value(CI.VPNNET_LAST_CHECK, str(now_ts))

        # use requests to log in, with form data
        session = requests.Session()
        with session.post(LOGIN_URL, data={
            'email': EMAIL,
            'password': PASSWORD,
        }) as r:
            if r.status_code != 200:
                return VPNNetError.LOGIN_FAILED

        # use requests to get the log page
        with session.get(LOG_URL) as r:
            if r.status_code != 200:
                return VPNNetError.LOG_FAILED
            data = r.json()['data']

        # save the log to the database, only data from today and yesterday will be saved
        for log in data:
            time = log['log_at']  # type: int
            time = datetime.datetime.fromtimestamp(time)  # type: datetime.datetime
            if time.date() != now.date() and time.date() != now.date() - datetime.timedelta(days=1):
                continue
            Record.update(
                date=time.date(),
                rate=log['rate'],
                upload=log['u'],
                download=log['d'],
            )

        return 0


class SessionView(views.View):
    @staticmethod
    def get(_):
        return Session.list_30_days()

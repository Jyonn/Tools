import datetime

from SmartDjango import models, E


@E.register(id_processor=E.idp_cls_prefix())
class VPNNetError:
    RECORD_NOT_FOUND = E('找不到记录')
    INTERVAL_NOT_REACHED = E('间隔未到')
    LOGIN_FAILED = E('登录失败')
    LOG_FAILED = E('获取日志失败')


class Record(models.Model):
    class Meta:
        unique_together = ('date', 'rate')

    date = models.DateField(
        verbose_name='日期',
    )

    rate = models.CharField(
        verbose_name='速率',
        max_length=10,
    )

    upload = models.PositiveIntegerField(
        verbose_name='上传数据量',
        default=0,
    )

    download = models.PositiveIntegerField(
        verbose_name='下载数据量',
        default=0,
    )

    @classmethod
    def get(cls, date, rate):
        try:
            return cls.objects.get(date=date, rate=rate)
        except cls.DoesNotExist:
            raise VPNNetError.RECORD_NOT_FOUND

    @classmethod
    def create(cls, date, rate):
        return cls.objects.create(date=date, rate=rate)

    @classmethod
    def get_or_create(cls, date, rate):
        try:
            return cls.get(date, rate)
        except E as e:
            assert e.eis(VPNNetError.RECORD_NOT_FOUND)
            return cls.create(date, rate)
        except Exception as e:
            raise e

    @classmethod
    def update(cls, date: datetime.date, rate, upload, download):
        record = cls.get_or_create(date, rate)
        updated = record.upload != upload or record.download != download
        record.upload = upload
        record.download = download
        record.save()

        if updated and date == datetime.date.today():
            Session.insert(record)

    def d(self):
        return self.dictify('date', 'rate', 'upload', 'download')


class Session(models.Model):
    INTERVAL = 30 * 60

    record = models.ForeignKey(
        Record,
        on_delete=models.CASCADE,
        verbose_name='记录',
        default=None,
        null=True,
        blank=True,
    )

    start = models.DateTimeField(
        verbose_name='开始时间',
    )

    end = models.DateTimeField(
        verbose_name='结束时间',
    )

    start_upload = models.PositiveIntegerField(
        verbose_name='开始上传数据量',
        default=0,
    )

    start_download = models.PositiveIntegerField(
        verbose_name='开始下载数据量',
        default=0,
    )

    end_upload = models.PositiveIntegerField(
        verbose_name='结束上传数据量',
        default=0,
    )

    end_download = models.PositiveIntegerField(
        verbose_name='结束下载数据量',
        default=0,
    )

    @classmethod
    def latest_today(cls, record):
        today = datetime.date.today()
        return cls.objects.filter(date=today, record=record).order_by('-end').first()

    @classmethod
    def create(cls, record: Record):
        now = datetime.datetime.now()
        upload = int(record.upload // float(record.rate))
        download = int(record.download // float(record.rate))
        return cls.objects.create(
            record=record,
            start=now,
            end=now,
            start_upload=upload,
            start_download=download,
            end_upload=upload,
            end_download=download,
        )

    @classmethod
    def insert(cls, record: Record):
        latest_session = cls.latest_today(record)
        if latest_session is None:
            return cls.create(record)

        now = datetime.datetime.now()
        if (now - latest_session.end).total_seconds() > cls.INTERVAL:
            return cls.create(record)

        latest_session.end = now
        latest_session.end_upload = int(record.upload // float(record.rate))
        latest_session.end_download = int(record.download // float(record.rate))
        latest_session.save()
        return latest_session

    @staticmethod
    def _readable_time(time):
        return time.strftime('%H:%M:%S')

    def _readable_start(self):
        assert isinstance(self.start, datetime.datetime)
        return self._readable_time(self.start)

    def _readable_end(self):
        assert isinstance(self.end, datetime.datetime)
        return self._readable_time(self.end)

    @staticmethod
    def _readable_size(size):
        if size < 1024:
            return f'{size}B'
        size = int(size / 1024)
        if size < 1024:
            return f'{size}KB'
        size = int(size / 1024)
        if size < 1024:
            return f'{size}MB'
        size = int(size / 1024)
        return f'{size}GB'

    def _readable_upload(self):
        byte = self.end_upload - self.start_upload
        return self._readable_size(byte)

    def _readable_download(self):
        byte = self.end_download - self.start_download
        return self._readable_size(byte)

    def _readable_date(self):
        if self.record:
            return self.record.date.strftime('%Y-%m-%d')
        return None

    @classmethod
    def list_30_days(cls):
        today = datetime.date.today()
        thirty_days_ago = today - datetime.timedelta(days=30)
        return cls.objects.filter(date__gte=thirty_days_ago).order_by('-date').dict(cls.d)

    def d(self):
        return self.dictify(
            'start', 'end', 'upload', 'download', 'date'
        )

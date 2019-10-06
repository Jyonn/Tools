import codecs
import os
import sys

import django

sys.path.extend(['../..'])

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Tools.settings")
django.setup()

from Base.param_limit import PL
from Model.Network.IP.models import IP


PROVINCES = [
    "河北省", "山西省", "吉林省", "辽宁省", "黑龙江省", "陕西省", "甘肃省", "青海省", "山东省", "福建省",
    "浙江省", "台湾省", "河南省", "湖北省", "湖南省", "江西省", "江苏省", "安徽省", "广东省", "海南省",
    "四川省", "贵州省", "云南省", "北京市", "上海市", "天津市", "重庆市", "内蒙古自治区", "新疆维吾尔自治区",
    "宁夏回族自治区", "广西壮族自治区", "西藏自治区", "香港特别行政区", "澳门特别行政区"
]


class IPLoader:
    @staticmethod
    def check_ip():
        with codecs.open('ipdb_20190325_cn.txt', 'r', encoding='utf8') as f:
            ips = f.readlines()
            ips = list(map(lambda x: x[:-2], ips))
            ips = list(map(lambda x: x.split(','), ips))

        for ip in ips:
            if len(ip) != 7:
                print(ip)
                continue
            lens = [20, 20, 10, 10, 20, 30, 30]
            for index, ip_data_seg in enumerate(ip):
                if len(ip_data_seg) >= lens[index]:
                    print(ip)
            map(PL.ip_dot2int, ip[:2])

        print(len(ips))

    @staticmethod
    def load_ip():
        with codecs.open('ipdb_20190325_cn.txt', 'r', encoding='utf8') as f:
            ips = f.readlines()
            ips = list(map(lambda x: x[:-2], ips))
            ips = list(map(lambda x: x.split(','), ips))

        for ip in ips:
            ip[:2] = list(map(PL.ip_dot2int, ip[:2]))
            if ip[3]:
                for province in PROVINCES:
                    if province.startswith(ip[3]):
                        ip[3] = province
                        break

            IP.new(*ip)


IPLoader.load_ip()

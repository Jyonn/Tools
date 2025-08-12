import requests
from django.http import HttpRequest
from qiniu import urlsafe_base64_encode
from smartdjango import Error, Code


@Error.register
class QNErrors:
    REQUEST_QINIU = Error("七牛请求错误", code=Code.BadRequest)
    QINIU_UNAUTHORIZED = Error("七牛端身份验证错误", code=Code.Unauthorized)
    FAIL_QINIU = Error("未知原因导致的七牛端操作错误", code=Code.BadRequest)
    UNAUTH_CALLBACK = Error("未经授权的回调函数", code=Code.Forbidden)


class QnManager:
    QINIU_MANAGE_HOST = "https://rs.qiniu.com"

    def __init__(self, auth, bucket, cdn_host, public, prefix):
        self.auth = auth
        self.bucket = bucket
        self.cdn_host = cdn_host
        self.public = public
        self.prefix = prefix

    @staticmethod
    def encode_key(key):
        key = key.replace('@', '@@')
        key = key.replace('$', '@S')
        return key

    @staticmethod
    def decode_key(key: str):
        new_key = ''
        while True:
            p_at = key.find('@')
            if p_at == -1:
                new_key += key
                break
            new_key += key[:p_at]
            if key[p_at + 1] == '@':
                new_key += '@'
            elif key[p_at + 1] == 'S':
                new_key += '$'
            else:
                pass
            key = key[p_at+2:]

        return new_key

    def get_upload_token(self, key, policy):
        """
        获取七牛上传token
        :param policy: 上传策略
        :param key: 规定的键
        """
        key = self.prefix + key
        return self.auth.upload_token(bucket=self.bucket, key=key, expires=3600, policy=policy), key

    def auth_callback(self, request: HttpRequest):
        """七牛callback认证校验"""
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is None:
            raise QNErrors.UNAUTH_CALLBACK
        url = request.get_full_path()
        body = request.body
        verified = self.auth.verify_callback(auth_header, url, body,
                                             content_type='application/json')
        if not verified:
            raise QNErrors.UNAUTH_CALLBACK

    def get_image(self, key, expires=3600, auto_rotate=True, resize=None, quality=100):
        if auto_rotate:
            if resize:
                if isinstance(resize, int):
                    resize = (resize, resize)
                if not resize[0]:
                    suffix = 'imageMogr2/auto-orient/thumbnail/x%s/blur/1x0/quality/%s' % (resize[1], quality)
                elif not resize[1]:
                    suffix = 'imageMogr2/auto-orient/thumbnail/%sx/blur/1x0/quality/%s' % (resize[0], quality)
                else:
                    suffix = 'imageView2/1/w/%s/h/%s/interlace/1/q/%s' % (resize[0], resize[1], quality)
            else:
                suffix = 'imageView2/0/interlace/1/q/%s' % quality
            url = '%s/%s?%s' % (self.cdn_host, key, suffix)
        else:
            url = '%s/%s' % (self.cdn_host, key)
        if self.public:
            return url
        else:
            return self.auth.private_download_url(url, expires=expires)

    def get_image_exif(self, key, expires=3600):
        url = '%s/%s?exif' % (self.cdn_host, key)
        if self.public:
            return url
        return self.auth.private_download_url(url, expires=expires)

    @classmethod
    def deal_manage_res(cls, target, access_token):
        url = '%s%s' % (cls.QINIU_MANAGE_HOST, target)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'QBox %s' % access_token,
        }

        try:
            r = requests.post(url, headers=headers)
        except requests.exceptions.RequestException:
            raise QNErrors.REQUEST_QINIU
        status = r.status_code
        r.close()
        if status == 200:
            return
        elif status == 401:
            raise QNErrors.QINIU_UNAUTHORIZED
        else:
            raise QNErrors.FAIL_QINIU('状态错误%s' % status)

    def delete_res(self, key):
        entry = '%s:%s' % (self.bucket, key)
        encoded_entry = urlsafe_base64_encode(entry)
        target = '/delete/%s' % encoded_entry
        access_token = self.auth.token_of_request(target, content_type='application/json')
        return self.deal_manage_res(target, access_token)

    def move_res(self, key, new_key):
        entry = '%s:%s' % (self.bucket, key)
        encoded_entry = urlsafe_base64_encode(entry)
        new_entry = '%s:%s' % (self.bucket, new_key)
        encoded_new_entry = urlsafe_base64_encode(new_entry)
        target = '/move/%s/%s' % (encoded_entry, encoded_new_entry)
        access_token = self.auth.token_of_request(target, content_type='application/json')
        return self.deal_manage_res(target, access_token)

""" 180228 Adel Liu

七牛上传政策
"""
import json


class Policy:
    def __init__(self, callback_url, max_image_size):
        self.callback_url = callback_url
        self.max_image_size = max_image_size

    def customize(self, **params):
        params.update(dict(
            key="$(key)",
            mime_type="$(mimeType)",
            color_average="$(imageAve)",
            image_info="$(imageInfo)"
        ))
        callback_body = json.dumps(params, ensure_ascii=False)
        callback_body = callback_body.replace('"$(imageInfo)"', '$(imageInfo)') \
            .replace('"$(imageAve)"', '$(imageAve)')

        policy = dict(
            callbackBody=callback_body,
            callbackUrl=self.callback_url
        )
        policy.update(dict(
            insertOnly=1,
            callbackBodyType='application/json',
            fsizeMin=1,
            fsizeLimit=self.max_image_size,
            mimeLimit='image/png;image/jpeg;image/heic',
        ))
        return policy

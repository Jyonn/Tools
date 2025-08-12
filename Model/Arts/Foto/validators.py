from smartdjango import Error, Code


@Error.register
class FotoErrors:
    NOT_FOUND = Error("图片不存在", code=Code.NotFound)
    CREATE = Error("图片上传失败", code=Code.InternalServerError)
    AS_COVER = Error("相册封面无法删除", code=Code.Forbidden)

    ALBUM_CREATE = Error("新增相册失败", code=Code.InternalServerError)
    ALBUM_NOT_FOUND = Error("相册不存在", code=Code.NotFound)
    ALBUM_NAME_TOO_SHORT = Error("相册名称需要至少{length}个字符", code=Code.BadRequest)

    SPACE_CREATE = Error("新增空间失败", code=Code.InternalServerError)
    SPACE_NOT_FOUND = Error("空间不存在", code=Code.NotFound)
    SPACE_NAME_TOO_SHORT = Error("空间名称需要至少{length}个字符", code=Code.BadRequest)

    FOTO_ID_TOO_SHORT = Error("图片ID需要至少{length}个字符", code=Code.BadRequest)


class SpaceValidator:
    MAX_NAME_LENGTH = 20
    MIN_NAME_LENGTH = 1

    @classmethod
    def name(cls, name):
        if len(name) < cls.MIN_NAME_LENGTH:
            raise FotoErrors.SPACE_NAME_TOO_SHORT(length=cls.MIN_NAME_LENGTH)


class AlbumValidator:
    MAX_NAME_LENGTH = 20
    MIN_NAME_LENGTH = 1

    @classmethod
    def name(cls, name):
        if len(name) < cls.MIN_NAME_LENGTH:
            raise FotoErrors.ALBUM_NAME_TOO_SHORT(length=cls.MIN_NAME_LENGTH)



class FotoValidator:
    MAX_FOTO_ID_LENGTH = 6
    MIN_FOTO_ID_LENGTH = 6
    MAX_KEY_LENGTH = 100
    MAX_COLOR_AVERAGE_LENGTH = 20
    MAX_MIME_TYPE_LENGTH = 50

    @classmethod
    def foto_id(cls, foto_id):
        if len(foto_id) < cls.MIN_FOTO_ID_LENGTH:
            raise FotoErrors.FOTO_ID_TOO_SHORT(length=cls.MIN_FOTO_ID_LENGTH)


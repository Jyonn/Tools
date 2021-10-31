import datetime

from SmartDjango import models, E
from django.utils.crypto import get_random_string
from smartify import P

from dev.Arts.Foto.base import qn_manager, policy


@E.register(id_processor=E.idp_cls_prefix())
class FotoError:
    NOT_FOUND = E("图片不存在")
    CREATE = E("图片上传失败")
    AS_COVER = E("相册封面无法删除")

    ALBUM_CREATE = E("新增相册失败")
    ALBUM_NOT_FOUND = E("相册不存在")

    SPACE_CREATE = E("新增空间失败")
    SPACE_NOT_FOUND = E("空间不存在")


class Space(models.Model):
    name = models.CharField(
        max_length=20,
        min_length=1,
        unique=True,
    )

    @classmethod
    def create(cls, name):
        try:
            return cls.get_by_name(name)
        except Exception:
            pass

        try:
            return cls.objects.create(name=name)
        except Exception as err:
            raise FotoError.SPACE_CREATE(debug_message=err)

    @classmethod
    def get_by_name(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist as err:
            raise FotoError.SPACE_NOT_FOUND(debug_message=err)

    def d(self):
        albums = self.album_set.dict(Album.d)
        fotos = Foto.get_pinned_fotos(space=self).dict(Foto.d)

        return dict(
            albums=albums,
            fotos=fotos,
        )


class Album(models.Model):
    class Meta:
        unique_together = ('name', 'space')

    name = models.CharField(
        max_length=20,
        min_length=1,
    )

    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    @classmethod
    def create(cls, name, space):
        try:
            return cls.get_by_name(name, space)
        except Exception:
            pass

        try:
            return cls.objects.create(name=name, space=space)
        except Exception as err:
            raise FotoError.ALBUM_CREATE(debug_message=err)

    @classmethod
    def get_by_name(cls, name, space):
        try:
            return cls.objects.get(name=name, space=space)
        except cls.DoesNotExist as err:
            raise FotoError.ALBUM_NOT_FOUND(debug_message=err)

    @classmethod
    def getter(cls, value):
        value['album'] = cls.get_by_name(name=value['album'], space=value['space'])
        return value

    @classmethod
    def creator(cls, value):
        value['album'] = cls.create(name=value['album'], space=value['space'])
        return value

    def _readable_fotos(self):
        return self.foto_set.dict(Foto.d)

    def d(self):
        return self.dictify('name')

    def d_with_fotos(self):
        return self.dictify('name', 'fotos')

    def remove(self):
        self.delete()

    def rename(self, name):
        self.name = name
        self.save()


class Foto(models.Model):
    foto_id = models.CharField(
        max_length=6,
        min_length=6,
        unique=True,
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
    )

    key = models.CharField(
        max_length=100,
        unique=True,
    )

    width = models.IntegerField()
    height = models.IntegerField()

    color_average = models.CharField(
        max_length=20,
        null=True,
        default=None,
    )

    mime_type = models.CharField(
        max_length=50,
    )

    orientation = models.IntegerField(
        default=1,
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
    )

    pinned = models.BooleanField(
        default=False,
    )

    @classmethod
    def is_id_unique(cls, foto_id):
        try:
            cls.objects.get(foto_id=foto_id)
            return False
        except cls.DoesNotExist:
            return True

    @classmethod
    def generate_foto_id(cls):
        while True:
            foto_id = get_random_string(6)
            if cls.is_id_unique(foto_id):
                return foto_id

    @classmethod
    def orientation_str2int(cls, orientation: list):
        if orientation[0] == 'TOP':
            return 1 if orientation[1] == 'LEFT' else 2
        elif orientation[0] == 'BOTTOM':
            return 4 if orientation[1] == 'LEFT' else 3
        elif orientation[1] == 'TOP':
            return 5 if orientation[1] == 'LEFT' else 6
        else:
            return 8 if orientation[1] == 'LEFT' else 7

    @classmethod
    def orientation_int2str(cls, orientation: int):
        o = orientation - 1
        s = [''] * 2

        s[o // 4] = 'TOP' if orientation in [1, 2, 5, 6] else 'BOTTOM'
        s[1 - o // 4] = 'LEFT' if orientation in [1, 4, 5, 8] else 'RIGHT'
        return '-'.join(s)

    def set_album(self, album):
        self.album = album
        self.save()

    def toggle_pin(self):
        self.pinned = not self.pinned
        self.save()

    @classmethod
    def get(cls, foto_id):
        try:
            return cls.objects.get(foto_id=foto_id)
        except cls.DoesNotExist:
            return FotoError.NOT_FOUND

    @classmethod
    def create(cls, width, height, orientation, **kwargs):
        if orientation >= 5:
            width, height = height, width

        try:
            return cls.objects.create(
                **kwargs,
                width=width,
                height=height,
                orientation=orientation,
                foto_id=cls.generate_foto_id(),
            )
        except Exception as err:
            raise FotoError.CREATE(debug_message=err)

    @classmethod
    def get_tokens(cls, num, **kwargs):
        key_prefix = hex(int(datetime.datetime.now().timestamp() * 1000))

        tokens = []
        for _ in range(num):
            key = key_prefix + '/' + get_random_string(length=16)
            tokens.append(qn_manager.get_upload_token(
                key=key, policy=policy.customize(**kwargs)))
        return tokens

    def get_source(self, expires=3600, auto_rotate=True, resize=None):
        return qn_manager.get_image(
            self.key, expires=expires, auto_rotate=auto_rotate, resize=resize)

    def get_sources(self):
        return dict(
            origin=self.get_source(auto_rotate=False, resize=None),
            square=self.get_source(auto_rotate=True, resize=(200, 200)),
            rotate=self.get_source(auto_rotate=True, resize=None)
        )

    def remove(self):
        qn_manager.delete_res(self.key)
        self.delete()

    @classmethod
    def get_pinned_fotos(cls, space):
        return cls.objects.filter(pinned=True, album__space=space)

    def _readable_sources(self):
        return dict(
            color=self.color_average,
            rotate=self.get_source(auto_rotate=True, resize=None),
            origin=self.get_source(auto_rotate=False, resize=None),
            square=self.get_source(auto_rotate=True, resize=(600, 600)),
        )

    def _readable_orientation(self):
        return [self.orientation, self.orientation_int2str(self.orientation)]

    def _readable_album(self):
        return self.album.name

    def d(self):
        return self.dictify(
            'sources',
            'width',
            'height',
            'foto_id',
            'orientation',
            'album'
        )

    def d_base(self):
        return self.dictify(
            'album',
            'foto_id',
        )


class SpaceP:
    name = Space.get_param('name').rename('space')
    name_getter = name.clone().process(Space.get_by_name)


class AlbumP:
    name = Album.get_param('name').rename('album')


class FotoP:
    id_getter = Foto.get_param('foto_id').clone().rename('foto').process(Foto.get)

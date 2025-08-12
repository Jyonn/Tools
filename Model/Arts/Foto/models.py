import datetime

from diq import Dictify
from django.db import models
from django.utils.crypto import get_random_string

from Model.Arts.Foto.validators import SpaceValidator, FotoErrors, AlbumValidator, FotoValidator
from dev.Arts.Foto.base import qn_manager, policy


class Space(models.Model, Dictify):
    vldt = SpaceValidator

    name = models.CharField(
        max_length=vldt.MAX_NAME_LENGTH,
        unique=True,
        validators=[vldt.name]
    )

    @classmethod
    def create(cls, name):
        try:
            return cls.get_by_name(name)
        except Exception as _:
            pass

        try:
            return cls.objects.create(name=name)
        except Exception as err:
            raise FotoErrors.SPACE_CREATE(debug_message=err)

    @classmethod
    def get_by_name(cls, name):
        try:
            return cls.objects.get(name=name)
        except cls.DoesNotExist as err:
            raise FotoErrors.SPACE_NOT_FOUND(debug_message=err)

    def d(self):
        albums = self.album_set.dict(Album.d)
        fotos = Foto.get_pinned_fotos(space=self)
        fotos = [foto.d() for foto in fotos]

        return dict(
            albums=albums,
            fotos=fotos,
        )


class Album(models.Model, Dictify):
    vldt = AlbumValidator

    class Meta:
        unique_together = ('name', 'space')

    name = models.CharField(
        max_length=vldt.MAX_NAME_LENGTH,
        validators=[vldt.name]
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
        except Exception as _:
            pass

        try:
            return cls.objects.create(name=name, space=space)
        except Exception as err:
            raise FotoErrors.ALBUM_CREATE(debug_message=err)

    @classmethod
    def get_by_name(cls, name, space):
        try:
            return cls.objects.get(name=name, space=space)
        except cls.DoesNotExist as err:
            raise FotoErrors.ALBUM_NOT_FOUND(debug_message=err)

    def _dictify_fotos(self):
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


class Foto(models.Model, Dictify):
    vldt = FotoValidator

    foto_id = models.CharField(
        max_length=vldt.MAX_FOTO_ID_LENGTH,
        unique=True,
        validators=[vldt.foto_id]
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
    )

    key = models.CharField(
        max_length=vldt.MAX_KEY_LENGTH,
        unique=True,
    )

    width = models.IntegerField()
    height = models.IntegerField()

    color_average = models.CharField(
        max_length=vldt.MAX_COLOR_AVERAGE_LENGTH,
        null=True,
        default=None,
    )

    mime_type = models.CharField(
        max_length=vldt.MAX_MIME_TYPE_LENGTH,
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
            return FotoErrors.NOT_FOUND

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
            raise FotoErrors.CREATE(debug_message=err)

    @classmethod
    def get_tokens(cls, num, **kwargs):
        key_prefix = hex(int(datetime.datetime.now().timestamp() * 1000))

        tokens = []
        for _ in range(num):
            key = key_prefix + '/' + get_random_string(length=16)
            tokens.append(qn_manager.get_upload_token(
                key=key, policy=policy.customize(**kwargs)))
        return tokens

    def get_source(self, expires=3600, auto_rotate=True, resize=None, quality=100):
        url = qn_manager.get_image(
            self.key, expires=expires, auto_rotate=auto_rotate, resize=resize, quality=quality)
        return url

    def get_exif(self, expires=3600):
        return qn_manager.get_image_exif(self.key, expires=expires)

    def resize(self):
        target = 1200
        if self.width <= target and self.height <= target:
            return self.width, self.height

        if self.width > self.height:
            return target, target * self.height // self.width

        return target * self.width // self.height, target

    def get_sources(self):
        return dict(
            origin=self.get_source(auto_rotate=False, resize=None),
            square=self.get_source(auto_rotate=True, resize=(600, 600), quality=75),
            rotate=self.get_source(auto_rotate=True, resize=self.resize(), quality=75)
        )

    def remove(self):
        qn_manager.delete_res(self.key)
        self.delete()

    @classmethod
    def get_pinned_fotos(cls, space):
        return cls.objects.filter(pinned=True, album__space=space)

    def _dictify_sources(self):
        return dict(
            color=self.color_average,
            origin=self.get_source(auto_rotate=False, resize=None),
            square=self.get_source(auto_rotate=True, resize=(600, 600), quality=75),
            rotate=self.get_source(auto_rotate=True, resize=self.resize(), quality=75),
            exif=self.get_exif(),
        )

    def _dictify_orientation(self):
        return [self.orientation, self.orientation_int2str(self.orientation)]

    def _dictify_album(self):
        return self.album.name

    def d(self):
        return self.dictify(
            'sources',
            'width',
            'height',
            'foto_id',
            'orientation',
            'album',
            'pinned'
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

from SmartDjango import Analyse
from django.views import View
from smartify import P

from Model.Arts.Foto.models import Foto, AlbumP, Album, FotoP
from dev.Arts.Foto.auth import Auth
from dev.Arts.Foto.base import qn_manager, boundary


class CallbackView(View):
    """/dev/Arts/Foto/callback"""

    @staticmethod
    @Analyse.r(b=[
        'key',
        'mime_type',
        'color_average',
        'image_info',
        AlbumP.name_getter,
    ])
    def post(r):
        print(r.d.dict())
        qn_manager.auth_callback(r)

        color_average = r.d.color_average['RGB']  # type: str
        foto_info = r.d.image_info

        if 'orientation' in foto_info:
            try:
                orientation = foto_info['orientation'].upper().split('-')
                orientation = Foto.orientation_str2int(orientation)
            except Exception:
                orientation = 1
        else:
            orientation = 1
        width, height = foto_info['width'], foto_info['height']

        foto = Foto.create(
            **r.d.dict('key', 'mime_type', 'album'),
            color_average=color_average,
            width=width,
            height=height,
            orientation=orientation,
        )

        return foto.d()


class TokenView(View):
    @staticmethod
    @Analyse.r(
        q=[AlbumP.name_creator, P('image_num', '图片数量').process(boundary(max_=99, min_=1))]
    )
    @Auth.require_admin
    def get(r):
        album = r.d.album
        image_num = r.d.image_num

        return Foto.get_tokens(
            num=image_num,
            album=album.name,
        )


class HomeView(View):
    @staticmethod
    def get(_):
        albums = Album.objects.dict(Album.d)
        fotos = Foto.get_pinned_fotos().dict(Foto.d)

        return dict(
            albums=albums,
            fotos=fotos,
        )


class FotoView(View):
    @staticmethod
    @Analyse.r(
        a=[FotoP.id_getter]
    )
    def get(r):
        foto = r.d.foto
        return foto.d()

    @staticmethod
    @Analyse.r(
        a=[FotoP.id_getter],
        b=[AlbumP.name_creator],
    )
    @Auth.require_admin
    def put(r):
        foto = r.d.foto
        album = r.d.album
        foto.set_album(album)
        return foto.d_base()

    @staticmethod
    @Analyse.r(
        a=[FotoP.id_getter],
    )
    @Auth.require_admin
    def delete(r):
        foto = r.d.foto
        foto.remove()
        return 0


class AlbumView(View):
    @staticmethod
    @Analyse.r(
        a=[AlbumP.name_getter]
    )
    def get(r):
        album = r.d.album
        return album.d_with_fotos()

    @staticmethod
    @Analyse.r(
        a=[AlbumP.name_creator]
    )
    @Auth.require_admin
    def post(_):
        return 0

    @staticmethod
    @Analyse.r(
        a=[AlbumP.name_creator],
        b=[AlbumP.name]
    )
    @Auth.require_admin
    def put(r):
        album = r.d.album
        album.rename(r.d.name)
        return album.d()

    @staticmethod
    @Analyse.r(
        a=[AlbumP.name_getter]
    )
    @Auth.require_admin
    def delete(r):
        album = r.d.album
        album.remove()
        return 0

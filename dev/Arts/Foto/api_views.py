from SmartDjango import Analyse
from django.views import View
from smartify import P, PDict

from Model.Arts.Foto.models import Foto, AlbumP, Album, FotoP, SpaceP
from dev.Arts.Foto.auth import Auth
from dev.Arts.Foto.base import qn_manager, boundary


class CallbackView(View):
    """/dev/Arts/Foto/callback"""

    @staticmethod
    @Analyse.r(b=PDict().set_fields(
        'key',
        'mime_type',
        'color_average',
        'image_info',
        AlbumP.name,
        SpaceP.name_getter).process(Album.getter)
    )
    def post(r):
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
        q=PDict().set_fields(
            SpaceP.name_getter,
            AlbumP.name,
            P('image_num', '图片数量').process(boundary(max_=99, min_=1))
        ).process(Album.getter)
    )
    @Auth.require_admin
    def get(r):
        album = r.d.album
        image_num = r.d.image_num

        return Foto.get_tokens(
            num=image_num,
            album=album.name,
            space=album.space.name,
        )


class HomeView(View):
    @staticmethod
    @Analyse.r(q=[SpaceP.name_getter])
    def get(r):
        return r.d.space.d()


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
    )
    @Auth.require_admin
    def put(r):
        foto = r.d.foto
        foto.toggle_pin()
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
        q=PDict().set_fields(
            SpaceP.name_getter,
            AlbumP.name,
        ).process(Album.getter)
    )
    def get(r):
        album = r.d.album
        return album.d_with_fotos()

    @staticmethod
    @Analyse.r(
        q=PDict().set_fields(
            SpaceP.name_getter,
            AlbumP.name,
        ).process(Album.creator)
    )
    @Auth.require_admin
    def post(_):
        return 0

    @staticmethod
    @Analyse.r(
        q=PDict().set_fields(
            SpaceP.name_getter,
            AlbumP.name,
        ).process(Album.getter),
        b=[AlbumP.name]
    )
    @Auth.require_admin
    def put(r):
        album = r.d.album
        album.rename(r.d.name)
        return album.d()

    @staticmethod
    @Analyse.r(
        q=PDict().set_fields(
            SpaceP.name_getter,
            AlbumP.name,
        ).process(Album.getter)
    )
    @Auth.require_admin
    def delete(r):
        album = r.d.album
        album.remove()
        return 0

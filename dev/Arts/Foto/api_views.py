from django.views import View
from smartdjango import analyse, Validator, OK

from Model.Arts.Foto.models import Foto, Album
from Model.Arts.Foto.params import AlbumParams, SpaceParams, FotoParams
from dev.Arts.Foto.auth import Auth
from dev.Arts.Foto.base import qn_manager, boundary


class CallbackView(View):
    """/dev/Arts/Foto/callback"""

    @analyse.json(
        'key',
        'mime_type',
        'color_average',
        'image_info',
        AlbumParams.name,
        SpaceParams.name_getter
    )
    def post(self, request):
        qn_manager.auth_callback(request)
        request.json.album = Album.get_by_name(**request.json())

        color_average = request.json.color_average['RGB']  # type: str
        foto_info = request.json.image_info

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
            key=request.json.key,
            mime_type=request.json.mime_type,
            album=request.json.album,
            color_average=color_average,
            width=width,
            height=height,
            orientation=orientation,
        )

        return foto.d()


class TokenView(View):
    @analyse.query(
        SpaceParams.name_getter,
        AlbumParams.name,
        Validator('image_num', '图片数量').to(boundary(max_=99, min_=1))
    )
    @Auth.require_admin
    def get(self, request):
        album = Album.get_by_name(**request.json())
        image_num = request.json.image_num

        return Foto.get_tokens(
            num=image_num,
            album=album.name,
            space=album.space.name,
        )


class HomeView(View):
    @analyse.query(SpaceParams.name_getter)
    def get(self, request):
        return request.query.space.d()


class FotoView(View):
    @analyse.argument(FotoParams.id_getter)
    def get(self, request, **kwargs):
        foto = request.argument.foto
        return foto.d()

    @analyse.argument(FotoParams.id_getter)
    @Auth.require_admin
    def put(self, request):
        foto = request.argument.foto
        foto.toggle_pin()
        return foto.d_base()

    @analyse.argument(FotoParams.id_getter)
    @Auth.require_admin
    def delete(self, request):
        foto = request.argument.foto
        foto.remove()
        return OK


class AlbumView(View):
    @analyse.query(
        SpaceParams.name_getter,
        AlbumParams.name,
    )
    def get(self, request):
        album = Album.get_by_name(**request.query())
        return album.d_with_fotos()

    @analyse.json(
        SpaceParams.name_getter,
        AlbumParams.name,
    )
    @Auth.require_admin
    def post(self, request):
        # Album.creator(request.json())
        Album.create(**request.json())
        return OK

    @analyse.query(SpaceParams.name_getter, AlbumParams.name)
    @analyse.json(AlbumParams.name.copy().rename('name'))
    @Auth.require_admin
    def put(self, request):
        album = Album.get_by_name(**request.query())
        album.rename(request.body.name)
        return album.d()

    @analyse.query(
        SpaceParams.name_getter,
        AlbumParams.name,
    )
    @Auth.require_admin
    def delete(self, request):
        album = Album.get_by_name(**request.query())
        album.remove()
        return OK

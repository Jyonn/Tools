from smartdjango import Params, Validator

from Model.Arts.Foto.models import Foto, Space, Album


class SpaceParams(metaclass=Params):
    model_class = Space

    name = Validator('space')
    name_getter = Validator('space').to(Space.get_by_name)


class AlbumParams(metaclass=Params):
    model_class = Album

    name = Validator('album')
    name_getter = Validator('album').to(Album.get_by_name)


class FotoParams(metaclass=Params):
    model_class = Foto

    id_getter = Validator('foto_id', final_name='foto').to(Foto.get)

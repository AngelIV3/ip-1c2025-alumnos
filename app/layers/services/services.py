# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
def getAllImages():
    raw_data = transport.getAllImages()
    images = []

    for pokemon in range(len(raw_data)):
        images.append(translator.fromRequestIntoCard(raw_data[pokemon])) 

    
    return images

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if card.name.lower() == name.lower():
            filtered_cards.append(card)

    return filtered_cards


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.get_all_favourites(user)
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromRepositoryIntoCard(favourite)
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)
# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)

    favourites_names = []

    for pokemon in favourite_list:
        favourites_names.append(pokemon.name)
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'favourites_names': favourites_names})

# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')  

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = services.filterByCharacter(name)
        favourite_list = []
        

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list})
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon

def filter_by_type(request):
    type = request.POST.get('type', '')

    images = []
    favourite_list = []

    if type != '':
        raw_data = services.getAllImages()

        for n in range(len(raw_data)):
            if type == raw_data[n].types[0]:
                images.append(raw_data[n])
            else:
                continue

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)

    return render(request, 'favourites.html', {'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)

    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    favourite_list = services.getAllFavourites(request)

    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def exit(request):
    logout(request)
    return redirect('home')
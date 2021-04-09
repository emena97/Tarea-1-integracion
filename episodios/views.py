from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.template import loader

r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes')

class Serie():
    def __init__(self, nombre):
        self.nombre = nombre
        self.temp = dict()
        self.temporadas = []


class Temporada():
    def __init__(self, serie, numero):
        self.numero = numero
        self.serie = serie
        self.episodios = dict()


class Episodio():
    def __init__(self, dicto):
        self.id = int(dicto[0])
        self.title = dicto[1]
        self.season = int(dicto[2])
        self.air_date = dicto[3]
        self.characters = dicto[4]
        self.episode_number = int(dicto[5])
        self.series = dicto[6]


class Personaje():
    def __init__(self, dicto):
        self.id = int(dicto[0])
        self.name = dicto[1]
        self.occupation = dicto[2]
        self.img = dicto[3]
        self.status = dicto[4]
        self.nickname = dicto[5]
        self.appearance = dicto[6]
        self.portrayed = dicto[7]
        self.category = dicto[8]
        self.bcs_appearances = dicto[9]

bb = Serie('Breaking Bad')
bcs = Serie('Better Call Saul')

for i in r.json():
    e = Episodio(list(i.values()))
    if e.series == 'Breaking Bad':
        if e.season in bb.temporadas:
            bb.temp[e.season].episodios[e.episode_number] = e
        else:
            bb.temporadas.append(e.season)
            bb.temp[e.season] = Temporada('Breaking Bad', e.season)
            bb.temp[e.season].episodios[e.episode_number] = e
    else:
        if e.season in bcs.temporadas:
            bcs.temp[e.season].episodios[e.episode_number] = e
        else:
            bcs.temporadas.append(e.season)
            bcs.temp[e.season] = Temporada('Better Call Saul', e.season)
            bcs.temp[e.season].episodios[e.episode_number] = e




def index(request):
    context = {
        'bb_seasons_list': bb.temporadas,
        'bcs_seasons_list': bcs.temporadas,
    }
    return render(request, 'episodios/index.html', context)

def bb_seasons(request, season_id):
    episode_list = []
    for i in list(bb.temp[int(season_id)].episodios.values()):
        episode_list.append(i.title)
    context = {
        'episode_list': episode_list,
        'season_id': season_id,
    }
    return render(request, 'episodios/bb_seasons.html', context)

def bcs_seasons(request, season_id):
    episode_list = []
    for i in list(bcs.temp[int(season_id)].episodios.values()):
        episode_list.append(i.title)
    context = {
        'episode_list': episode_list,
        'season_id': season_id,
    }
    return render(request, 'episodios/bcs_seasons.html', context)

def bb_episodes(request, season_id, episode_name):
    for episode in list(bb.temp[season_id].episodios.values()):
        if episode.title == episode_name:
            episode_info = episode
    context = {
        'episode_id': episode_info.id,
        'episode_title': episode_info.title,
        'episode_season': episode_info.season,
        'episode_number': episode_info.episode_number,
        'episode_date': episode_info.air_date,
        'episode_characters': episode_info.characters,
        'episode_series': 'Breaking Bad',
    }
    return render(request, 'episodios/bb_episodes.html', context)

def bcs_episodes(request, season_id, episode_name):
    for episode in list(bcs.temp[season_id].episodios.values()):
        if episode.title == episode_name:
            episode_info = episode
    context = {
        'episode_id': episode_info.id,
        'episode_title': episode_info.title,
        'episode_season': episode_info.season,
        'episode_number': episode_info.episode_number,
        'episode_date': episode_info.air_date,
        'episode_characters': episode_info.characters,
        'episode_series': 'Better Call Saul',
    }
    return render(request, 'episodios/bcs_episodes.html', context)


def character(request, character):
    payload = {'name': character}
    r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters', params=payload)
    r = list(r.json()[0].values())
    p = Personaje(r)
    payload2 = {'author': character}
    r2 = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/quote', params=payload2)
    r2 = r2.json()
    quotes = []
    for dicto in r2:
        quotes.append(list(dicto.values())[1])

    context = {
        'character_id': p.id,
        'character_name': p.name,
        'character_occupation_list': p.occupation,
        'character_img': p.img,
        'character_status': p.status,
        'character_nickname': p.nickname,
        'character_bb_appearances': p.appearance,
        'character_portrayed': p.portrayed,
        'character_category': p.category,
        'character_bcs_appearances': p.bcs_appearances,
        'quotes': quotes,
    }
    return render(request, 'episodios/character.html', context)


def search(request):
    s = request.POST.get('buscar', "")
    characters_names = []
    i = 0
    c = 10
    while c > 9:
        payload = {'name': s, 'offset': i, 'limit': 10}
        r = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters', params=payload)
        r = r.json()
        c = len(r)
        for per in r:
            name = per['name']
            if name not in characters_names:
                characters_names.append(name)
        i += 10
    print(characters_names)
    matches = characters_names
    #for name in characters_names:
    #    if s.lower() in name.lower():
    #        matches.append(name)
    context = {
        'matching_names': matches
    }
    return render(request, 'episodios/search_results.html', context)

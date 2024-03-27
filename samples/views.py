from rich import print as rprint
import urllib
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import BandInfo, AlbumInfo, SongInfo, SourceInfo
from django.views.generic import ListView
from urllib.parse import unquote
import discogs_client as DiscogsClient
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic as YTMusicClient
import os
import json
from imdb import Cinemagoer

DISCOGS_USER_TOKEN=os.getenv('DISCOGS_USER_TOKEN')
SPOTIFY_CLIENT_ID=os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET=os.getenv('SPOTIFY_CLIENT_SECRET')
YTMUSIC_ACCESS_TOKEN=os.getenv('YTMUSIC_ACCESS_TOKEN')
YTMUSIC_REFRESH_TOKEN=os.getenv('YTMUSIC_REFRESH_TOKEN')

with open('oauth.json') as file:
    oauth = json.load(file)
oauth['access_token'] = YTMUSIC_ACCESS_TOKEN
oauth['refresh_token'] = YTMUSIC_REFRESH_TOKEN


discogs_client = DiscogsClient.Client('ExampleApplication/0.1', user_token=DISCOGS_USER_TOKEN)

spotify_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify_client = spotipy.Spotify(client_credentials_manager=spotify_credentials_manager)

ytMusic = YTMusicClient('oauth.json')

imdb_client = Cinemagoer()

def contribute(request):
    blank_uri = 'https://secure.gravatar.com/avatar/53bfb1fac188f4edb589cbd53460e409?s=100&r=pg&d=mm'
    album_data = []
    artist_data = []
    track_data = []
    track_obj = []
    if request.method == 'POST':
        rprint(request.POST)
        artist = request.POST.get('artist_name_or_discogs_id', '')
        print(artist)
        album = request.POST.get('album_name_or_discogs_id', '')
        track = request.POST.get('track_id', '')
        if artist.isnumeric() and not album and not track:
            stage = 'got_artist'
            artist_result = discogs_client.artist(int(artist))
            album_result = [rel for rel in artist_result.releases if type(rel) == DiscogsClient.models.Master and rel.data['artist'] == artist_result.name]
            album_data = [{'name': item.title, 'id': item.id, 'img': (getattr(item, 'images') or [{'uri': blank_uri}])[0]['uri']} for item in album_result]
        elif artist and not album and not track:
            stage = 'find_artist'
            artist_result = list(discogs_client.search(artist, type='artist'))[:6]
            artist_data = [{'name': item.name, 'id': item.id, 'img': (getattr(item, 'images') or [{'uri': blank_uri}])[0]['uri']} for item in artist_result]
        elif not artist and album.isnumeric() and not track:
            stage = 'got_album'
            album_result = discogs_client.master(int(album))
        elif not artist and album and not track:
            stage = 'find_album'
            album_result = list(discogs_client.search(album, type='master'))[:6]
            album_data = [{'name': item.title, 'id': item.id, 'img': (getattr(item, 'images') or [{'uri': blank_uri}])[0]['uri']} for item in album_result]
        elif artist.isnumeric() and album.isnumeric() and not track:
            stage = 'got_both'
            artist_result = discogs_client.artist(int(artist))
            album_result = discogs_client.master(int(album))
            track_data = [{'id': track.position, 'name': track.title}  for track in album_result.tracklist]
        elif artist and album and not track:
            stage = 'find_both'
            artist_result = list(discogs_client.search(artist, type='artist'))[:6]
            artist_data = [{'name': item.name, 'id': item.id, 'img': (getattr(item, 'images') or [{'uri': blank_uri}])[0]['uri']} for item in artist_result]
            album_result = list(discogs_client.search(album, type='master'))[:6]
            album_data = [{'name': item.title, 'id': item.id, 'img': (getattr(item, 'images') or [{'uri': blank_uri}])[0]['uri']} for item in album_result]
        elif track:
            stage = 'got_all'
            artist_result = discogs_client.artist(int(artist))
            album_result = discogs_client.master(int(album))
            track_result = album_result.tracklist[int(track) - 1]
            track_obj = {'artist': artist_result, 'album': album_result, 'track': track_result}
        else:
            artist = ''
            album = ''
            stage = 'start'
    else:
        artist = ''
        album = ''
        stage = 'start'
    context = {'artist': artist, 'album': album, 'album_data': album_data, 'artist_data': artist_data, 'track_data': track_data, 'stage': stage, 'track_obj': track_obj}
    print(stage)
    rprint(context)
    return render(request, 'samples/contribute.html', context=context)


home_list = [
    {
        'title': 'About',
        'content': 'SamplesAbyss is an attempt to resurrect (or at least reincarnate) the old website of samples.sloth org.',
    },
    {
        'title': 'Stats',
        'content': 'Statistics about the page.',
    },
    {
        'title': 'TODO - in order',
        'content': 'Implement formatting for data. Implement breadcrumbs (how to fix it when on samples page?). Implement IMDB/Spotify/Discogs API. Fix data (compilations etc). Implement search function. Implement contribute function.',
    },
    {
        'title': 'Top-of-the-line',
        'content': 'I guess I could select top artist and top source here?',
    },
    {
        'title': 'Spotlight',
        'content': 'I guess I could spotlight an artist or source here? I could also do an "underdog" version?',
    },
    {
        'title': 'Latest addition',
        'content': 'Nothing to add here as of yet. Expand the database by adding date of addition and then query for last 5 entries here and show them in sample layout, I guess?',
    },
]

def home(request):
    context = {
        'posts': home_list,
    }
    return render(request, 'samples/home.html', context=context)

def browse(request):
    context = {
        'bands': BandInfo.objects.all()
    }
    return render(request, 'samples/browse.html', context=context)

def search(request):
    return render(request, 'samples/search.html')

def sample_search_view(request):
    # SampleInfo.objects.filter(text__contains='rain').filter(text__contains='tears')
    search_text = request.GET.get('search-sample')
    context = {
        'search_text': search_text
    }
    return render(request, 'samples/sample_search.html', context=context)

def song_search_view(request):
    search_text = request.GET.get('song-sample')
    context = {
        'search_text': search_text
    }
    return render(request, 'samples/song_search.html', context=context)

def get_artist_discogs(band):
    band = unquote(band)
    results = discogs_client.search(band, type='artist')[0]
    result_dict = {
        'discogs_id': results.id,
        'discogs_name': results.name,
        'discogs_img': results.images[0]['uri'] if results.images else '',
        'discogs_url': results.url,
        'discogs_releases': results.releases,
    }
    return result_dict

def get_artist_spotify(band_name):
    band_name = unquote(band_name)
    results = spotify_client.search(q='artist:' + band_name, type='artist')['artists']['items'][0]
    result_dict = {
        'spotify_id': results['id'],
        'spotify_name': results['name'],
        'spotify_img': results['images'][1]['url'] if results['images'] else '',
        'spotify_uri': results['uri'],
        'spotify_url': results['external_urls']['spotify'],
    }
    return result_dict

def get_artist_ytmusic(band_name):
    band_name = unquote(band_name)
    results = [res for res in ytMusic.search(band_name) if res['category'] == 'Artists'][0]
    result_dict = {
        'ytmusic_id': results['browseId'],
        'ytmusic_name': results['artist'],
        'ytmusic_img': results['thumbnails'][1]['url'],
        'ytmusic_url': 'https://music.youtube.com/channel/' + results['browseId'],
    }
    return result_dict

def get_album_discogs(album_name):
    album_name = unquote(album_name)
    result = discogs_client.search(album_name, type='release')[0]
    result_dict = {
        'discogs_id': result.id,
        'discogs_name': result.title,
        'discogs_img': result.images[0]['uri'],
        'discogs_url': result.url,
    }
    return result_dict

def get_album_spotify(album_name):
    album_name = unquote(album_name)
    result = spotify_client.search(album_name, type='album')['albums']['items'][0]
    result_dict = {
        'spotify_id': result['id'],
        'spotify_name': result['name'],
        'spotify_img': result['images'][1]['url'],
        'spotify_url': result['external_urls']['spotify'],
        'spotify_uri': result['uri'],
    }
    return result_dict

def get_album_ytmusic(album_name):
    album_name = unquote(album_name)
    result = [res for res in ytMusic.search(album_name, filter='albums', ignore_spelling=True)][0]
    url = ytMusic.get_album(result['browseId'])['audioPlaylistId']    
    result_dict = {
        'ytmusic_name': result['title'],
        'ytmusic_id': result['browseId'],
        'ytmusic_url': 'https://music.youtube.com/playlist?list=' + url,
        'ytmusic_img': result['thumbnails'][2]['url'],
    }
    return result_dict

def get_song_ytmusic(band, album, song):
    results = ytMusic.search(album, filter='albums', ignore_spelling=True)[0]
    tracks_info = ytMusic.get_album(results['browseId'])['tracks']
    song = [track for track in tracks_info if track['title'] == song][0]['videoId']
    return 'https://www.youtube.com/embed/' + song

def get_song_spotify(band, album, song):
    album_id = spotify_client.search(album, type='album')['albums']['items'][0]['id']
    tracks = spotify_client.album(album_id)['tracks']['items']
    track_info = [track for track in tracks if track['name'] == song][0]
    return 'https://open.spotify.com/embed/track/' + track_info['id']

def get_movie(movie):
    movie = unquote(movie)
    result = imdb_client.search_movie(movie)[0]
    result_dict = {
        'imdb_name': result['title'],
        'imdb_url': 'https://www.imdb.com/title/tt' + result.movieID,
        'imdb_img': result['full-size cover url'],
    }
    return result_dict

class BandListView(ListView):
    def get_queryset(self) -> QuerySet[Any]:
        letter = self.kwargs.get('letter')
        if letter == "#":
            letter = '[^a-zA-Z]'
        band_list = BandInfo.objects.filter(name__regex=f'^{letter}').order_by('name')
        return band_list
    
    def get_context_data(self):
        context = super().get_context_data()
        context['letter'] = self.kwargs.get('letter')
        return context

class AlbumListView(ListView):
    def get_queryset(self) -> QuerySet[Any]:
        band = urllib.parse.unquote(self.kwargs.get('band'))
        
        album_list = BandInfo.objects.filter(name=band).first().albuminfo_set.all()
        return album_list

    def get_context_data(self):
        context = super().get_context_data()
        band = self.kwargs.get('band')

        discogs_dict = get_artist_discogs(band)
        context.update(discogs_dict)
        spotify_dict = get_artist_spotify(band)
        context.update(spotify_dict)
        ytmusic_dict = get_artist_ytmusic(band)
        context.update(ytmusic_dict)

        context['band'] = band
        return context

class SongListView(ListView):
    def get_queryset(self) -> QuerySet[Any]:
        album = urllib.parse.unquote(self.kwargs.get('album'))
        song_list = AlbumInfo.objects.filter(name=album).first().songinfo_set.all()
        return song_list

    def get_context_data(self):
        context = super().get_context_data()
        album = self.kwargs.get('album')

        discogs_dict = get_album_discogs(album)
        context.update(discogs_dict)
        spotify_dict = get_album_spotify(album)
        context.update(spotify_dict)
        ytmusic_dict = get_album_ytmusic(album)
        context.update(ytmusic_dict)

        context['album'] = album
        return context

class SampleListView(ListView):
    def get_queryset(self) -> QuerySet[Any]:
        song = urllib.parse.unquote(self.kwargs.get('song'))
        sample_list = SongInfo.objects.filter(name=song).first().sampleinfo_set.all()
        return sample_list

    def get_context_data(self):
        context = super().get_context_data()
        song = self.kwargs.get('song')
        album = SongInfo.objects.filter(name=song).first().album.name
        band = SongInfo.objects.filter(name=song).first().album.band.name
        # context['ytmusic_url'] = get_song_ytmusic(band, album, song)
        context['spotify_url'] = get_song_spotify(band, album, song)

        context['song'] = song
        return context

class SourceSampleListView(ListView):
    template_name = 'samples/sourcesampleinfo_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        source = urllib.parse.unquote(self.kwargs.get('source'))
        source_list = SourceInfo.objects.filter(name=source).first().sampleinfo_set.all()
        return source_list

    def get_context_data(self):
        context = super().get_context_data()
        movie = self.kwargs.get('source')

        imdb_dict = get_movie(movie)
        print(movie)
        print(imdb_dict)
        context.update(imdb_dict)

        context['source'] = movie
        return context

class SourceListView(ListView):
    def get_queryset(self) -> QuerySet[Any]:
        letter = self.kwargs.get('letter')
        if letter == "#":
            letter = '[^a-zA-Z]'
        source_list = SourceInfo.objects.filter(name__regex=f'^{letter}').order_by('name')
        return source_list
    
    def get_context_data(self):
        context = super().get_context_data()
        context['letter'] = self.kwargs.get('letter')
        return context


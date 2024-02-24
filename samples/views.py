import urllib
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import BandInfo, AlbumInfo, SongInfo, SourceInfo
from django.views.generic import ListView

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

def contribute(request):
    return render(request, 'samples/contribute.html')

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
        context['band'] = self.kwargs.get('band')
        return context

class SongListView(ListView):
    def get_queryset(self) -> QuerySet[Any]:
        album = urllib.parse.unquote(self.kwargs.get('album'))
        song_list = AlbumInfo.objects.filter(name=album).first().songinfo_set.all()
        return song_list

    def get_context_data(self):
        context = super().get_context_data()
        context['album'] = self.kwargs.get('album')
        return context

class SampleListView(ListView):
    def get_queryset(self) -> QuerySet[Any]:
        song = urllib.parse.unquote(self.kwargs.get('song'))
        sample_list = SongInfo.objects.filter(name=song).first().sampleinfo_set.all()
        return sample_list

    def get_context_data(self):
        context = super().get_context_data()
        context['song'] = self.kwargs.get('song')
        return context

class SourceListView(ListView):
    template_name = 'samples/sourceinfo_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        source = urllib.parse.unquote(self.kwargs.get('source'))
        source_list = SourceInfo.objects.filter(name=source).first().sampleinfo_set.all()
        return source_list

    def get_context_data(self):
        context = super().get_context_data()
        context['source'] = self.kwargs.get('source')
        return context


# SamplesAbyss

Django project to build a website for browsing/searching/contributing to database of samples in music

## Deployment

Project uses poetry for dependency management. In addition I am also using conda for env management. Steps to set up both are:

Installation steps
```
# create a directory to install minicaonda in
mkdir -p ~/miniconda3
# download latest miniconda version
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
# run the install script
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
# delete the intall script
rm -rf ~/miniconda3/miniconda.sh
# add a conda initialize to your bash
~/miniconda3/bin/conda init bash
# Verify the installaton 
conda list
# Install poetry
curl -sSL https://install.python-poetry.org | python3 - --version 1.2.2
```

Project setup steps
```
# Create conda environment
conda create -y -n SamplesAbyss python=3.11
# Activate environment
conda activate SamplesAbyss
# Cd to project folder that holds poetry.lock (assuming in home)
cd ~/SamplesAbyss
# Install requirements using poetry
poetry install
```

Running the server
```
python manage.py runserver
```

## Concept

The website will, at the start, offer three functionality:
1. Browsing (by band and source)
2. Searching
3. Contributing

During the setup of stages, below, browsing should be implemented at minimum. Stage 11 offers the way
to implement contribution, both for adding new and correcting old. 

### Display

#### Band page

Division of about 1:2 or 1:3
Left side:
    logo and various band links (spotify, youtube, wiki, homepage, social, discogs)
Right side:
    albums in format of cover above, name and year below, sorted by year descending
    both cover and name link to album page
    albums with samples identified with border?

#### Album page

Division of about 1:2 or 1:3
Left side:
    cover and various album links (spotify, youtube, wiki, discogs)
Right side:
    list of songs linking to song page
    songs with samples identified with border or an icon?

#### Song page

Division of about 1:2 or 1:3
Left side:
    album cover and various song links (spotify, youtube)
Right side:
    list of samples and sources
    source links to source page
    Collate the samples per source or list sequentially?

#### Source page

Division of about 1:2 or 1:3
Left side:
    cover and various song links (IMDB, wiki)
Right side:
    Tree of band-album-song links
(I don't think I should list the samples here)

#### Browse page

Grid layout - 4 columns finishing on 3.

### API

Spotify, discogs and IMDB API will be used that I know of exist.
Youtube and wiki API I need to check.
Socials will need to be added automatically.

## Stages

Stages according to the tutorial by Corey Shafer: https://www.youtube.com/watch?v=UmljXZIypDc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

### Stage 1: Django setup

Nothing special is done apart from setting up django, conda environment, this readme etc.

### Stage 2: Aplication and routes

Samples application will be added as well as some default routes (landing page, search, browse, contribute pages).

### Stage 3: Templates

Pages will be worked out in more detail here. ~~At this point the page should be mostly functional.~~
At this point I will have a basic layout and alphabet part of browse section. Search section needs the
db to be integrated. Contribute will be implemented last. For both contribute and search I need forms,
which happens at login part.

### Stage 4: Admin page

Nothing here, apart from checking how I can access the samples database from the admin page.

### Stage 5: Database and migration

Samples database will be migrated/created in this step. Corey implements blog functionality at this step, so I have to
implement the sample source functionality as well, and I have to supply with some samples. As the db is quite large,
instead of manually transferring, I will use two databases: one for django functionality (default), the other for samples.

### Stage 6: User registration

This will be skipped for now, as no user registration will be done. In the future, Google SSO will be offered.
Correct on Google SSO offering, but I can use this logic to create a search and contribute fields here.

### Stage 7: Login and logout system

This will be skipped for now, as no user registration will be done. In the future, Google SSO will be offered.
Correct on Google SSO offering, but I can use this logic to create a search and contribute fields here.

### Stage 8: User profile and picture

This will be skipped for now, as no user registration will be done. In the future, Google SSO will be offered.
Correct on Google SSO offering, but I can use this logic to create specific pages for letters, etc, instead of manually
creating them. Specifically, I think this part holds the flexible URL that can be used to generate letter-band-album... pages.

### Stage 9: Update user profile

This will be skipped for now, as no user registration will be done. In the future, Google SSO will be offered.

### Stage 10: Create, update and delete posts

Contribute page and functionality will be worked at here.

### Stage 11: Pagination

This will be important to add for browsing, as there is a large number of entries. However, instead of pagination
I will look into alphabetical pagination for bands. When a band is selected a simple list will suffice. Likewise for
the song list on a specific album and samples on a song.

### Stage 12: Email and password reset

This will be skipped for now, as no user registration will be done. In the future, Google SSO will be offered.

### Stage 13: Deployment

The rest will be done off-github, to deploy the page.

### Extra 14: Band/Album/Song redesign

The layout will be redone using the design description above. At this stage this will be a placeholder with dummy data.

### Extra 15: Source page

Browse either needs to have sources added as second alphabet-grid or split into Browse bands + Browse sources.

### Extra 15: API support

API calls will be added to call to Discogs, Spotify, IMDB, YouTubeMusic. The calls will return links and thumbnails.
Along with those APIs, YTM and Spotify embeds will be added for songs.
In addition, a default error image and message will be generated.

### Extra 16: DB redesign

DB will be redesigned to hold additional columns. In first commit columns will be added, in the next they will be populated.
1. Media url for thumbnails stored locally
2. Urls for respective sites via API
3. Verified or legacy column (or both) to track verification of old samples
4. Move timestamp_source to sample_info table

In addition, after adding verification column, an indicator will need to be added to track and show that on the page.

### Extra 17: Search

Search will be constrained only to search samples.
The idea is to split the search string into chained filters. There could be issues with that and order of search returns.

### Extra 18: Contribute

Contribute part needs to have three functionality:
1. API calls to verify the band/album/source
2. Interactive dropdowns when one stage is selected
3. Ability to search for a song by a band and list of albums who have that song are offered.

### Extra 19: SSO

In addition to SSO enable tracking of activity and a sort of credibility rating. Don't sweat profiles.

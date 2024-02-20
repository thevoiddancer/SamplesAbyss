# SamplesAbyss

Django project to build a website for browsing/searching/contributing to database of samples in music

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

#### Source page

Division of about 1:2 or 1:3
Left side:
    cover and various song links (IMDB, wiki)
Right side:
    Tree of band-album-song links
(I don't think I should list the samples here)

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
Potentially database will be migrated in this step. Corey implements blog functionality at this step, so I have to
implement the sample source functionality as well, and I have to supply with some samples. As the db is quite large,
instead of manually transferring, I will use two databases: one for django functionality (default), the other for samples.

### Stage 3: Templates

Pages will be worked out in more detail here. At this point the page should be mostly functional

### Stage 4: Admin page

Nothing here, apart from checking how I can access the samples database from the admin page.

### Stage 5: Database and migration

Usually I would create the samples db here, but as I think we needed some for stage 2, the job will already be handled there.

### Stage 6: User registration

This will be skipped for now, as no user registration will be done. In the future, Google SSO will be offered.

### Stage 7: Login and logout system

This will be skipped for now, as no user registration will be done. In the future, Google SSO will be offered.

### Stage 8: User profile and picture

This will be skipped for now, as no user registration will be done. In the future, Google SSO will be offered.

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
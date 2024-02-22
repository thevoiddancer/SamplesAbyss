from django.db import models

class BandInfo(models.Model):
    name = models.CharField(blank=True, null=True, max_length=300)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'band_info'


class AlbumInfo(models.Model):
    name = models.CharField(blank=True, null=True, max_length=300)
    band = models.ForeignKey('BandInfo', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'album_info'
        unique_together = (('name', 'band'),)


class SongInfo(models.Model):
    name = models.CharField(blank=True, null=True, max_length=300)
    album = models.ForeignKey(AlbumInfo, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'song_info'
        unique_together = (('name', 'album'),)


class SampleInfo(models.Model):
    text = models.TextField(blank=True, null=True)
    song = models.ForeignKey('SongInfo', models.DO_NOTHING, blank=True, null=True)
    source = models.ForeignKey('SourceInfo', models.DO_NOTHING, blank=True, null=True)
    timestamp_song = models.TimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sample_info'


class SourceInfo(models.Model):
    name = models.CharField(blank=True, null=True, max_length=300)
    timestamp_source = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_info'

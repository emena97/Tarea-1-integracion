from django.db import models


class Episode(models.Model):
    episode_id = models.IntegerField()
    title = models.CharField(max_length=300)
    season = models.CharField(max_length=5)
    episode_number = models.IntegerField()
    air_date = models.CharField(max_length=50)
    characters = models.JSONField(default=list,blank=True, null=True)
    series = models.CharField(max_length=5)


class Character(models.Model):
    character_id = models.IntegerField()
    name = models.CharField(max_length=100)
    ocuppation = models.JSONField(default=list, blank=True, null=True)
    img = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    nickname = models.CharField(max_length=70)
    bb_appearances = models.JSONField(default=list, blank=True, null=True)
    bcs_appearances = models.JSONField(default=list, blank=True, null=True)
    actor_portrayed = models.CharField(max_length=100)
    category = models.JSONField(default=list, blank=True, null=True)


class Quote(models.Model):
    quote_id = models.IntegerField()
    quote = models.CharField(max_length=400)
    author = models.ForeignKey(Character, on_delete=models.CASCADE)
    series = models.CharField(max_length=100)



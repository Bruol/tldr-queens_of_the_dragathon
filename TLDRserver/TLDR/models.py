from django.db import models


# Create your models here.

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=200)
    lecture_number = models.CharField(max_length=11)
    department = models.CharField(max_length=10)
    semester = models.CharField(max_length=2)


class Video(models.Model):
    presentation_date = models.DateField()
    infered_titel = models.CharField(max_length=100)
    presenters = models.TextField()
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    topics = models.ManyToManyField("Topic", related_name = "discussed_in")
    transcript = models.TextField()
    source_url = models.URLField()

class Topic(models.Model):
    title = models.CharField(max_length=100)
    bulletpoints = models.TextField()
    summary = models.TextField()
    chunk1 = models.TextField()
    chunk2 = models.TextField()
    chunk3 = models.TextField()
    tags = models.ManyToManyField("Tag", related_name = "topics")

class Tag(models.Model):
    name = models.CharField(max_length=100)

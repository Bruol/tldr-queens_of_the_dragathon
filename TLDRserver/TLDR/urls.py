from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("classes/<int:class_id>/", views.videos, name="class_index"),
    path("transcripts/<int:summary_id>/", views.summary, name="summary"),
]

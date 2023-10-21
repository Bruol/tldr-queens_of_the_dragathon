from TLDR.models import *
from django.db.models import Count

import os 
import json

dir = "../transcription/transcripts/"


def populate_lectures():
    for lecture_folder in os.listdir(dir):
        if not lecture_folder.startswith("."):
            meta_data = json.load(open(dir + lecture_folder + "/metadata.json"))
            
            print("writing to database lecture: "  + meta_data["name"])

            lecture = Lecture()

            lecture.lecture_name = meta_data["name"]
            lecture.lecture_number = meta_data["CourseNumber"]
            lecture.department = meta_data["Department"]
            lecture.semester = meta_data["Semester"]
            lecture.save()

            print("lecture saved")

def populate_videos():
    print("populating videos")

def populate_topics():
    print("populating topics")

def delete_duplicates():

    # delete duplicate lectures

    duplicate_lecs = Lecture.objects.values('lecture_number').annotate(lecture_number_count=Count('lecture_number')).filter(lecture_number_count__gt=1)

    for lec in duplicate_lecs:
        lec_num = lec['lecture_number']
        lecs_to_delete = Lecture.objects.filter(lecture_number=lec_num).order_by('pk')[1:]
        for  d_lec in lecs_to_delete:
            print("deleting lecture: " + d_lec.lecture_name)
            d_lec.delete()
    



delete_duplicates()
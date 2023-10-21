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
    vid_dir = "../transcription/jsons/"


    for js in os.listdir(vid_dir):
        data = json.load(open(vid_dir + js))
        video = Video()
        video.infered_titel = data["lecture_title"]

        lecture_folder = js[:2]
        
        meta_data = json.load(open(dir + lecture_folder + "/metadata.json"))

        video.source_url = meta_data["URL"]
        video.presentation_date = js[3:-5]
        
        pres = ""
        for lecturer in meta_data["Lecturer"]:
            pres = pres+lecturer+"; "

        video.presenters = pres

        ln = meta_data["CourseNumber"]

        video.lecture_id = Lecture.objects.filter(lecture_number=ln).first()

        video.save()
        for t in data["topics"]:
            top = Topic()
            top.title = t[0]
            top.bulletpoints = t[1]
            top.summary = t[2]

            length = len(t[3])
            if (length > 0):
                top.chunk1 = data["chunks"][int(t[3][0])]
            if (length > 1):
                top.chunk2 = data["chunks"][int(t[3][1])]
            if (length > 2):
                top.chunk3 = data["chunks"][int(t[3][2])]

            top.save()
            video.topics.add(top)

        with open ("../transcription/transcripts/" + js[:2] + "/transcripts/" + js[:-5] + ".txt", "r") as f:
            file = f.read()

        video.transcript = file
        video.save()




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
    
def delete_database():
    Lecture.objects.all().delete()
    Video.objects.all().delete()
    Topic.objects.all().delete()

populate_lectures()
populate_videos()
# delete_duplicates()

# delete_database()
from TLDR.models import *
import os 
import json

dir = "../transcription/transcripts/"


def popuiate_lectures():
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


def delete_duplicates():
    lectures = Lecture.objects.all()
    
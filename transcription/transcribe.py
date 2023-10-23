import os
import re
import subprocess

shorthand = "cg"

lang = "en"

mp4dir = "./lectureRecordings/" + shorthand 
wavdir = "./lectureRecordings/" + shorthand + "-wav"
txtdir = "./lectureRecordings/" + shorthand + "-txt"

def rename_files():
    pattern = "_.*(?=.mp4)"

    for filename in os.listdir(mp4dir):
        new_filename = re.sub(pattern, "", filename)
        new_filename = "ep_" + new_filename 
        os.rename(os.path.join(mp4dir, filename), os.path.join(mp4dir, new_filename))


def create_wav_files():


    for filename in os.listdir(mp4dir):
        wav_filename = filename.replace(".mp4", ".wav")
        os.system("ffmpeg -i " + os.path.join(mp4dir,filename) + " -acodec pcm_s16le -ar 16000 -ac 2 " + os.path.join(wavdir,wav_filename))


def transcribe():
    whisper_ex =  "../whisper.cpp/main "
    arguments = "-m ../whisper.cpp/models/ggml-small.bin -l " + lang + "  -f "


    for file in os.listdir(wavdir):
        command = (whisper_ex + arguments + os.path.join(wavdir, file))
        res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)

        filename = os.path.join(txtdir, file.replace(".wav.txt", ".txt"))

        with open(filename , "w") as f:
            f.write(res.stdout)



def extract_txt_files():
    for file in os.listdir(wavdir):
        if file.endswith(".txt"):
            newfile = file.replace(".wav.txt", ".txt")
            os.rename(os.path.join(wavdir, file), os.path.join(txtdir, newfile))

if __name__ == "__main__":
    # rename_files()
    # create_wav_files()
    transcribe()
    # extract_txt_files()

import openai
import os
import re
import json

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

apikey = os.environ.get("OPENAI_API_KEY")

def count_tokens(filename):

    # Read the file
    with open(filename, "r") as f:
        text = f.read()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Return the total token count
    return len(tokens)

def break_up_tokens(tokens, chunk_size, overlap_size):
    if len(tokens) <= chunk_size:
        yield tokens
    else:
        chunk = tokens[:chunk_size]
        yield chunk
        yield from break_up_tokens(tokens[chunk_size-overlap_size:], chunk_size, overlap_size)

def break_up_file(fn, chunk_size=2000, overlap_size=200):
    with open(fn, 'r') as f:
        text = f.read()
    tokens = word_tokenize(text)
    return list(break_up_tokens(tokens, chunk_size, overlap_size))


def convert_to_detokenized_text(tokenized_text):
    prompt_text = " ".join(tokenized_text)
    prompt_text = prompt_text.replace(" 's", "'s")
    return prompt_text


def create_chunk_summaries(filename):
    prompt_response = []
    chunks = break_up_file(filename)

    for chunk in chunks:
        text_part = convert_to_detokenized_text(chunk)
        prompt_request = "Make a summary of the following lecture transcript excerpt. Format your response in markdown: " + text_part
        
        message = [
             {"role": "user", "content": prompt_request}
        ]
        
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
        )
    
        prompt_response.append(response["choices"][0]["message"]["content"].strip())
    
    print("Got all chunk summaries")

    return prompt_response



def get_chunks(infile="input.txt",outfile="output.txt"):

    print("trying to get chunks from file: " + infile)

    if os.path.exists(outfile):
        print("getting chunks from file")
        # read summary from file if it exists
        with open(outfile, 'r') as f:
            chunk_summaries = f.read()
        
        chunk_summaries = chunk_summaries.split("\n\n\n\n")

        # return summary
        return chunk_summaries
    else:

        print("chunk summaries dont exist yet thus get them from opanai")

        # get summary from openai api
        chunk_summaries = create_chunk_summaries(infile)

        # write summary to file
        with open(outfile, 'w') as f:
            i = 1
            for chunk in chunk_summaries:
                f.write("Summary " + str(i) + ":\n")
                f.write(chunk)
                f.write("\n\n\n\n")
                i += 1
        # return summary
        return chunk_summaries


def summarize_chunks(chunk_summaries,outfile,prompt):
    
    print("use chunks to create a summary of the lecture")
        
    if os.path.exists(outfile):
        # read summary from file if it exists
        with open(outfile, 'r') as f:
            lecture_summary = f.read()
        
    else:
        prompt_request = prompt + str(chunk_summaries)


        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt_request}
                ]
            )

        lecture_summary = response["choices"][0]["message"]["content"].strip()
        
        with open(outfile, "w") as f:
            f.write(lecture_summary)

    return lecture_summary


def generate_title(lecture_summary, outfile, prompt):

    if os.path.exists(outfile):
        
        print("use title from file")
        # read summary from file if it exists
        with open(outfile, 'r') as f:
            lecture_title = f.read()
        
        return lecture_title
    else:
                
        print("use lecture summary to create a title for the lecture")
        
        prompt_request = prompt + lecture_summary

        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt_request}
                ]
            )

        lecture_title = response["choices"][0]["message"]["content"].strip()

        with open(outfile, "w") as f:
            f.write(lecture_title)

        return lecture_title

def generate_tags(video_dict, prompt):
        print("use topic summary to create a tags the topics")
        
        
        for i in video_dict["topics"]:
            prompt_request = prompt + i[2]

            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt_request}
                    ]
                )
            # Create a new tuple with the updated values
            updated_i = i + (response["choices"][0]["message"]["content"].strip().split(","),)

            # Find the index of the old tuple in the list and replace it
            index = video_dict["topics"].index(i)
            video_dict["topics"][index] = updated_i
            print()
            print(video_dict["topics"][index])
            print()
            

        return video_dict

def remove_first_and_empty_lines(input_string):
    lines = input_string.split('\n')
    
    # Find the index of the first non-empty line after the first line
    for i, line in enumerate(lines[1:], start=1):
        if line.strip():
            break
    else:
        # Handle the case where there are no non-empty lines after the first line
        i = len(lines)
    
    # Join the lines and return the result
    return '\n'.join(lines[i:])


def strings_to_dict(lecture_title, chunks, summary):
    temp_topics = []
    topics = []

    sections = summary.split("# In-Depth Summaries")

    # Split the summary into sections
    short_topics = sections[0].split("\n## ")
    long_topics = sections[1].split("\n## ")


    # Iterate through each section, skipping the first one (Summary)
    for short_topic in short_topics[1:]:
        topic_title = short_topic.split("\n")[:3][0]

        matches = re.findall(r'Summary (\d+)', short_topic)
        sources = []
        for match in matches:
            for group in match:
                sources.append(group)
        temp = short_topic.split("\n")[3:]
        temp_topics.append((topic_title, '\n'.join(temp), sources))
        
    i = 0
    for long_topic in long_topics[1:]:
        long_topic = remove_first_and_empty_lines(long_topic)

        #try:
        # Add the topic to the topics list
        #except Exception as e:
        topics.append((temp_topics[i][0], temp_topics[i][1], long_topic, temp_topics[i][2]))
        i += 1

    # Create the dictionary
    lecture_dict = {
        "lecture_title": lecture_title,
        "chunks": chunks,
        "topics": topics
    }

    return lecture_dict
    
if __name__ == "__main__":

    root_dir = "./transcripts"

    with open("../Prompts/Summary_prompt.txt", "r") as f:
        summary_prompt = f.read()
    
    with open("../Prompts/Title_prompt.txt", "r") as f:
        title_prompt = f.read()
    
    with open("../Prompts/Tags_prompt.txt", "r") as f:
        tags_prompt = f.read()

    transcript_files = []
        
    for dir in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir,dir)):
            cur_dir = os.path.join(root_dir,dir)
            for file in os.listdir(os.path.join(cur_dir, "transcripts")):
                if file.endswith(".txt"):
                    infile = os.path.join(cur_dir, "transcripts", file)
                    chunkfile = os.path.join(cur_dir, "chunks", file.replace(".txt", "_chunks.txt"))
                    outfile = os.path.join(cur_dir, "summaries", file.replace(".txt", "_summary.txt"))

                    tr = [infile, chunkfile, outfile, dir]

                    transcript_files.append(tr)
    

    jsons = []

    for i in range(0,len(transcript_files)):
        tr = transcript_files[i]

        print("processing file number: " + str(i) + "\n")

        infile = tr[0]
        chunkfile = tr[1]
        outfile = tr[2]
        filename = infile.split("/")[-1][:-4] + ".json"

        outfile_title = tr[2].replace("_summary.txt", "_title.txt")

        chunk_summaries = get_chunks(infile, chunkfile)

        lecture_summary = summarize_chunks(chunk_summaries, outfile, summary_prompt)   

        lecture_title = generate_title(lecture_summary, outfile_title, title_prompt)
        video_dict = strings_to_dict(lecture_title, chunk_summaries, lecture_summary)

        video_dict = generate_tags(video_dict, tags_prompt)

        # write dict to json
        with open("jsons/" + filename, 'w') as json_file:
            json.dump(video_dict, json_file)


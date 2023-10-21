
import openai
import os

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

    
if __name__ == "__main__":

    root_dir = "./transcripts"

    with open("../Prompts/Summary_prompt.txt", "r") as f:
        summary_prompt = f.read()
    
    with open("../Prompts/Title_prompt.txt", "r") as f:
        title_prompt = f.read()

    transcript_files = []
        
    for dir in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir,dir)):
            cur_dir = os.path.join(root_dir,dir)
            for file in os.listdir(os.path.join(cur_dir, "transcripts")):
                if file.endswith(".txt"):
                    infile = os.path.join(cur_dir, "transcripts", file)
                    chunkfile = os.path.join(cur_dir, "chunks", file.replace(".txt", "_chunks.txt"))
                    outfile = os.path.join(cur_dir, "summaries", file.replace(".txt", "_summary.txt"))

                    tr = [infile, chunkfile, outfile]

                    transcript_files.append(tr)

    print(transcript_files)
    

    for i in range(0,len(transcript_files)):
        tr = transcript_files[i]

        print("processing file number: " + str(i) + "\n")

        infile = tr[0]
        chunkfile = tr[1]
        outfile = tr[2]
        outfile_title = tr[2].replace("_summary.txt", "_title.txt")

        chunk_summaries = get_chunks(infile, chunkfile)

        lecture_summary = summarize_chunks(chunk_summaries, outfile, summary_prompt)   

        lecture_title = generate_title(lecture_summary, outfile_title, title_prompt)


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

def break_up_file(fn, chunk_size=2000, overlap_size=100):
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
        prompt_request = "Summarize this lecture transcript and return it in markdown format: " + text_part
        
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

    print("Getting chunks from file: " + infile)

    if os.path.exists(outfile):
        # read summary from file if it exists
        with open(outfile, 'r') as f:
            chunk_summaries = f.read()
        
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
                f.write("\n\n")
                i += 1
        # return summary
        return chunk_summaries


def summarize_chunks(chunk_summaries,outfile):
    
    if os.path.exists(outfile):
        # read summary from file if it exists
        with open(outfile, 'r') as f:
            lecture_summary = f.read()
        
    else:
        prompt_request = "Using the following summaries of different parts of a lecture that together comprise the entire lecture, make a summary that lists the 3-5 main topics along with short key take-aways from those topics. Add subtopics with their own short key take-aways when reasonable.  For each topic: mention from which summary number the information was sourced. \n Finish your response with another section with in depth summaries for each of the topics. Format your response in markdown" + str(chunk_summaries)


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



if __name__ == "__main__":

    #root_dir = "./transcripts"

    transcript_files = []
        
    for dir in os.listdir(root_dir):
        if os.path.isdir(os.path.join(root_dir,dir)):
            cur_dir = os.path.join(root_dir,dir)
            for file in os.listdir(os.path.join(cur_dir, "transcripts")):
                infile = os.path.join(cur_dir, "transcripts", file)
                chunkfile = os.path.join(cur_dir, "chunks", file.replace(".txt", "_chunks.txt"))
                outfile = os.path.join(cur_dir, "summaries", file.replace(".txt", "_summary.txt"))

                tr = [infile, chunkfile, outfile]

                transcript_files.append(tr)


    for tr in transcript_files:
        infile = tr[0]
        chunkfile = tr[1]
        outfile = tr[2]

        chunk_summaries = get_chunks(infile, chunkfile)

        lecture_summary = summarize_chunks(chunk_summaries, outfile)

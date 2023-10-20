
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
    return prompt_response



def get_chunks(infile="input.txt",outfile="output.txt"):

    if os.path.exists(outfile):
        # read summary from file if it exists
        with open(outfile, 'r') as f:
            chunk_summaries = f.read()
        
        # return summary
        return chunk_summaries
    else:
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


if __name__ == "__main__":

    chunk_summaries = get_chunks()

    prompt_request = "Using the 6 following summaries of 6 different non-overlapping parts of a lecture that together comprise the entire lecture, make a summary that lists the 3-5 main topics along with short key take-aways from those topics. Add subtopics with their own short key take-aways when reasonable.  For each topic: mention from which summary number the information was sourced. \n Finish your response with another section with in depth summaries for each of the topics. Format your response in markdown." + str(chunk_summaries)


    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt_request}
            ]
        )

    meeting_summary = response["choices"][0]["message"]["content"].strip()
    print(meeting_summary)

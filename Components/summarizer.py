import re
from Components.constants import *
from Components.transcript import *
from transformers import AutoTokenizer, pipeline

# Clean Text Function
def clean_text(text):
    text = re.sub(r'[^\x00-\x7F]+'," ", text)
    text = re.sub(r'\n+',' ', text)
    text = re.sub(r'\s+',' ',text).strip()
    return text

# Split text into chunks
def split_text_into_chunks(text, max_tokens=MAX_TOKENS):
    tokenizer = AutoTokenizer.from_pretrained(LLM)
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk) for chunk in chunks]

# Summarize Text Function using Facebook LLM via Hugging Face
def summarize_text(transcript, summarizer_pipeline):
    """
    Summarizes the provided transcript using the BART model.

    Parameters:
    - transcript (str): The video transcript to summarize.

    Returns:
    - summary (str): The summarized text or an error message.
    """
    try:
        # Split the text into chunks
        t = clean_text(transcript)
        chunks = split_text_into_chunks(t)

        # Summarize each chunk
        summaries = [summarizer_pipeline(chunk, max_length=140, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]

        # Combine the summaries if needed
        result = " ".join(summaries)

        if len(result) > 0:
            return result
        else:
            return "No summarizable text found in the provided transcript."
    except Exception as e:
        # Return an error message in case of failure
        return f"Error summarizing transcript: {e}"

# Summarize the transcripts in the DataFrame
def generate_summaries(videos_df):
    """
    Iterates over each video's transcript and generates summaries using the provided summarizer.

    Parameters:
    - videos_df (DataFrame): The DataFrame containing videos with transcripts.

    Returns:
    - videos_df (DataFrame): The updated DataFrame with summaries.
    """
    summarizer_pipeline = pipeline('summarization', model=LLM)

    # Initialize a new column for summaries
    videos_df['Summary'] = None

    # Iterate over each transcript and generate summaries
    for index, row in videos_df.iterrows():
        transcript = row['Transcript']
        video_title = row['Title']
        
        if transcript and 'transcripts are disabled' not in transcript.lower() and 'no transcript found' not in transcript.lower():
            print(f'Summarizing transcript for video: {video_title}')
            try:
                summary = summarize_text(transcript, summarizer_pipeline)
                videos_df.at[index, 'Summary'] = summary
                print(f'Summary generated for video: {video_title}')
            except Exception as e:
                print(f'Error summarizing transcript for video: {video_title}, Error: {str(e)}')
                videos_df.at[index, 'Summary'] = f'Error summarizing transcript: {str(e)}'
        else:
            print(f'No valid transcript found for video: {video_title}. Skipping summarization.')
            videos_df.at[index, 'Summary'] = 'No transcript found for this video.'

    return videos_df

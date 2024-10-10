# Components/transcript.py

import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import streamlit as st  # Import Streamlit for displaying messages

def extract_video_id(youtube_url):
    """
    Extracts the video ID from a YouTube URL.
    """
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", youtube_url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        return None

def extract_transcripts(videos_df):
    """
    Extracts transcripts for each video in the DataFrame.
    """
    # Initialize a new column for transcripts
    videos_df['Transcript'] = None

    # Iterate over each video and fetch the transcript
    for index, row in videos_df.iterrows():
        youtube_url = row['Link']
        video_title = row['Title']
        video_id = extract_video_id(youtube_url)

        if video_id:
            try:
                # Fetch the transcript using the video ID
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                
                # Combine the transcript segments into a single string
                transcript = ' '.join([segment['text'] for segment in transcript_list])
                
                # Assign the transcript to the DataFrame
                videos_df.at[index, 'Transcript'] = transcript

                # Debug message
                st.write(f"✅ Transcript extracted for video: **{video_title}**")

            except TranscriptsDisabled:
                st.write(f"⚠️ Transcripts are disabled for this video: **{video_title}**.")
                videos_df.at[index, 'Transcript'] = "Transcripts are disabled for this video."
                
            except NoTranscriptFound:
                st.write(f"⚠️ No transcript found for this video: **{video_title}**.")
                videos_df.at[index, 'Transcript'] = "No transcript found for this video."
                
            except Exception as e:
                st.write(f"❌ An error occurred while fetching transcript for **{video_title}**: {str(e)}")
                videos_df.at[index, 'Transcript'] = "Error occurred while fetching transcript."
        else:
            st.write(f"❌ Invalid YouTube URL for video: **{video_title}**.")
            videos_df.at[index, 'Transcript'] = "Invalid YouTube URL."

    return videos_df

# streamlit_app.py

import streamlit as st
import pandas as pd
from Components.constants import DESTINATION, PREFERENCES, MAX_RESULTS, MIN_VIEWS, LLM
from Components.youtube_search import fetch_youtube_videos
from Components.transcript import extract_transcripts
from Components.summarizer import generate_summaries
from Components.DPR import encode_passage, faiss_vector_store, search_relevant_passages
from Components.agent import generate_question
import faiss
import torch
import ollama  # Ensure ollama is imported for LLM interactions

# Initialize FAISS and DPR only once using Streamlit's caching
@st.cache_resource
def initialize_dpr(videos_df):
    if videos_df.empty:
        return None
    passage_embeddings = encode_passage(videos_df)
    faiss_index = faiss_vector_store(passage_embeddings)
    return faiss_index

# Function to generate LLM response
def generate_llm_response(query, context):
    prompt = f"""
You are a helpful travel guide assistant. Based on the following information, answer the question below.

### Context:
{context}

### Question:
{query}

### Answer:
"""
    try:
        response = ollama.chat(model="llama3.1:8b", messages=[{'role':'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    st.set_page_config(page_title="Travel Guide Video Summarizer", layout="wide")
    st.title("🌍 Travel Guide Video Summarizer")

    # Initialize session state for chat history, videos_df, faiss, and generated_questions
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'videos_df' not in st.session_state:
        st.session_state['videos_df'] = pd.DataFrame()
    if 'faiss_initialized' not in st.session_state:
        st.session_state['faiss_initialized'] = False
    if 'generated_questions' not in st.session_state:
        st.session_state['generated_questions'] = ""

    st.sidebar.header("Customize Your Search")

    # User Inputs
    destination = st.sidebar.text_input("Enter travel destination:", DESTINATION)
    preferences = st.sidebar.multiselect("Select your preferences:", PREFERENCES, default=PREFERENCES)
    min_views = st.sidebar.number_input("Minimum Views:", min_value=0, value=MIN_VIEWS, step=1000)
    max_results = st.sidebar.number_input("Maximum Results:", min_value=1, max_value=50, value=MAX_RESULTS, step=1)

    # Optional: Load Test Video
    if st.sidebar.button("Load Test Video"):
        test_videos = [{
            'Title': 'Amsterdam Travel Guide | Top 10 Attractions',
            'Duration': '15:30',
            'Views': 250000,
            'Channel': 'TravelWithMe',
            'Link': 'https://www.youtube.com/watch?v=abcd1234EFG'  # Replace with a valid video ID that has a transcript
        }]
        st.session_state['videos_df'] = pd.DataFrame(test_videos)
        st.markdown("### Test Video Loaded:")
        for idx, row in st.session_state['videos_df'].iterrows():
            st.markdown(f"**{idx + 1}. {row['Title']}**")
            st.markdown(f"Duration: {row['Duration']} | Views: {row['Views']} | Channel: {row['Channel']}")
            st.markdown(f"[Watch Video]({row['Link']})")
            st.markdown("---")

    # Fetch Videos
    if st.sidebar.button("Fetch Videos"):
        if destination and preferences:
            with st.spinner("Fetching YouTube videos..."):
                videos = fetch_youtube_videos(destination, preferences, min_views, max_results)
            
            if videos:
                st.success(f"✅ Found {len(videos)} videos with more than {min_views} views.")
                st.session_state['videos_df'] = pd.DataFrame(videos)
                
                st.markdown("### Fetched Videos:")
                st.markdown("**Note:** Click on 'Watch Video' to view the video.")
                for idx, row in st.session_state['videos_df'].iterrows():
                    st.markdown(f"**{idx + 1}. {row['Title']}**")
                    st.markdown(f"Duration: {row['Duration']} | Views: {row['Views']} | Channel: {row['Channel']}")
                    st.markdown(f"[Watch Video]({row['Link']})")
                    st.markdown("---")
            else:
                st.warning("⚠️ No videos found with the given criteria.")
        else:
            st.error("❗ Please enter a destination and select at least one preference.")

    # Extract Transcripts
    if not st.session_state['videos_df'].empty:
        if st.button("Extract Transcripts"):
            with st.spinner("Extracting transcripts..."):
                st.session_state['videos_df'] = extract_transcripts(st.session_state['videos_df'])
            st.success("✅ Transcripts extracted.")
            
            st.markdown("### Videos with Transcripts:")
            for idx, row in st.session_state['videos_df'].iterrows():
                st.markdown(f"**{idx + 1}. {row['Title']}**")
                st.markdown(f"Transcript: {row['Transcript']}")
                st.markdown("---")

    # Generate Summaries
    if not st.session_state['videos_df'].empty and 'Transcript' in st.session_state['videos_df'].columns:
        if st.button("Generate Summaries"):
            with st.spinner("Generating summaries..."):
                st.session_state['videos_df'] = generate_summaries(st.session_state['videos_df'])
            st.success("✅ Summaries generated.")
            
            st.markdown("### Videos with Summaries:")
            for idx, row in st.session_state['videos_df'].iterrows():
                st.markdown(f"**{idx + 1}. {row['Title']}**")
                st.markdown(f"Summary: {row['Summary']}")
                st.markdown("---")

    # Initialize DPR
    if not st.session_state['videos_df'].empty and 'Summary' in st.session_state['videos_df'].columns:
        if st.button("Initialize DPR"):
            with st.spinner("Encoding passages and initializing DPR..."):
                faiss_index = initialize_dpr(st.session_state['videos_df'])
            if faiss_index is not None:
                st.success("✅ DPR initialized.")
                st.session_state['faiss_initialized'] = True
                st.session_state['faiss_index'] = faiss_index  # Store FAISS index in session state
                st.write("FAISS Index has been initialized and is ready for chat.")
            else:
                st.error("❌ Failed to initialize DPR. DataFrame is empty or invalid.")

    # Generate Travel Questions using Agent
    if not st.session_state['videos_df'].empty and 'Summary' in st.session_state['videos_df'].columns:
        if st.button("Generate Travel Questions"):
            with st.spinner("Generating questions..."):
                questions = generate_question(destination)
            st.session_state['generated_questions'] = questions  # Store in session state
            st.success("✅ Questions generated.")
            st.markdown(f"### Top 10 Questions for First-Time Travelers to {destination}:")
            st.markdown(st.session_state['generated_questions'])
            st.markdown("---")  # Separator for clarity

    # Display Stored Generated Questions Persistently
    if st.session_state['generated_questions']:
        st.markdown(f"### Top 10 Questions for First-Time Travelers to {destination}:")
        st.markdown(st.session_state['generated_questions'])
        st.markdown("---")  # Separator for clarity

    # Chat Interface
    if not st.session_state['videos_df'].empty and 'Summary' in st.session_state['videos_df'].columns:
        st.header("💬 Chat with Travel Guide Assistant")

        # Input for user query
        user_query = st.text_input("Ask a question about your travel destination:")

        if st.button("Send") and user_query:
            if not st.session_state.get('faiss_initialized', False):
                st.error("❗ Please initialize DPR before using the chat.")
            else:
                with st.spinner("Generating response..."):
                    # Retrieve relevant passages using DPR
                    faiss_index = st.session_state.get('faiss_index', None)
                    if faiss_index is None:
                        st.error("❌ FAISS Index not available.")
                        return
                    top_k_videos = search_relevant_passages(
                        st.session_state['videos_df'], user_query, faiss_index, top_k=3
                    )
                    # Combine summaries as context
                    context = "\n".join(top_k_videos['Summary'].tolist())
                    # Generate response from LLM
                    llm_response = generate_llm_response(user_query, context)
                
                # Update chat history
                st.session_state['chat_history'].append({"user": user_query, "assistant": llm_response})
        
        # Display chat history
        if st.session_state['chat_history']:
            st.markdown("### Conversation:")
            for chat in st.session_state['chat_history']:
                st.markdown(f"**You:** {chat['user']}")
                st.markdown(f"**Assistant:** {chat['assistant']}")
                st.markdown("---")

    # Option to download the results
    if not st.session_state['videos_df'].empty:
        csv = st.session_state['videos_df'].to_csv(index=False)
        st.download_button("📥 Download Results as CSV", data=csv, file_name='summarized_videos.csv', mime='text/csv')

if __name__ == "__main__":
    main()









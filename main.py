# streamlit

import ollama  # Ensure Ollama is imported for LLM interactions
import warnings
import pandas as pd
import streamlit as st
from Components.constants import *
from Components.youtube_search import fetch_youtube_videos
from Components.transcript import extract_transcripts
from Components.summarizer import generate_summaries
from Components.DPR import encode_passage, faiss_vector_store, search_relevant_passages
from Components.agent import generate_question
from Components.itinerary import generate_itinerary  # Ensure this is correctly implemented

# Suppress all warnings
warnings.filterwarnings("ignore")

# Initialize FAISS and DPR only once using Streamlit's caching
@st.cache_resource
def initialize_dpr(videos_df):
    if videos_df.empty:
        return None
    passage_embeddings = encode_passage(videos_df)
    faiss_index = faiss_vector_store(passage_embeddings)
    return faiss_index

# Function to generate LLM response
def generate_llm_response(query, context, LLM = "llama3.2"):
    prompt = f"""
You are a helpful travel guide assistant. Based on the following information, answer the question below.

### Context:
{context}

### Question:
{query}

### Answer:
"""
    try:
        response = ollama.chat(model = LLM, messages=[{'role':'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error generating response: {e}"

def main():
    # Set Streamlit page configuration
    st.set_page_config(page_title="✈️ Travel Agent Video Summarizer with Ollama LLM's", layout="wide", page_icon="🌎")
    
    # Initialize session state for chat history, videos_df, faiss, generated_questions, and itinerary
        # Initialize session state for chat history, videos_df, faiss, generated_questions, and itinerary
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'videos_df' not in st.session_state:
        st.session_state['videos_df'] = pd.DataFrame()
    if 'faiss_initialized' not in st.session_state:
        st.session_state['faiss_initialized'] = False
    if 'generated_questions' not in st.session_state:
        st.session_state['generated_questions'] = []  # Initialize as a list
    if 'itinerary' not in st.session_state:
        st.session_state['itinerary'] = []  # Initialize as a list
    
    # Sidebar - Navigation Menu and Logo
    st.sidebar.image("./assets/logo.png")  # Display the logo in the sidebar
    menu = ["🏠 Home", "🤖 Travel Agent", "📧 Contact"]
    choice = st.sidebar.selectbox("Navigate", menu)
    
    # Home Page
    if choice == "🏠 Home":
        st.header("🚀 Travel Agent Video Summary Assistant (Ollama LLM's)")
        st.markdown("---")
        st.markdown("""
### **Welcome to the Travel Guide Video Summarizer!** 😊

**Discover, Transcribe, Summarize, and Interact with YouTube Travel Videos** tailored to your desired destinations within the Netherlands.

#### **What We Offer:**

- **🔍 Comprehensive Video Fetching:**  
  Retrieve a curated list of YouTube videos focused on your chosen destination and travel preferences.

- **📝 Automatic Transcription:**  
  Convert video audio into accurate text transcripts, making it easier to extract key information.

- **✂️ Concise Summarization:**  
  Generate clear and concise summaries from transcripts, highlighting essential travel tips and recommendations.

- **🤖 Interactive Travel Agent:**  
  Engage with our AI-powered travel assistant to ask personalized questions and receive tailored answers based on the video content.

- **📥 Downloadable Results:**  
  Export your data, including fetched videos, transcripts, summaries, and itineraries, for offline use and future reference.

#### **Built with an Open-Source Stack:**

- **FAISS for Efficient Retrieval:**  
  Quickly and accurately retrieve relevant video content based on your inputs.

- **Transformers & DPR for NLP Tasks:**  
  Utilize advanced natural language processing models to handle transcription and summarization.

- **Ollama LLM's for Intelligent Responses:**  
  Provide context-aware and intelligent responses through our language model integration.  
  LLMs include models like Llama3.2, Gemma9b, Mistral-Nemo, and Phi3.

Enhance your travel planning experience with our intelligent video summarizer and make your next trip to the unforgettable! 🚀              
---

""")

    # Travel Agent Page
    elif choice == "🤖 Travel Agent":
        st.title("🌎 Travel Agent: Your Video Summary Companion (Ollama LLM's)")

                # User Inputs (Still on main page for better UX)
        destination = st.text_input("**✈️ Enter travel destination:**", DESTINATION)

        # Update preferences based on selected destination
        preferences_list = DESTINATION_PREFERENCES.get(destination, DEFAULT_PREFERENCES)

        # Note for users
        st.markdown("**❕Note:** Please select preferences that are suitable for your chosen destination.")

        # Preferences input field
        preferences = st.multiselect("**✅ Select your preferences:**", preferences_list, default=preferences_list)

        min_views = st.number_input("**👀 Minimum Views:**", min_value=0, value=MIN_VIEWS, step=1000)
        max_results = st.number_input("**🔍 Maximum Results:**", min_value=1, max_value=50, value=MAX_RESULTS, step=1)

        budget = st.selectbox("**💵 Select your budget:**", BUDGET_OPTIONS)
        travel_style = st.selectbox("**💁 Select your travel style:**", TRAVEL_STYLE_OPTIONS)

        # **Moved Duration Input Outside the Button Click**
        duration = st.number_input(
            "**🗓️ Enter trip duration (in days):**",
            min_value=1,
            max_value=30,
            value=3,
            step=1,
            key='duration_input'  # Unique key to avoid conflicts
        )

        # Fetch Videos
        if st.sidebar.button("⚙️ Fetch Videos"):
            if destination and preferences:
                with st.spinner("⚙️ Fetching YouTube videos..."):
                    videos = fetch_youtube_videos(destination, preferences, min_views, max_results)

                if videos:
                    st.session_state['videos_df'] = pd.DataFrame(videos)
                    st.success(f"✅ Found {len(videos)} videos with more than {min_views} views.")

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
        if not st.session_state.get('videos_df', pd.DataFrame()).empty:
            if st.sidebar.button("🛠️ Extract Transcripts"):
                with st.spinner("🛠️ Extracting transcripts..."):
                    st.session_state['videos_df'] = extract_transcripts(st.session_state['videos_df'])
                st.success("✅ Transcripts extracted.")

                st.markdown("### Videos with Transcripts:")
                for idx, row in st.session_state['videos_df'].iterrows():
                    st.markdown(f"**{idx + 1}. {row['Title']}**")
                    st.markdown(f"Transcript: {row['Transcript']}")
                    st.markdown("---")

        # Generate Summaries
        if not st.session_state['videos_df'].empty and 'Transcript' in st.session_state['videos_df'].columns:
            if st.sidebar.button("📊 Generate Summaries"):
                with st.spinner("📊 Generating summaries..."):
                    # Initialize a progress bar
                    progress_bar = st.progress(0)

                    # Generate summaries for all videos
                    st.session_state['videos_df'] = generate_summaries(st.session_state['videos_df'])

                    # Update the progress bar to 100%
                    progress_bar.progress(1.0)
                st.success("✅ Summaries generated.")

                st.markdown("### Videos with Summaries:")
                for idx, row in st.session_state['videos_df'].iterrows():
                    st.markdown(f"**{idx + 1}. {row['Title']}**")
                    st.markdown(f"Summary: {row['Summary']}")
                    st.markdown("---")

        # Initialize DPR
        if not st.session_state['videos_df'].empty and 'Summary' in st.session_state['videos_df'].columns:
            if st.sidebar.button("🔧 Initialize DPR"):
                with st.spinner("🔧 Encoding passages and initializing DPR..."):
                    faiss_index = initialize_dpr(st.session_state['videos_df'])
                if faiss_index is not None:
                    st.session_state['faiss_initialized'] = True
                    st.session_state['faiss_index'] = faiss_index  # Store FAISS index in session state
                    st.success("✅ DPR initialized.")
                    st.write("FAISS Index has been initialized and is ready for chat.")
                else:
                    st.error("❌ Failed to initialize DPR. DataFrame is empty or invalid.")

        # Generate Travel Questions using Agent
        if not st.session_state['videos_df'].empty and 'Summary' in st.session_state['videos_df'].columns:
            if st.sidebar.button("💡 Generate Travel Questions"):
                with st.spinner("💡 Generating questions..."):
                    questions = generate_question(destination)
                st.session_state['generated_questions'].append(questions)  # Append to the list
                st.success("✅ Questions generated.")

        # Display Stored Generated Questions Persistently
        if st.session_state['generated_questions']:
            st.markdown(f"### Top 10 Questions for First-Time Travelers to {destination}:")
            for idx, question_set in enumerate(st.session_state['generated_questions'], 1):
                st.markdown(f"**Set {idx}:**")
                st.markdown(question_set)
            st.markdown("---")  # Separator for clarity

        # Generate Itinerary
        if not st.session_state['videos_df'].empty and 'Summary' in st.session_state['videos_df'].columns:
            if st.sidebar.button("🗓️ Generate Itinerary"):
                with st.spinner("🗓️ Generating itinerary..."):
                    itinerary = generate_itinerary(
                        st.session_state['videos_df'],
                        duration=int(duration),
                        budget=budget,
                        travel_style=travel_style
                    )
                st.session_state['itinerary'].append(itinerary)  # Append to the list
                st.success("✅ Itinerary generated.")

        # Display Stored Itineraries Persistently
        if st.session_state['itinerary']:
            st.markdown(f"### 🗓️ Your Itinerary for {destination}:")
            for idx, itin in enumerate(st.session_state['itinerary'], 1):
                st.markdown(f"**Itinerary {idx}:**")
                st.markdown(itin)
            st.markdown("---")  # Separator for clarity

            # **Download Itinerary**
            itinerary_text = "\n\n".join(st.session_state['itinerary'])
            st.download_button(
                "📥 Download Itinerary as Text",
                data=itinerary_text,
                file_name='itinerary.txt',
                mime='text/plain'
            )

        # Chat Interface
        if not st.session_state['videos_df'].empty and 'Summary' in st.session_state['videos_df'].columns:
            st.header("💬 Chat with Travel Guide Assistant")

            # Input for user query
            user_query = st.text_input("Ask a question about your travel destination:")

            if st.button("🛎️ Send") and user_query:
                if not st.session_state.get('faiss_initialized', False):
                    st.error("❗ Please initialize DPR before using the chat.")
                else:
                    with st.spinner("🛎️ Generating response..."):
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

                # Initialize chat history if not already done
                if 'chat_history' not in st.session_state:
                    st.session_state['chat_history'] = []

                # Update chat history
                st.session_state['chat_history'].append({"user": user_query, "assistant": llm_response})

        # Display chat history
        if st.session_state.get('chat_history'):
            st.markdown("### Conversation:")
            for chat in st.session_state['chat_history']:
                st.markdown(f"**You:** {chat['user']}")
                st.markdown(f"**Assistant:** {chat['assistant']}")
                st.markdown("---")

        # Option to download the results
        if not st.session_state['videos_df'].empty:
            csv = st.session_state['videos_df'].to_csv(index=False)
            st.download_button(
                "📥 Download Results as CSV",
                data=csv,
                file_name='summarized_videos.csv',
                mime='text/csv'
            )

    # Contact Page
    elif choice == "📧 Contact":
        st.title("📬 Contact Us")
        st.markdown("""
    We'd love to hear from you! Whether you have a question, feedback, or want to contribute, feel free to reach out.

    - **Email:** [pavun9848@gmail.com](mailto:pavun9848@gmail.com) ✉️
    - **GitHub:** [Contribute on GitHub](https://github.com/Pavun-KumarCH) 🛠️
    - **LinkedIn:** [Connect with us on LinkedIn](https://www.linkedin.com/in/pawan-kumar-ai-expert/) 💼
    
    If you'd like to request a feature, report a bug, or provide feedback, please open a pull request on our GitHub repository. Your contributions are highly appreciated! 🙌
    """)
    
    # Footer
    st.markdown("---")
    st.markdown("© 2024 Travel Guide Video Summarizer by Pavan Kumar CH. All rights reserved. 🛡️")

if __name__ == "__main__":
    main()

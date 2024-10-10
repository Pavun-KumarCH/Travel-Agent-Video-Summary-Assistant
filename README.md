# 🚀 Travel Agent Video Summary Assistant

## Overview

The **Travel Agent Video Summary Assistant** is an interactive tool that enhances your travel planning experience by summarizing YouTube travel videos. This application is designed to fetch, transcribe, and summarize travel-related video content, allowing users to access tailored information about their desired destinations. Built with Streamlit, the application enables seamless interaction, providing a user-friendly interface to discover travel videos, extract key insights, and generate personalized itineraries based on user preferences.

## Features

- **Video Fetching**:  
  Retrieve a curated list of YouTube videos based on user-defined destinations and preferences, making it easier to find relevant content that aligns with your travel interests.

- **Automatic Transcription**:  
  Convert video audio into accurate text transcripts with high fidelity, ensuring that no essential information is missed during the summarization process.

- **Concise Summarization**:  
  Generate clear and concise summaries from the transcripts, highlighting essential travel tips, recommendations, and notable attractions, so you can quickly grasp the highlights of each video.

- **Interactive Travel Agent**:  
  Engage with an AI-powered assistant that can answer your personalized travel queries based on the summarized video content, providing recommendations, insights, and additional details about your destination.

- **Downloadable Results**:  
  Export results, including fetched videos, transcripts, summaries, and personalized itineraries, in formats such as CSV and DOCX for offline use and future reference.

- **Itinerary Generation**:  
  Create a personalized travel itinerary based on video summaries and user preferences, including duration, budget, and travel style, to streamline your travel planning process.

- **User-Friendly Interface**:  
  A clean and intuitive interface built with Streamlit, ensuring that users can navigate through the application easily and access various features without hassle.

## Tech Stack

- **Frontend**: Streamlit for creating the web interface, providing an interactive experience for users.
  
- **Backend**: Python with libraries including:
  - `pandas` for data manipulation and handling DataFrames.
  - `python-docx` for generating Word documents to export itineraries and summaries.
  - `ollama` for integrating advanced language models to enhance responses.

- **NLP**: 
  - Transformers for accurate transcription and summarization of video content.
  - FAISS (Facebook AI Similarity Search) for efficient retrieval of relevant video content based on user queries.

- **Deployment**: The application can be deployed locally for personal use or hosted on cloud platforms to allow access from anywhere.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Travel-Agent-Video-Summary-Assistant.git
   cd Travel-Agent-Video-Summary-Assistant
2. Create a new conda environment (optional but recommended):
   ```bash
   conda create -n agent python=3.9
   conda activate agent

3. Install required packages:
   ```bash
   pip install streamlit python-docx pandas ollama

4. Run the Streamlit app:
   ```bash
   streamlit run app.py

5. Open your web browser and navigate to http://localhost:8501 to access the application.

## Usage

1. **Fetch Videos**:  
   Enter your desired travel destination and preferences, then click on the "Fetch Videos" button to retrieve relevant YouTube travel videos.

2. **Extract Transcripts**:  
   Once videos are fetched, use the "Extract Transcripts" button to convert the video audio into text, making it easier to summarize the content.

3. **Generate Summaries**:  
   After extracting transcripts, click on "Generate Summaries" to create concise summaries for each video, allowing you to quickly review the essential points.

4. **Create Itinerary**:  
   Specify your trip duration, budget, and travel style, then click "Generate Itinerary" to create a personalized travel plan based on the summaries.

5. **Interact with the AI Assistant**:  
   Use the chat interface to ask questions about your travel destination. The assistant will provide context-aware responses based on the video summaries.

6. **Download Results**:  
   At any point, you can download the results, including summaries and itineraries, for offline access.

## Showcase

### Project Video
Watch our project video to see the Travel Agent Video Summary Assistant in action:
[![Watch the video](https://img.youtube.com/vi/your_video_id/0.jpg)](https://www.youtube.com/watch?v=your_video_id)
----------------------------------------------------------------
[![Watch the video]()

### Screenshots
Below are some screenshots of the application:

![Screenshot 1](https://github.com/Pavun-KumarCH/Travel-Agent-Video-Summary-Assistant/blob/fd81e75d249d6c384e020f4e78eebb98f00c02be/assets/screenshots/Screenshot%202024-10-10%20122605.png)
*Home Page*

![Screenshot 2](https://github.com/Pavun-KumarCH/Travel-Agent-Video-Summary-Assistant/blob/fd81e75d249d6c384e020f4e78eebb98f00c02be/assets/screenshots/Screenshot%202024-10-10%20120839.png)
*Travel Agent page with personal preference's*

![Screenshot 3](https://github.com/Pavun-KumarCH/Travel-Agent-Video-Summary-Assistant/blob/fd81e75d249d6c384e020f4e78eebb98f00c02be/assets/screenshots/Screenshot%202024-10-10%20121234.png)
*Summary Generation from the video's*
 
![Screenshot 4](https://github.com/Pavun-KumarCH/Travel-Agent-Video-Summary-Assistant/blob/fd81e75d249d6c384e020f4e78eebb98f00c02be/assets/screenshots/Screenshot%202024-10-10%20121415.png)
*Itinerary generation and Agentic Chat Model*

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Contact

For questions or feedback, feel free to reach out via email: [pavun9848@gmail.com](mailto:pavun9848@gmail.com).

---

**© 2024 Travel Guide Video Summarizer by Team-206. All rights reserved.**

# Search YouTube Videos
import pandas as pd
from Components.constants import *
from youtubesearchpython import VideosSearch

def parse_views(views_str):
    """
    Parses the views string from YouTube and converts it to an integer.
    Example: 5,909 views -> 5909
    """
    views_str = views_str.lower().replace('views', '').replace(",", '').strip()
    return int(views_str)  # In case of any parsing error

def parse_duration(duration_str):
    """
    Parses the duration string from YouTube and converts it to total minutes.
    Example: "5:30" -> 5.5 minutes
    Example: "10:00" -> 10 minutes
    """
    parts = duration_str.split(':')
    # Convert to minutes, assuming the format is always "MM:SS" or "H:MM:SS"
    if len(parts) == 2:  # MM:SS
        minutes = int(parts[0])
        seconds = int(parts[1])
    elif len(parts) == 3:  # H:MM:SS
        minutes = int(parts[1]) + int(parts[0]) * 60
        seconds = int(parts[2])
    else:
        return 0  # Unexpected format
    
    return minutes + (seconds / 60)  # Return total minutes

def fetch_youtube_videos(destination, preferences, MIN_VIEWS, MAX_RESULTS, MIN_DURATION=5):
    """
    Fetches relevant YouTube videos based on the destination and user preferences.

    Parameters:
    - destination (str): The travel destination (e.g., 'Amsterdam').
    - preferences (list): List of user-selected preferences (e.g., ['Museums', 'Outdoor Activities']).
    - MIN_VIEWS (int): Minimum number of views required.
    - MAX_RESULTS (int): Maximum number of videos to fetch.
    - MIN_DURATION (int): Minimum duration in minutes to include a video.

    Returns:
    - videos (list): List of dictionaries containing video details with views parsed as integers.
    """
    # Combine the Preferences into a search query
    preference_query = " ".join(preferences)
    search_query = f"{destination} travel guide {preference_query} Netherlands"

    # Initializing VideoSearch
    video_search = VideosSearch(search_query, limit=MAX_RESULTS)

    # Execute Search 
    search_results = video_search.result()

    videos = []
    for video in search_results['result']:
        views_str = video['viewCount']['text']
        views = parse_views(views_str)
        duration_str = video['duration']
        duration = parse_duration(duration_str)
        
        # Filter out the videos with fewer than MIN_VIEWS or less than MIN_DURATION
        if views < MIN_VIEWS or duration < MIN_DURATION:
            continue  # Skip this video

        # Add the video details to the dictionary
        videos_data = {
            'Title': video['title'],
            'Duration': duration_str,  # Keep original duration string for display
            'DurationMinutes': duration,  # Total duration in minutes (for possible future use)
            'Views': views,  # Store as integer
            'Channel': video['channel']['name'],
            'Link': video['link']
        }
        videos.append(videos_data)
    
    return videos

def display_results(videos):
    """
    Displays the list of videos in a pandas DataFrame and optionally opens them in the browser.

    Parameters:
    - videos (list): List of dictionaries containing video details.
    """
    if not videos:
        print("No videos found with the specified criteria.")
        return
    
    # Create a DataFrame for better display
    videos_df = pd.DataFrame(videos)
    print(videos_df[['Title', 'Duration', 'Views', 'Channel']].to_string(index=False))

    # Display Clickable links
    print("\nClick the links below to watch the videos:\n")
    for idx, video in enumerate(videos, 1):
        # Display as Markdown link
        print(f"{idx}. {video['Title']}: [Watch Video]({video['Link']})")
    
    return videos_df

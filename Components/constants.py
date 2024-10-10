# Load Constants

DESTINATION = "Amsterdam, Dubai, Hawaii"

# Define Destination-Specific Preferences
DESTINATION_PREFERENCES = {
    "Amsterdam": [
        "Swimming",
        "Snorkeling",
        "Skydiving",  # Although Amsterdam is landlocked, including for demonstration
        "Museums",
        "Outdoor Activities",
        "Beaches",
        "Hiking",
        "Cultural Experiences",
        "Food Tours",
        "Adventure Sports",
        "Historical Sites",
        "Wildlife Tours",
        "Scenic Views",
        "City Tours",
        "Wellness Retreats",
        "Nightlife",
    ],
    "Hawaii": [
        "Swimming",
        "Snorkeling",
        "Scuba Diving",
        "Beaches",
        "Hiking",
        "Cultural Experiences",
        "Adventure Sports",
        "Scenic Views",
    ],
    "Paris": [
        "Museums",
        "Cultural Experiences",
        "Food Tours",
        "Historical Sites",
        "City Tours",
        "Scenic Views",
    ],
    "Dubai": [
        "Skydiving",
        "Beaches",
        "Adventure Sports",
        "Nightlife",
        "City Tours",
        "Scenic Views",
    ],
    "New York": [
        "Museums",
        "City Tours",
        "Food Tours",
        "Cultural Experiences",
        "Nightlife",
        "Historical Sites",
    ],
    # Add more destinations and their preferences as needed
}

# Default Preferences if Destination is Not Specified
DEFAULT_PREFERENCES = [
    "Water Games",
    "Scuba Diving",
    "Museums",
    "Outdoor Activities",
    "Beaches",
    "Hiking",
    "Cultural Experiences",
    "Food Tours",
    "Adventure Sports",
    "Historical Sites",
    "Wildlife Tours",
    "Scenic Views",
    "City Tours",
    "Wellness Retreats",
    "Nightlife",
    "Swimming",
    "Snorkeling",
    "Skydiving",
]

# Additional User Inputs
BUDGET_OPTIONS = ["Budget-Friendly", "Mid-Range", "Luxury"]
TRAVEL_STYLE_OPTIONS = ["Solo", "Family", "Romantic", "Adventure"]
MAX_RESULTS = 20  # Number of videos to fetch
MIN_VIEWS = 10000  # 10,000 views # Threshold for minimum views
LLM = "facebook/bart-large-cnn"
LOCAL_LLM = "llama3.2"
MAX_TOKENS = 1000
MIN_DURATION = 10

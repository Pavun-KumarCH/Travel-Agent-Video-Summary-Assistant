# Load Constants
from decimal import MIN_EMIN

DESTINATION = "Amsterdam"
PREFERENCES = [
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
]
MAX_RESULTS = 20 # Number of videos to fetch
MIN_VIEWS = 10000 # 10,000 views # Threshold for minimum views
LLM = "facebook/bart-large-cnn"
LOCAL_LLM = "llama3.2"
MAX_TOKENS = 1000
MIN_DURATION = 10

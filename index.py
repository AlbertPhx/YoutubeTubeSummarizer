from youtube_transcript_api import YouTubeTranscriptApi
import requests
import re
from bs4 import BeautifulSoup

def clean_filename(title):
    """Clean and format the title into a programmer-friendly snake_case file name."""
    # Remove special characters and convert spaces to underscores
    title = re.sub(r'[\/:*?"<>|]', '', title)  # Remove invalid characters
    title = re.sub(r'\s+', '_', title)         # Replace spaces with underscores
    title = re.sub(r'[^\w_]', '', title)       # Remove remaining non-alphanumeric characters
    return title.lower()                       # Convert to lowercase

def get_youtube_title(video_url):
    """Fetch the YouTube title using web scraping."""
    try:
        response = requests.get(video_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find("title").text
        return title.replace(" - YouTube", "").strip()
    except Exception as e:
        print(f"Error fetching title: {e}")
        return "unknown_title"

def download_youtube_subtitles(video_url, language='en'):
    try:
        # Extract video ID from the URL
        video_id = video_url.split("v=")[1]
        if "&" in video_id:
            video_id = video_id.split("&")[0]

        # Fetch the title
        title = get_youtube_title(video_url)
        clean_title = clean_filename(title)  # Clean the title into snake_case
        output_file = f"{clean_title}.txt"

        print(f"Downloading subtitles for: {title}")

        # Fetch subtitles using YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        
        # Save subtitles to a text file
        with open(output_file, 'w', encoding='utf-8') as file:
            for entry in transcript:
                file.write(f"{entry['text']}\n")
        
        print(f"Subtitles saved to: {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
video_url = "https://www.youtube.com/watch?v=dmFPPZFqF4w"  # Replace with your YouTube video URL
download_youtube_subtitles(video_url)

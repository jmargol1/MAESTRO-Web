import requests
from pyht import Client, TTSOptions, Format
import re
import os

API_KEY = "play_ht_api_key"
USER_ID = "play_ht_user_id"
AUDIO_URL = "url_to_voice_sample"


#Generate the voice clone voice id
def create_instant_voice(api_key, user_id, audio_url):
    """
    Creates an instant cloned voice using the PlayHT API and returns the voice_id.

    Parameters:
        api_key (str): The API key for authentication.
        user_id (str): The user ID for authentication.
        audio_url (str): The path to the audio file to be used for cloning.

    Returns:
        str: The voice_id of the created cloned voice.
    """
    # API endpoint
    url = "https://api.play.ht/api/v2/cloned-voices/instant"

    # Prepare the payload and files
    payload = {"voice_name": "sales-voice"}
    files = {"sample_file": (audio_url, open(audio_url, "rb"), "audio/mpeg")}

    # Set up headers
    headers = {
        "accept": "application/json",
        "AUTHORIZATION": api_key,
        "X-USER-ID": user_id,
    }

    try:
        # Make the POST request
        response = requests.post(url, data=payload, files=files, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the JSON response
        response_data = response.json()

        # Extract and return the voice_id
        voice_id = response_data.get("id")
        if voice_id:
            return voice_id
        else:
            raise ValueError("'id' field not found in the response.")

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None
    except ValueError as e:
        print(f"Error processing response: {e}")
        return None
    finally:
        # Ensure the file is closed after processing
        if "sample_file" in files:
            files["sample_file"][1].close()

#Generate the Voice Clone
# Initialize PlayHT API with your credentials
client = Client(USER_ID, API_KEY)

# Configure your stream
options = TTSOptions(
    voice="s3://voice-cloning-zero-shot/d0616da8-76b0-4e59-8648-d01a2d2ff09f/sales-voice/manifest.json",  # Prof Zhao
    format=Format.FORMAT_MP3,
    speed=1,
    temperature=0.1,
    quality='Premium',
    voice_guidance=1,
    style_guidance=1,
    sample_rate=24000
)

# Function to split text into chunks based on max lines and max characters
def split_text_into_chunks(text, max_lines=6, max_chars=500):
    # Split text into lines while preserving section headers and timestamps
    lines = re.split(r'(?<=\]) ', text)
    chunks = []
    chunk = []
    char_count = 0

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        if char_count + len(line) <= max_chars and len(chunk) < max_lines:
            chunk.append(line)
            char_count += len(line)
        else:
            if chunk:  # Only add non-empty chunks
                chunks.append(" ".join(chunk))
            chunk = [line]
            char_count = len(line)

    if chunk:  # Add the last chunk if it's not empty
        chunks.append(" ".join(chunk))

    return chunks

# Function to load and process a single script file
def process_script_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read().strip()  # Remove leading/trailing whitespace
    return content

# Function to parse a single script file with format [slide1](introduction) text...
def parse_slide_format_1(content):
    slides = []
    pattern = re.compile(r'\[slide(\d+)\]\(([^)]+)\)\s*(.*)')
    matches = pattern.findall(content)
    for slide_number, slide_title, slide_text in matches:
        slides.append({
            "slide_number": slide_number,
            "slide_title": slide_title,
            "slide_text": slide_text.strip(),
            "output_filename": f"output_{slide_number}.mp3"
        })
    return slides

# Function to parse a single script file with format [s1] text...
def parse_slide_format_2(content):
    slides = []
    pattern = re.compile(r'\[s(\d+)\]\s*(.*)')
    matches = pattern.findall(content)
    for slide_number, slide_text in matches:
        slides.append({
            "slide_number": slide_number,
            "slide_text": slide_text.strip(),
            "output_filename": f"output_{slide_number}.mp3"
        })
    return slides

# Function to process multiple script files in the format slide_1_script.txt, slide_2_script.txt, etc.
def process_multiple_script_files(input_dir):
    slides = []
    for filename in os.listdir(input_dir):
        if filename.startswith("slide_") and filename.endswith("_script.txt"):
            slide_number = filename.split("_")[1]  # Extract slide number from filename
            slide_filepath = os.path.join(input_dir, filename)
            slide_content = process_script_file(slide_filepath)
            slides.append({
                "slide_number": slide_number,
                "slide_text": slide_content,
                "output_filename": f"output_{slide_number}.mp3"
            })
    return slides

# Main function to handle all cases
def generate_audio_from_scripts(input_dir, script_format="multiple_files"):
    if script_format == "format_1":
        # Case 1: Single script file with format [slide1](introduction) text...
        script_filepath = os.path.join(input_dir, "script.txt")
        content = process_script_file(script_filepath)
        slides = parse_slide_format_1(content)
    elif script_format == "format_2":
        # Case 2: Single script file with format [s1] text...
        script_filepath = os.path.join(input_dir, "script.txt")
        content = process_script_file(script_filepath)
        slides = parse_slide_format_2(content)
    elif script_format == "multiple_files":
        # Case 3: Multiple script files in the format slide_1_script.txt, slide_2_script.txt, etc.
        slides = process_multiple_script_files(input_dir)
    else:
        raise ValueError("Invalid script format specified.")

    # Generate audio for each slide
    for slide in slides:
        slide_number = slide["slide_number"]
        slide_text = slide["slide_text"]
        output_filename = slide["output_filename"]
        output_filepath = os.path.join(input_dir, output_filename)

        # Skip if the slide content is empty
        if not slide_text:
            print(f"Skipping slide {slide_number} because the script is empty.")
            continue

        # Split the slide content into chunks
        text_chunks = split_text_into_chunks(slide_text)

        # Skip if no valid chunks are found
        if not text_chunks:
            print(f"Skipping slide {slide_number} because no valid chunks were generated.")
            continue

        # Generate audio for the slide
        try:
            with open(output_filepath, "wb") as audio_file:
                for chunk_text in text_chunks:
                    # Validate the chunk before sending it to the API
                    if not chunk_text.strip():  # Skip empty chunks
                        print(f"Skipping empty chunk for slide {slide_number}.")
                        continue

                    # Log the chunk being sent to the API
                    print(f"Processing chunk for slide {slide_number}: {chunk_text[:50]}...")  # Log first 50 chars

                    # Send the chunk to the API
                    for chunk in client.tts(text=chunk_text, voice_engine="Play3.0-mini", options=options):
                        audio_file.write(chunk)

            print(f"Audio for slide {slide_number} generated and saved as {output_filename}.")
        except Exception as e:
            print(f"Error generating audio for slide {slide_number}: {e}")

# Example usage
input_dir = "/content/output/scripts"  # Directory containing script files
script_format = "multiple_files"  # Options: "format_1", "format_2", "multiple_files"

generate_audio_from_scripts(input_dir, script_format)
import os
import argparse
from openai import OpenAI
import subprocess
from utils import *

def generate_slide_script(image_path, slide_number, total_slides, previous_content, api_key):
    client = OpenAI(api_key=api_key)
    base64_image = encode_image(image_path)
    
    system_message = {
        "role": "system",
        "content": """You are an expert computer science lecturer delivering clear, concise explanations.
    Rules:
    1. Only explain visible content
    2. Use natural speech patterns
    3. No meta-references or slide mentions
    4. Skip irrelevant metadata
    5. Maintain logical flow between slides
    6. Keep explanations focused and precise
    7. Explain concepts concisely
    8. Never say "Title:..."
    """
    }
    
    position = "first" if slide_number == 1 else "last" if slide_number == total_slides else "middle"
    position_instructions = {
        "first": "Just mention the name of the algorithm or topic we will explore. Duration: 2-5 seconds.",
        "middle": "Continue the technical explanation, connecting with previous concepts. Duration: 40-90 seconds.",
        "last": "Conclude the visible content naturally."
    }
    
    user_message = {
        "role": "user",
        "content": [
            {"type": "text", "text": f"Generate a teaching script following these parameters:\n"
                                   f"1. Content scope: Only explain visible elements\n"
                                   f"2. Position context: {position_instructions[position]}\n"
                                   f"3. Technical accuracy: Maintain precise terminology\n"
                                   f"4. Flow: Natural transitions between concepts"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]
    }
    
    messages = [system_message] + (previous_content or []) + [user_message]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=350,
            temperature=0.7
        )
        return response.choices[0].message.content, messages
    except Exception as e:
        print(f"Error generating script for slide {slide_number}: {str(e)}")
        return "", messages

def generate_audio(script_text, slide_number, output_dir, api_key):
    client = OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=script_text
    )
    
    audio_path = os.path.join(output_dir, f"slide_{slide_number}.mp3")
    response.stream_to_file(audio_path)
    time.sleep(1)
    return audio_path

def create_video_ffmpeg(images_dir, audio_dir, output_path):
    """Create video from images and audio."""
    pairs = get_sorted_pairs(images_dir, audio_dir)
    if not pairs:
        raise ValueError("No valid image-audio pairs found")

    video_list = "video_list.txt"
    audio_concat = "audio_concat.txt"
    temp_video = "temp_video.mp4"
    temp_audio = "temp_audio.mp3"
    
    with open(video_list, "w") as vf, open(audio_concat, "w") as af:
        for img, aud in pairs:
            dur = get_audio_duration(aud)
            vf.write(f"file '{img}'\nduration {dur}\n")
            af.write(f"file '{aud}'\nduration {dur}\n")
        vf.write(f"file '{pairs[-1][0]}'\n")
        af.write(f"file '{pairs[-1][1]}'\n")

    # video and audio
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", video_list,
                   "-vsync", "vfr", "-pix_fmt", "yuv420p", "-c:v", "libx264", temp_video])
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", audio_concat,
                   "-c", "copy", temp_audio])
    
    # merge video and audio
    subprocess.run(["ffmpeg", "-y", "-i", temp_video, "-i", temp_audio,
                   "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_path])

    # cleanup
    for f in [video_list, audio_concat, temp_video, temp_audio]:
        if os.path.exists(f):
            os.remove(f)

def main():
    parser = argparse.ArgumentParser(description="Generate video from PDF presentation")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("api_key", help="OpenAI API key")
    parser.add_argument("--output", default="output.mp4", help="Output video path")
    args = parser.parse_args()

    setup_directories()
    clean_directories()

    try:
        images_dir = convert_pdf_to_images(args.pdf_path)
        
        # script generation
        scripts_dir = "output/scripts"
        os.makedirs(scripts_dir, exist_ok=True)
        image_files = sorted([os.path.join(images_dir, f) for f in os.listdir(images_dir) 
                            if f.endswith(".png")], key=natural_sort_key)
        
        conversation_history = []
        scripts_list = []
        
        print("Generating scripts...")
        for i, image_file in enumerate(image_files, 1):
            script_text, updated_history = generate_slide_script(
                image_file, i, len(image_files), conversation_history, args.api_key
            )
            conversation_history = updated_history
            scripts_list.append(script_text)
            
            with open(os.path.join(scripts_dir, f"slide_{i}_script.txt"), "w") as f:
                f.write(script_text)
        
        # audio generation
        print("Generating audio...")
        audio_dir = "output/audio"
        os.makedirs(audio_dir, exist_ok=True)
        for i, script_text in enumerate(scripts_list, 1):
            if script_text.strip():
                generate_audio(script_text, i, audio_dir, args.api_key)
        
        # video generation
        print("Creating video...")
        create_video_ffmpeg(images_dir, audio_dir, args.output)
        print(f"Video created successfully: {args.output}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
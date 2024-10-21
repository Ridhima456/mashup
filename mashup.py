import streamlit as st
from youtubesearchpython import VideosSearch
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.utils import which
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# Set the ffmpeg path manually
AudioSegment.converter = which("E:/ffmpeg/bin/ffmpeg.exe")

# Function to sanitize filenames by replacing problematic characters
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Function to search for YouTube videos by keyword
def search_youtube(keyword, max_results=1):
    videos_search = VideosSearch(keyword, limit=max_results)
    results = videos_search.result()
    if results['result']:
        return [video['link'] for video in results['result']]  # Return a list of video links
    return []

# Function to download videos by keyword
def download_videos_by_keyword(keyword, save_path, number_of_videos=1):
    video_links = search_youtube(keyword, max_results=number_of_videos)
    if video_links:
        try:
            # yt-dlp options
            ydl_opts = {
                'format': 'best',  # Select the best quality
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save location and file name template
            }

            # Download each video in the list
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(video_links)
            print('Videos downloaded successfully!')

        except Exception as e:
            print("Some Error occurred:", e)
    else:
        print("No videos found for the given keyword.")

# Function to convert video to audio
def convert_videos_to_audio(video_dir, audio_dir):
    # Ensure video directory exists
    if not os.path.exists(video_dir):
        print(f"Error: The directory '{video_dir}' does not exist.")
        return

    # Ensure audio directory exists
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    # Process each video in the directory
    for video_file in os.listdir(video_dir):
        if video_file.endswith(".mp4") or video_file.endswith(".mkv") or video_file.endswith(".webm"):
            video_path = os.path.join(video_dir, video_file)
            audio_filename = sanitize_filename(os.path.splitext(video_file)[0]) + '.mp3'
            audio_path = os.path.join(audio_dir, audio_filename)

            try:
                # Load the video clip
                with VideoFileClip(video_path) as video_clip:
                    # Extract audio and save as MP3
                    video_clip.audio.write_audiofile(audio_path)
                    print(f'Converted {video_file} to {audio_path}')
            except Exception as e:
                print(f"Error converting {video_file}: {e}")

# Function to process audio: extract the first 10 seconds from each file and then combine
def process_and_join_audio(audio_dir, output_path):
    combined_audio = AudioSegment.empty()

    # Process each audio file in the directory
    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".mp3"):
            audio_path = os.path.join(audio_dir, audio_file)
            print(f"Processing file: {audio_path}")  # Debugging print

            try:
                # Load the audio file
                audio = AudioSegment.from_file(audio_path)

                # Extract only the first 10 seconds
                trimmed_audio = audio[:10 * 1000]  # Extract first 10 seconds (10 * 1000 ms)

                # Append to the combined audio
                combined_audio += trimmed_audio
                print(f'Processed {audio_file}')
            except Exception as e:
                print(f"Error processing file {audio_file}: {e}")

    # Export the combined audio
    combined_audio.export(output_path, format="mp3")
    print(f'Combined audio saved to {output_path}')

# Function to send email with attachment
def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, body, attachment_path):
    try:
        # Create the email object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Attach the file
        if attachment_path:
            with open(attachment_path, 'rb') as attachment:
                # Create a MIMEBase object for the file
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
                msg.attach(part)

        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)

        print('Email sent successfully!')

    except Exception as e:
        print(f"Failed to send email. Error: {e}")

# Streamlit app logic
st.title("Download and Send Combined Audio")

singer_name = st.text_input("Enter Singer Name")
number_of_songs = st.number_input("Enter Number of Songs", min_value=1, step=1)
email = st.text_input("Enter Receiver's Email")

if st.button("Submit"):
    if singer_name and email:
        # Define paths for saving files
        SAVE_PATH = "Downloads"
        AUDIO_SAVE_PATH = "Audio"
        COMBINED_AUDIO_PATH = "combined_audio.mp3"

        # Step 1: Ensure save path exists
        if not os.path.exists(SAVE_PATH):
            os.makedirs(SAVE_PATH)

        # Step 2: Download videos
        download_videos_by_keyword(singer_name, SAVE_PATH, number_of_songs)

        # Step 3: Convert videos to audio
        convert_videos_to_audio(SAVE_PATH, AUDIO_SAVE_PATH)

        # Step 4: Process and join audio files
        process_and_join_audio(AUDIO_SAVE_PATH, COMBINED_AUDIO_PATH)

        # Step 5: Send the email with the combined audio file attached
        # Use app password for secure authentication
        sender_email = "ridhimachoudahry123rc@gmail.com"  # Replace with sender's email
        sender_password = "annk ulwm jcif hzgl"
        subject = f"Combined Audio of {singer_name} songs"
        body = f"Here is the combined audio file of {singer_name}'s songs."
        
        send_email_with_attachment(sender_email, sender_password, email, subject, body, COMBINED_AUDIO_PATH)

        st.success("Process complete! Email sent successfully.")
    else:
        st.error("Please fill in all the fields.")

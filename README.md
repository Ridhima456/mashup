# mashup
##  YouTube Mashup Audio Downloader & Emailer
This is a Streamlit web application that allows users to input a singer's name, specify the number of songs they want to download from YouTube, and provide an email address to receive the combined audio of the first 10 seconds of each song. The app downloads YouTube videos, converts them to audio, processes the audio, and emails the combined file to the provided email address.

## Features
Search and download YouTube videos by singer name.
Convert downloaded videos to MP3 audio.
Extract the first 10 seconds of each audio file and combine them.
Email the combined audio file as an attachment.
## Requirements
Python 3.6 or higher
The following Python packages:
streamlit
yt-dlp
moviepy
pydub
youtubesearchpython
## Setup Instructions
#### 1. Clone the repository
bash
Copy code
git clone https://github.com/your-repo/youtube-mashup-audio-downloader
cd youtube-mashup-audio-downloader
### 2. Install dependencies
Run the following command to install all required packages:

bash
Copy code
pip install streamlit yt-dlp moviepy pydub youtubesearchpython
### 3. Ensure FFmpeg is installed
Download FFmpeg from ffmpeg.org.
Extract it and set the path to the ffmpeg.exe in the code at:
python
Copy code
AudioSegment.converter = which("path/to/your/ffmpeg/bin/ffmpeg.exe")
### 4. Run the Application
To start the application, run the following command:

bash
Copy code
streamlit run app.py
The app will open in your default web browser. You can also visit the URL http://localhost:8501.

#### 5. Input Data
Enter the singer name.
Enter the number of songs you want to download.
Enter the email address to receive the combined audio file.
Click Submit to start the process.
## Email Setup
Replace the placeholder your_email@gmail.com in the code with your own Gmail address.
Replace your_app_password with a Gmail App Password. You can generate an App Password from your Google account settings if you have 2-Step Verification enabled.
## How It Works
The app searches for the specified number of YouTube videos by the singer's name.
It downloads the videos and converts them to MP3 format.
The app processes the audio, extracts the first 10 seconds of each audio file, and combines them.
The combined audio file is emailed to the provided email address as an attachment.
## Troubleshooting
Ensure that ffmpeg is installed and the path is correctly set.
Ensure you have a valid Gmail App Password for sending emails via the app.
## License
This project is open-source and available under the MIT License.

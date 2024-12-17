
# 🎶 Audio Splitter, Merger, and Backing Track Downloader 🎶  

This project is a **Django-based web application** that allows users to:  
1. **Split audio files** into smaller parts.  
2. **Merge multiple audio files** into one.  
3. **Download backing tracks** (like MP3 files) from external source but the source is (secret) :)

The application is only for my personal use. Because I love to play guitar, I want to be able to make guitar backing track for any song.

---

## 🚀 **Features**

### 1. **Audio Splitter**  
- Upload an mp3 file and split it into smaller parts based on specific time intervals.  
- Saves split parts for easy download.

### 2. **Audio Merger**  
- Upload multiple audio files and merge them into a single track.  
- The merge follows specific logic that only I understand the reason for :)
- Outputs the merged file in mp3 format.
- Easy download.

### 3. **Backing Track Downloader**  
- Download MP3 backing tracks but you need to have the token.
- Saves downloaded file.

---

## 🛠️ **Technologies Used**

- **Backend**: Django (Python)  
- **Media Storage**: Django Media Directory  
- **Audio Processing**: `pydub` library for splitting and merging audio files  
- **HTTP Requests**: `requests` for downloading MP3 files from external sources  

---
## 🎛️ **Setup Instructions**

### 1. **Clone the Repository**

```bash
git clone https://github.com/am-awaludinmuhammad/audiowork.git
cd audiowork
```

---

### 2. **Install Dependencies**

Ensure you have Python and `pip` installed. Install the required libraries:

```bash
pip install -r requirements.txt
```
---

### 3. **Setup .env file**

Start the local server:

```bash
cp .env.example .env
```
---

### 4. **Run the Development Server**

Start the local server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser to access the application.

---

## 📦 **Dependencies**

The following libraries are used in this project:

- `Django` - Web framework  
- `pydub` - Audio processing library  
- `requests` - For HTTP file downloads  
- `ffmpeg` - Required for `pydub` to handle audio file conversions 

---
## 📝 **License**
This code is for personal use only. All rights reserved.
---

## 📧 **Contact**

For any questions or support, feel free to reach out:  
- **Email**: am.awaludinmuhammad@gmail.com  
- **GitHub**: [Awaludin Muhammad](https://github.com/am-awaludinmuhammad)
---
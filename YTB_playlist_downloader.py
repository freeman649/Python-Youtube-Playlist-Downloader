import re
import os
import tkinter as tk
from googleapiclient.discovery import build
from pytube import YouTube

def get_playlist_videos(api_key, playlist_link):
    youtube = build('youtube', 'v3', developerKey=api_key)

    playlist_id = re.findall(r'[?&]list=([^&]+)', playlist_link)[0]

    playlist_items = youtube.playlistItems().list(
        playlistId=playlist_id,
        part='snippet',
        maxResults=50
    ).execute()

    videos = []
    for playlist_item in playlist_items['items']:
        video = {
            'title': playlist_item['snippet']['title'],
            'videoId': playlist_item['snippet']['resourceId']['videoId'],
            'url': f'https://www.youtube.com/watch?v={playlist_item["snippet"]["resourceId"]["videoId"]}'
        }
        videos.append(video)

    return videos

def download_videos(videos):
    if not os.path.exists("videos"):
        os.makedirs("videos")

    for video in videos:
        youtube_url = video["url"]
        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(file_extension="mp4", resolution="720p").first()
            result_text.config(state=tk.NORMAL)
            result_text.insert(tk.END, f"Téléchargement de {yt.title}...\n")
            result_text.config(state=tk.DISABLED)
            stream.download("videos")
            result_text.config(state=tk.NORMAL)
            result_text.insert(tk.END, f"{yt.title} a été téléchargé avec succès.\n\n")
            result_text.config(state=tk.DISABLED)
        except Exception as e:
            result_text.config(state=tk.NORMAL)
            result_text.insert(tk.END, f"Erreur lors du téléchargement de {yt.title}: {e}\n\n")
            result_text.config(state=tk.DISABLED)

def fetch_videos():
    api_key = api_key_entry.get()
    playlist_link = playlist_link_entry.get()

    try:
        videos = get_playlist_videos(api_key, playlist_link)

        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)

        result_text.insert(tk.END, "Vidéos de la playlist :\n")
        for video in videos:
            result_text.insert(tk.END, f'{video["title"]} - {video["url"]}\n')

        result_text.config(state=tk.DISABLED)

        download_videos(videos)
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"Une erreur s'est produite : {e}\n")
        result_text.config(state=tk.DISABLED)



window = tk.Tk()
window.title("YouTube Playlist Downloader")

api_key_label = tk.Label(window, text="Clé API YouTube:")
api_key_label.pack()
api_key_entry = tk.Entry(window, width=40)
api_key_entry.pack()

playlist_link_label = tk.Label(window, text="Lien de la playlist YouTube:")
playlist_link_label.pack()
playlist_link_entry = tk.Entry(window, width=40)
playlist_link_entry.pack()

fetch_button = tk.Button(window, text="Récupérer les vidéos", command=fetch_videos)
fetch_button.pack()

result_text = tk.Text(window, height=10, width=50, state=tk.DISABLED)
result_text.pack()

window.mainloop()

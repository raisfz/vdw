from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/download")
def download_video(url: str = Query(..., title="Video URL")):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        result = {
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail'),
            'formats': [
                {
                    'format_note': f.get('format_note'),
                    'ext': f.get('ext'),
                    'filesize': f.get('filesize'),
                    'url': f.get('url')
                }
                for f in formats if f.get('url') and f.get('vcodec') != 'none'
            ]
        }
        return result

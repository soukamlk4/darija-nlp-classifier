from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

# ----------------------------------------
# LA VIDÉO CIBLE
# ----------------------------------------
VIDEO_ID = "TLf7wGzmQ1w"
CHANNEL = "manual_video"
CATEGORY = "Food/Cuisine"  # ← change ça

# ----------------------------------------
# PARTIE 1 — COMMENTAIRES
# ----------------------------------------
def get_comments(video_id):
    comments = []
    next_page_token = None

    try:
        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response["items"]:
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "text": snippet["textDisplay"],
                    "date": snippet["publishedAt"]
                })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    except Exception as e:
        print(f"❌ Erreur commentaires : {e}")

    return comments

# ----------------------------------------
# PARTIE 2 — TRANSCRIPTION
# ----------------------------------------
def get_transcription(video_id):
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id, languages=['ar'])
        return transcript
    except Exception as e:
        print(f"❌ Erreur transcription : {e}")
        return None

def chunk_text(transcript, chunk_size=150):
    full_text = " ".join([seg.text for seg in transcript])
    words = full_text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        if len(chunk.split()) >= 20:
            chunks.append(chunk)
    return chunks

# ----------------------------------------
# SCRAPING COMMENTAIRES
# ----------------------------------------
print(f"📥 Récupération des commentaires pour {VIDEO_ID}...")
comments = get_comments(VIDEO_ID)
print(f"✅ {len(comments)} commentaires trouvés")

comments_data = []
for j, c in enumerate(comments):
    comments_data.append({
        "id": f"YT_{CHANNEL}_{VIDEO_ID}_{j:04d}",
        "text": c["text"],
        "source_platform": "YouTube",
        "source_type": "comment",
        "source_account": CHANNEL,
        "category": CATEGORY,
        "date": c["date"],
        "label": None
    })

# Sauvegarde commentaires
df_comments = pd.DataFrame(comments_data)
os.makedirs("data/raw", exist_ok=True)
df_comments.to_csv(f"data/raw/video_{VIDEO_ID}_comments.csv", 
                   index=False, encoding="utf-8-sig")
print(f"💾 Commentaires sauvegardés : data/raw/video_{VIDEO_ID}_comments.csv")

# ----------------------------------------
# SCRAPING TRANSCRIPTION
# ----------------------------------------
print(f"\n📥 Récupération de la transcription pour {VIDEO_ID}...")
transcript = get_transcription(VIDEO_ID)

if transcript:
    chunks = chunk_text(transcript)
    print(f"✅ {len(chunks)} chunks trouvés")

    transcript_data = []
    for j, chunk in enumerate(chunks):
        transcript_data.append({
            "id": f"YT_TRANSCRIPT_{CHANNEL}_{VIDEO_ID}_{j:03d}",
            "text": chunk,
            "source_platform": "YouTube",
            "source_type": "transcription",
            "source_account": CHANNEL,
            "category": CATEGORY,
            "date": None,
            "label": None
        })

    df_transcript = pd.DataFrame(transcript_data)
    df_transcript.to_csv(f"data/raw/video_{VIDEO_ID}_transcription.csv",
                         index=False, encoding="utf-8-sig")
    print(f"💾 Transcription sauvegardée : data/raw/video_{VIDEO_ID}_transcription.csv")
else:
    print("⚠️ Pas de transcription disponible pour cette vidéo")

# ----------------------------------------
# RÉSUMÉ
# ----------------------------------------
print(f"\n{'='*50}")
print(f"✅ TERMINÉ")
print(f"Commentaires : {len(comments_data)}")
print(f"Transcription chunks : {len(transcript_data) if transcript else 0}")
print(f"\nFichiers créés dans data/raw/ :")
print(f"  - video_{VIDEO_ID}_comments.csv")
if transcript:
    print(f"  - video_{VIDEO_ID}_transcription.csv")
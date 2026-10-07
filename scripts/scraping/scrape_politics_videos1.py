from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import pandas as pd
import os
import time

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

# ----------------------------------------
# LISTE DES VIDÉOS CIBLÉES
# ----------------------------------------
videos = [
    {"id": "ez_ainrxTDo", "category": "Politics/Société", "account": "manual_politics"},
    {"id": "rjgUvwR5XNE", "category": "Politics/Société", "account": "manual_politics"},
    {"id": "6H91c284Dg4", "category": "Politics/Société", "account": "manual_politics"},
    {"id": "8vD2dty6YGY", "category": "Politics/Société", "account": "manual_politics"},
    {"id": "Jzu63GtMKfo", "category": "Politics/Société", "account": "manual_politics"},
    {"id": "Zix16HW7QxI", "category": "Politics/Société", "account": "manual_politics"},
    {"id": "pCMEamSc8Os", "category": "Politics/Société", "account": "manual_politics"},
    {"id": "IJBMQVmoYnA", "category": "Politics/Société", "account": "manual_politics"},
    {"id": "gfERjJ3RYFM", "category": "Politics/Société", "account": "manual_politics"},
]

# ----------------------------------------
# FONCTIONS
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
        print(f"  ❌ Erreur : {e}")
    return comments

def get_transcription(video_id):
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id, languages=['ar'])
        return transcript
    except Exception as e:
        print(f"  ⚠️ Transcription : {e}")
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
# PIPELINE
# ----------------------------------------
os.makedirs("data/raw", exist_ok=True)

all_comments = []
all_transcriptions = []

for video in videos:
    vid_id   = video["id"]
    category = video["category"]
    account  = video["account"]

    print(f"\n{'='*50}")
    print(f"🎬 Vidéo : {vid_id} | {category}")

    # --- Commentaires ---
    print(f"  📥 Récupération commentaires...")
    comments = get_comments(vid_id)
    print(f"  ✅ {len(comments)} commentaires")

    for j, c in enumerate(comments):
        all_comments.append({
            "id":              f"YT_{account}_{vid_id}_{j:04d}",
            "text":            c["text"],
            "source_platform": "YouTube",
            "source_type":     "comment",
            "source_account":  account,
            "category":        category,
            "date":            c["date"],
            "label":           None
        })

    # --- Transcription ---
    print(f"  📥 Récupération transcription...")
    transcript = get_transcription(vid_id)

    if transcript:
        chunks = chunk_text(transcript)
        print(f"  ✅ {len(chunks)} chunks")
        for j, chunk in enumerate(chunks):
            all_transcriptions.append({
                "id":              f"YT_TRANSCRIPT_{account}_{vid_id}_{j:03d}",
                "text":            chunk,
                "source_platform": "YouTube",
                "source_type":     "transcription",
                "source_account":  account,
                "category":        category,
                "date":            None,
                "label":           None
            })
    else:
        print(f"  ⚠️ Pas de transcription")

    time.sleep(1)

# ----------------------------------------
# SAUVEGARDE
# ----------------------------------------
print(f"\n{'='*50}")
print("💾 Sauvegarde des fichiers...")

# Commentaires
df_comments = pd.DataFrame(all_comments)
df_comments.to_csv("data/raw/politics_videos_comments.csv",
                   index=False, encoding="utf-8-sig")
print(f"✅ Commentaires : data/raw/politics_videos_comments.csv ({len(df_comments)} lignes)")

# Transcriptions
if all_transcriptions:
    df_transcriptions = pd.DataFrame(all_transcriptions)
    df_transcriptions.to_csv("data/raw/politics_videos_transcriptions.csv",
                             index=False, encoding="utf-8-sig")
    print(f"✅ Transcriptions : data/raw/politics_videos_transcriptions.csv ({len(df_transcriptions)} lignes)")
else:
    print("⚠️ Aucune transcription trouvée")

# ----------------------------------------
# RÉSUMÉ FINAL
# ----------------------------------------
print(f"\n{'='*50}")
print(f"✅ TERMINÉ")
print(f"Total commentaires   : {len(all_comments)}")
print(f"Total transcriptions : {len(all_transcriptions)}")
print(f"\nRépartition commentaires par catégorie :")
print(df_comments["category"].value_counts())
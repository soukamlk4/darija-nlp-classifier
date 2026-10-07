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
# VIDÉOS MANUELLES — Religion
# ----------------------------------------
manual_videos = [
    {"id": "TqQFS6Su0so", "category": "Religion", "account": "manual_religion"},
    {"id": "3zzjXdFlFAU", "category": "Religion", "account": "manual_religion"},
    {"id": "mN29oWSm8-c", "category": "Religion", "account": "manual_religion"},
    {"id": "z44oRLCvP2M", "category": "Religion", "account": "manual_religion"},
    {"id": "6M2IAoSDyu0", "category": "Religion", "account": "manual_religion"},
    {"id": "mZb9UR_3lm0", "category": "Religion", "account": "manual_religion"},
    {"id": "qZp3ODcXzhM", "category": "Religion", "account": "manual_religion"},
    {"id": "625UnebfXfo", "category": "Religion", "account": "manual_religion"},
    {"id": "aL_10aRwQIU", "category": "Religion", "account": "manual_religion"},
    {"id": "6GIl1Fh72g4", "category": "Religion", "account": "manual_religion"},



]

# ----------------------------------------
# CHAÎNES YouTube — Religion
# ----------------------------------------
channels = [
    ("yassineelamri", "Religion"),
    ("issti9ama",     "Religion"),
]

# ----------------------------------------
# FONCTIONS
# ----------------------------------------
def get_channel_id(channel_name):
    try:
        request = youtube.search().list(
            part="snippet",
            q=channel_name,
            type="channel",
            maxResults=1
        )
        response = request.execute()
        channel_id = response["items"][0]["id"]["channelId"]
        print(f"   ID trouvé : {channel_id}")
        return channel_id
    except Exception as e:
        print(f"   Erreur : {e}")
        return None

def get_video_ids(channel_id, max_videos=30):
    video_ids = []
    next_page_token = None
    try:
        while len(video_ids) < max_videos:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                type="video",
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            for item in response["items"]:
                video_ids.append(item["id"]["videoId"])
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
    except Exception as e:
        print(f"   Erreur vidéos : {e}")
    print(f"   {len(video_ids)} vidéos trouvées")
    return video_ids[:max_videos]

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
        print(f"   Erreur commentaires : {e}")
    return comments

def get_transcription(video_id):
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id, languages=['ar'])
        return transcript
    except Exception as e:
        print(f"   Transcription : {e}")
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

all_comments       = []
all_transcriptions = []

# --- PARTIE 1 : Vidéos manuelles ---
print("\n" + "="*50)
print("📋 PARTIE 1 — Vidéos manuelles")
print("="*50)

for video in manual_videos:
    vid_id   = video["id"]
    category = video["category"]
    account  = video["account"]

    print(f"\n🎬 Vidéo : {vid_id}")

    # Commentaires
    print(f"  📥 Commentaires...")
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

    # Transcription
    print(f"  📥 Transcription...")
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

# --- PARTIE 2 : Chaînes YouTube ---
print("\n" + "="*50)
print("📋 PARTIE 2 — Chaînes YouTube")
print("="*50)

for channel_name, category in channels:
    print(f"\n=== Chaîne : {channel_name} ===")

    channel_id = get_channel_id(channel_name)
    if not channel_id:
        print(f"  ⏭️ Chaîne introuvable")
        continue

    video_ids = get_video_ids(channel_id, max_videos=30)

    for i, vid_id in enumerate(video_ids):
        print(f"  Vidéo {i+1}/{len(video_ids)} : {vid_id}", end=" ")

        # Commentaires
        comments = get_comments(vid_id)
        for j, c in enumerate(comments):
            all_comments.append({
                "id":              f"YT_{channel_name}_{i:03d}_{j:04d}",
                "text":            c["text"],
                "source_platform": "YouTube",
                "source_type":     "comment",
                "source_account":  channel_name,
                "category":        category,
                "date":            c["date"],
                "label":           None
            })

        # Transcription
        transcript = get_transcription(vid_id)
        if transcript:
            chunks = chunk_text(transcript)
            for j, chunk in enumerate(chunks):
                all_transcriptions.append({
                    "id":              f"YT_TRANSCRIPT_{channel_name}_{i:03d}_{j:03d}",
                    "text":            chunk,
                    "source_platform": "YouTube",
                    "source_type":     "transcription",
                    "source_account":  channel_name,
                    "category":        category,
                    "date":            None,
                    "label":           None
                })

        print(f"→ {len(comments)} commentaires")
        time.sleep(1)

    # Sauvegarde intermédiaire
    pd.DataFrame(all_comments).to_csv(
        "data/raw/domain_religion_comments.csv",
        index=False, encoding="utf-8-sig"
    )
    print(f"  💾 Sauvegarde intermédiaire : {len(all_comments)} commentaires")
    time.sleep(2)

# ----------------------------------------
# SAUVEGARDE FINALE — 2 fichiers
# ----------------------------------------
print(f"\n{'='*50}")
print("💾 Sauvegarde finale...")

# Fichier 1 — Commentaires
df_comments = pd.DataFrame(all_comments)
df_comments.to_csv("data/raw/domain_religion_comments.csv",
                   index=False, encoding="utf-8-sig")
print(f"✅ Commentaires  : data/raw/domain_religion_comments.csv ({len(df_comments)} lignes)")

# Fichier 2 — Transcriptions
if all_transcriptions:
    df_transcriptions = pd.DataFrame(all_transcriptions)
    df_transcriptions.to_csv("data/raw/domain_religion_transcriptions.csv",
                             index=False, encoding="utf-8-sig")
    print(f"✅ Transcriptions : data/raw/domain_religion_transcriptions.csv ({len(df_transcriptions)} lignes)")
else:
    print("⚠️ Aucune transcription trouvée")

# ----------------------------------------
# RÉSUMÉ FINAL
# ----------------------------------------
print(f"\n{'='*50}")
print(f"✅ RELIGION TERMINÉ")
print(f"Total commentaires   : {len(all_comments)}")
print(f"Total transcriptions : {len(all_transcriptions)}")
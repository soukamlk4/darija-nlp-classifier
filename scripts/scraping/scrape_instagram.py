import instaloader
import pandas as pd
import time
import random
import os

# ----------------------------------------
# CONNEXION INSTAGRAM
# ----------------------------------------
L = instaloader.Instaloader()

# Mets tes identifiants ici
INSTAGRAM_USER = "lilac__chu"
INSTAGRAM_PASS = "soukaina2004__"

try:
    L.login(INSTAGRAM_USER, INSTAGRAM_PASS)
    print("✅ Connecté à Instagram")
except Exception as e:
    print(f"❌ Erreur connexion : {e}")
    pass  # ← change exit() par pass

# ----------------------------------------
# LISTE DES SOURCES
# ----------------------------------------
sources = [
    ("sehti.fid9i9a",      "Medical/Santé"),
    ("doctor.mouad",        "Medical/Santé"),
    ("professeurdirham",    "Business/Économie"),
    ("noureddinekhiti",     "Business/Économie"),
    ("pilota.11",           "Sports/Fitness"),
    ("coachhajar.ma",       "Sports/Fitness"),
    ("rachidachachi",       "Politics/Société"),
    ("yassine_elamri.1",    "Religion"),
    ("issti9ama",           "Religion"),
    ("simosedraty",         "Entertainment"),
    ("nbalsimarouane",      "Entertainment"),
    ("9ossos",              "Food/Cuisine"),
    ("chef.moha",           "Food/Cuisine"),
    ("inidnews",            "Miscill"),
]

# ----------------------------------------
# FONCTION SCRAPING
# ----------------------------------------
def scrape_instagram(username, category, max_posts=30):
    data = []
    
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print(f"  👤 {profile.full_name} — {profile.mediacount} posts")
        
        post_count = 0
        for post in profile.get_posts():
            if post_count >= max_posts:
                break
            
            try:
                comment_count = 0
                for comment in post.get_comments():
                    data.append({
                        "id": f"IG_{username}_{post_count:03d}_{comment_count:04d}",
                        "text": comment.text,
                        "source_platform": "Instagram",
                        "source_type": "comment",
                        "source_account": username,
                        "category": category,
                        "date": str(comment.created_at_utc),
                        "label": None
                    })
                    comment_count += 1
                
                post_count += 1
                print(f"  Post {post_count}/{max_posts} → {comment_count} commentaires")
                
                # Pause aléatoire entre chaque post
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"  ⚠️ Erreur post : {e}")
                time.sleep(5)
                continue
    
    except Exception as e:
        print(f"  ❌ Erreur profil {username} : {e}")
    
    return data

# ----------------------------------------
# PIPELINE PRINCIPALE
# ----------------------------------------
all_data = []

for username, category in sources:
    print(f"\n=== Scraping Instagram : {username} ({category}) ===")
    
    data = scrape_instagram(username, category, max_posts=30)
    all_data.extend(data)
    
    print(f"  💬 Total {username} : {len(data)} commentaires")
    
    # Sauvegarde intermédiaire après chaque compte
    df_temp = pd.DataFrame(all_data)
    df_temp.to_csv("data/raw/all_instagram_comments.csv", index=False, encoding="utf-8-sig")
    print(f"  💾 Sauvegarde : {len(df_temp)} textes au total")
    
    # Pause longue entre chaque compte pour éviter le blocage
    pause = random.uniform(30, 60)
    print(f"  ⏳ Pause de {int(pause)} secondes...")
    time.sleep(pause)

# ----------------------------------------
# SAUVEGARDE FINALE
# ----------------------------------------
df_final = pd.DataFrame(all_data)
df_final.to_csv("data/raw/all_instagram_comments.csv", index=False, encoding="utf-8-sig")

print(f"\n{'='*50}")
print(f"✅ SCRAPING INSTAGRAM TERMINÉ")
print(f"Total commentaires : {len(df_final)}")
print(f"\nRépartition par catégorie :")
print(df_final["category"].value_counts())
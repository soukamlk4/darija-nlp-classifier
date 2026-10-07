# DATASET_REPORT.md
## Projet NLP — Classification automatique de textes en Darija marocaine
### Mllouk Soukaina - Salma Lafnager

---

## 4.1 🌍 Sources des Données

### Plateformes utilisées

Les données ont été collectées à partir de deux plateformes principales :

- **YouTube** — commentaires sous les vidéos + transcriptions automatiques des vidéos
- **Instagram** — commentaires sous les posts et reels (tentative)

---

### Pourquoi ces sources ?

YouTube et Instagram sont les deux plateformes les plus utilisées par les créateurs de contenu marocains en Darija. Elles offrent une grande diversité de domaines thématiques (santé, politique, religion, cuisine, sport, économie) et permettent d'accéder à de la Darija **orale transcrite** (via les sous-titres automatiques YouTube) ainsi qu'à de la Darija **écrite informelle** (via les commentaires). Ces sources reflètent l'usage réel de la Darija dans des contextes numériques authentiques.

---

### Description des sources

#### YouTube — Commentaires

La principale source de données. Pour chaque domaine thématique, des vidéos de chaînes marocaines pertinentes ont été ciblées. Dans un premier temps, les chaînes officielles mentionnées dans le cahier des charges ont été utilisées lorsqu'elles existaient sur YouTube. Lorsque la chaîne n'existait pas ou ne produisait pas assez de données, des vidéos supplémentaires ont été sélectionnées **manuellement** en recherchant des contenus en Darija pour chaque domaine. Les commentaires ont été récupérés via l'**API YouTube Data v3**.

Les domaines couverts et le nombre de commentaires collectés sont les suivants :

| Domaine | Nombre de commentaires |
|---|---|
| Politics/Société | 18 815 |
| Business/Économie | 13 195 |
| Sports/Fitness | 12 316 |
| Medical/Santé | 8 157 |
| Food/Cuisine | 4 606 |
| Religion | 4 208 |
| **Total** | **61 297** |

> **Note :** Le domaine *Entertainment/Divertissement* n'a pas été collecté. En effet, les commentaires sous les vidéos de divertissement sont très génériques (réactions courtes, emojis, blagues) et il est difficile de déterminer à partir du seul commentaire qu'il appartient à ce domaine, contrairement aux autres domaines qui ont un vocabulaire thématique identifiable.

#### YouTube — Transcriptions

En complément des commentaires, des transcriptions automatiques de vidéos YouTube ont été collectées pour les domaines où les sous-titres automatiques en arabe étaient disponibles. Les vidéos ont été sélectionnées **manuellement**, en privilégiant celles dont les sous-titres automatiques étaient activés. Le texte transcrit a été découpé en chunks de 150 mots (minimum 20 mots par chunk) afin de constituer des unités textuelles exploitables. Ces données représentent la Darija **orale**, telle qu'utilisée par les créateurs de contenu.

#### Instagram — Commentaires (tentative échouée)

Une tentative de scraping des commentaires Instagram a été réalisée via la bibliothèque `instaloader`, en ciblant les comptes mentionnés dans le cahier des charges (ex. `sehti.fid9i9a`, `doctor.mouad`, `rachidachachi`, etc.). Cette approche n'a pas abouti : Instagram bloque systématiquement ce type d'accès automatisé, même avec authentification. Les données Instagram n'ont donc **pas pu être collectées** et l'ensemble du corpus repose sur YouTube.

---

### Date de collecte

La collecte des données a été effectuée au cours des **mois de mars/avril 2025**.

---

### Type de langue

Les textes collectés présentent les caractéristiques linguistiques suivantes :

- **Darija marocaine en alphabet arabe** : majoritaire dans les commentaires et les transcriptions
- **Darija en Arabizi (alphabet latin avec chiffres)** : fréquente dans les commentaires (ex. `7, 9, 3, 2`)
- **Forme mixte arabe/latin** : très courante sur les réseaux sociaux marocains (code-switching)
- **Darija mêlée de français** : présente notamment dans les domaines Business et Sports

---

### Observations

#### Qualité des données

- Les commentaires YouTube sont globalement de bonne qualité pour la Darija : le vocabulaire dialectal marocain est bien représenté, avec des structures orales et familières typiques des réseaux sociaux.
- Les transcriptions reflètent la Darija orale et sont plus longues et structurées que les commentaires. Elles contiennent cependant davantage d'arabe standard (MSA), notamment dans les domaines Religion et Politique, ce qui nécessite un filtrage lors du prétraitement.
- Certains commentaires sont trop courts ou ne contiennent que des emojis : ils sont filtrés lors de l'étape de nettoyage.

#### Problèmes rencontrés

- **Instagram inaccessible** : le scraping via `instaloader` a été bloqué par les mécanismes anti-bot d'Instagram, rendant impossible la collecte sur cette plateforme.
- **Commentaires désactivés** : certaines vidéos YouTube ont leurs commentaires désactivés, réduisant le volume collecté par vidéo.
- **Transcriptions absentes** : plusieurs vidéos n'ont pas de sous-titres automatiques disponibles en arabe, limitant le nombre de chunks de transcription récupérables.
- **Déséquilibre entre domaines** : la répartition finale n'est pas uniforme. Le domaine *Politics/Société* est surreprésenté (18 815 commentaires) tandis que *Religion* et *Food/Cuisine* sont sous-représentés (autour de 4 000 commentaires).
- **Bruit linguistique** : présence de spam, de commentaires en arabe standard, de commentaires en anglais ou en français pur, filtrés lors du nettoyage.

---

### Avantages de ces sources

- **Authenticité** : les données proviennent d'interactions réelles entre utilisateurs marocains, garantissant une Darija naturelle et non construite.
- **Diversité thématique** : les 6 domaines couverts offrent une large palette de vocabulaires et de registres.
- **Diversité des types de texte** : la combinaison commentaires (Darija écrite courte) et transcriptions (Darija orale longue) enrichit le corpus.
- **Accessibilité via API officielle** : l'utilisation de l'API YouTube Data v3 assure une collecte stable, reproductible et conforme aux conditions d'utilisation.
- **Volume conséquent** : plus de 61 000 commentaires collectés, offrant une base solide pour la labellisation et l'entraînement des modèles.

---

## 4.2 🧹 Collecte & Nettoyage

### Méthode de collecte

**API YouTube Data v3 (principale)**
Tous les commentaires YouTube ont été récupérés via l'API officielle YouTube Data v3 (`youtube.commentThreads().list`), en itérant sur les pages de résultats (`nextPageToken`) avec un maximum de 100 commentaires par requête. Pour chaque domaine, deux types de fichiers ont été générés : les commentaires et les transcriptions. Les vidéos ont été identifiées soit en cherchant les chaînes mentionnées dans le cahier des charges lorsqu'elles existaient sur YouTube, soit par **sélection manuelle** de vidéos pertinentes en Darija lorsque les chaînes étaient absentes ou insuffisantes.

**Transcriptions automatiques YouTube**
Les sous-titres automatiques en arabe (`languages=['ar']`) ont été récupérés via la bibliothèque `youtube-transcript-api`. Le texte complet de chaque transcription a ensuite été découpé en **chunks de 150 mots**, avec un minimum de 20 mots par chunk pour écarter les segments trop courts. Seules les vidéos disposant de sous-titres automatiques activés ont pu être traitées.

**Instagram (tentative)**
Une tentative de scraping via `instaloader` a été menée sur les comptes indiqués dans le cahier des charges. Elle n'a pas abouti en raison du blocage systématique par les mécanismes anti-bot d'Instagram. Aucune donnée Instagram n'est donc présente dans le corpus final.

**Combinaison et mélange**
Une fois tous les fichiers par domaine générés, ils ont été fusionnés avec le script `combine_domains.py` (un premier dédoublonnage sur le texte brut y est effectué), puis commentaires et transcriptions nettoyés ont été combinés et mélangés aléatoirement avec `mix_dataset.py` (`random_state=42` pour la reproductibilité).

---

### Étapes de nettoyage

Le nettoyage a été appliqué séparément aux commentaires (`etape2_preprocessing1.ipynb`) et aux transcriptions (`etape2_preprocessing1_transcr.ipynb`), avec des pipelines adaptées à chaque type de texte.

#### Étape 1 — Nettoyage de base

Appliqué à tous les textes (commentaires et transcriptions) :

- Suppression des URLs (`http://`, `www.`) et des mentions `@user`
- Suppression des hashtags `#`
- Remplacement des emojis par un espace (via la bibliothèque `emoji`)
- Conservation uniquement des caractères arabes (Unicode `\u0600–\u06FF`), latins, chiffres et ponctuation légère (`،,.!?;:`)
- Réduction des répétitions abusives de caractères : toute séquence de 4+ caractères identiques réduite à 3 (ex. `هههههه` → `ههه`)
- Nettoyage des espaces multiples et des chaînes vides

Pour les **transcriptions uniquement**, une étape supplémentaire de suppression des patterns sonores a été appliquée : annotations audio `[موسيقى]`, `[ضحك]`, `[تصفيق]` (musique, rires, applaudissements), ainsi que les formules de call-to-action (`اشترك`, `لايك`, `subscribe`), les mentions de sponsors (`برعاية`, `sponsored`) et les formules d'outro (`نشوفكم في فيديو`).

#### Étape 2 — Suppression des doublons

Après le nettoyage de base, les doublons ont été supprimés sur la colonne `text_clean` (texte après nettoyage), pour éviter de garder des commentaires identiques après normalisation même s'ils étaient légèrement différents à l'état brut.

#### Étape 3 — Filtrage avancé

Quatre filtres ont été appliqués pour ne conserver que les textes linguistiquement exploitables en Darija :

**Filtre 1 — Contenu vulgaire**
Détection et suppression des commentaires contenant du vocabulaire vulgaire ou offensant, à partir d'une liste de termes en Arabizi et en arabe (ex. `zebi`, `9ahba`, `عاهرة`, `قحبة`, etc.).

**Filtre 2 — Dominance français/anglais**
Suppression des textes sans caractères arabes dont au moins 40 % des tokens (commentaires) ou 50 % (transcriptions) appartiennent à un lexique français/anglais (`je`, `tu`, `the`, `is`, `merci`, `bonjour`…), sans aucun marqueur de Darija en alphabet latin (`bzaf`, `hada`, `machi`, `walou`…).

**Filtre 3 — Dominance arabe standard (MSA)**
Suppression des textes contenant 2+ marqueurs MSA (`يجب`, `ينبغي`, `الذي`, `التي`, `لقد`, `تم`…) sans aucun marqueur Darija. Le seuil a été légèrement relevé pour les transcriptions (3+ marqueurs MSA) car elles sont naturellement plus longues et peuvent mélanger Darija et MSA dans un même chunk.

**Filtre 4 — Contenu non informatif / parasites**
- *Commentaires* : suppression des textes de moins de 2 mots, des textes composés uniquement de chiffres ou de ponctuation, des commentaires génériques ultra-courts (`bravo`, `شكرا`, `machallah`) et des call-to-action (`subscribe`, `partage`, `لايك`…).
- *Transcriptions* : suppression des segments de moins de 5 mots et des chunks ne contenant que des annotations audio ou des formules parasites (sponsor, outro, CTA).

---

### Analyse exploratoire

Les notebooks incluent une analyse exploratoire complète des données nettoyées :

- **Longueur des textes par source** : calcul de la moyenne, médiane, min et max du nombre de mots. Les transcriptions sont structurellement plus longues (chunks de 150 mots) comparées aux commentaires qui sont généralement courts.
- **Distribution arabe vs latin par catégorie** : calcul du pourcentage de caractères arabes et latins par domaine, révélant les variations de code-switching selon les thématiques.
- **Mots et bigrammes fréquents** : top 30 des unigrammes et top 20 des bigrammes sur l'ensemble du corpus nettoyé.
- **Détection du code-switching** : identification des textes contenant à la fois des caractères arabes et latins. La Darija marocaine présente un fort taux de mélange de scripts, particulièrement dans les domaines Business et Sports.

---

### Normalisation

Conformément aux recommandations du cahier des charges, la normalisation a été **volontairement minimale** afin de préserver la richesse linguistique de la Darija. Aucune normalisation orthographique (unification de l'écriture `واش` / `wach` / `w3ch`) n'a été appliquée. Le texte original a été conservé à l'exception des suppressions de bruit décrites ci-dessus.

---

## 4.3 🏷️ Annotation du Gold Dataset

### Comment le Gold Dataset a été créé

La constitution du Gold Dataset s'est déroulée en plusieurs étapes itératives, combinant extraction ciblée, enrichissement qualitatif et annotation manuelle via un outil dédié.

#### Étape 1 — Extraction initiale des 1 000 lignes

À partir du dataset fusionné `dataset_all_mixed.csv` (50 386 textes), les 1 000 premières lignes ont été extraites pour constituer la base du Gold Standard. À chaque ligne a été ajoutée une colonne `labeled_ia`, générée automatiquement par un script Python via un simple mapping de la catégorie source vers la classe finale :

```python
mapping = {
    'Politics/Société':  'Politics_Society',
    'Business/Économie': 'Business_Economy',
    'Sports/Fitness':    'Sports',
    'Medical/Santé':     'Health_Science',
    'Food/Cuisine':      'Cuisine',
    'Religion':          'Religion'
}
df["labeled_ia"] = df["category"].map(mapping)
```

> **Important :** `labeled_ia` n'est pas une annotation par intelligence artificielle — c'est une suggestion automatique basée sur la chaîne source d'extraction. Elle sert uniquement d'aide à la labellisation manuelle pour accélérer le processus.

#### Étape 2 — Enrichissement par exemples de qualité

Après observation dans Label Studio, il est apparu que la majorité des 1 000 lignes initiales contenaient des commentaires non classifiables (formules de politesse, emojis, spams, hors-sujet). Pour garantir un Gold Standard représentatif et utile pour le LLM, le dataset a été enrichi avec des exemples ciblés par classe :

- **20 commentaires longs (≥ 10 mots) avec mots-clés thématiques** par classe sous-représentée
- **4 à 10 transcriptions YouTube** par classe, selon les besoins

Un script Python avec filtrage par mots-clés (en Darija arabe, Arabizi et français) a été utilisé pour s'assurer que les commentaires sélectionnés avaient un contenu thématique réel. Les classes enrichies prioritairement : `Food/Cuisine`, `Religion`, `Medical/Santé` et `Sports/Fitness`.

#### Étape 3 — Annotation manuelle avec Label Studio

Le fichier `gold_standard_to_annotate.csv` a été importé dans **Label Studio**, un outil open-source d'annotation de données. Le projet a été configuré avec les 7 classes suivantes :

| Classe | Description |
|---|---|
| `Politics_Society` | Politique, société, débats citoyens |
| `Business_Economy` | Économie, finance, entrepreneuriat |
| `Sports` | Sport, fitness, entraînement |
| `Health_Science` | Santé, médecine, conseils médicaux |
| `Cuisine` | Recettes, cuisine, gastronomie |
| `Religion` | Islam, pratiques religieuses, contenu spirituel |
| `Nonsense` | Commentaires sans valeur thématique |

Pour chaque texte affiché, l'annotateur disposait de la suggestion `labeled_ia` comme point de départ et pouvait valider le label suggéré s'il était correct, le corriger si le texte ne correspondait pas à la source, ou assigner `Nonsense` pour tout texte sans contenu exploitable.

#### Étape 4 — Fusion et finalisation

Après export JSON depuis Label Studio, un script de fusion a été appliqué pour reconstituer le Gold Standard complet. Les textes annotés manuellement conservent le label humain, les textes non touchés dans Label Studio conservent leur `labeled_ia` comme `label_final`. Les `Nonsense` ont ensuite été réduits à 200 exemplaires (sur 572 initiaux) pour éviter un déséquilibre trop fort.

**Distribution finale du Gold Standard (`gold_final_balanced.csv`) :**

| Classe | Nombre d'exemples |
|---|---|
| Nonsense | 200 |
| Politics_Society | 160 |
| Sports | 94 |
| Business_Economy | 71 |
| Health_Science | 65 |
| Cuisine | 61 |
| Religion | 48 |
| **TOTAL** | **699** |

---

### Qui a annoté ?

L'annotation manuelle a été réalisée par les membres du groupe, en utilisant Label Studio en local (`http://localhost:8080`). Chaque texte a été examiné individuellement par un annotateur humain qui prenait la décision finale de la classe, indépendamment de la suggestion automatique.

---

### Règles d'annotation utilisées

**1. Règle du contenu dominant**
La classe attribuée est celle du **sujet principal** du texte, pas de la chaîne source. Un commentaire sur une vidéo Business qui parle de santé → `Health_Science`.

**2. Règle des mots religieux vs contenu religieux**
Les formules de politesse contenant des termes religieux (`تبارك الله`, `الله يرحم والديك`, `إن شاء الله`) sont classées `Nonsense` — elles ne parlent pas de religion comme sujet. La classe `Religion` est réservée aux textes qui **traitent** de l'islam, de la pratique religieuse ou de questions théologiques.

**3. Règle de la longueur minimale**
Les textes de moins de 3 mots sont systématiquement classés `Nonsense` (absence de contexte classifiable).

**4. Règle du français / anglais générique**
Un commentaire 100% en français ou en anglais sans contenu thématique clair (`Merci beaucoup`, `Super vidéo`, `Bravo`) → `Nonsense`. En revanche, si le contenu est thématiquement identifiable (`Cette recette est excellente`) → classe correspondante.

**5. Règle des transcriptions**
Les transcriptions YouTube sont classées dans la catégorie de la chaîne source par défaut, sauf incohérence évidente avec le contenu.

**Exemples concrets de décisions d'annotation :**

| Texte | Décision | Justification |
|---|---|---|
| `تبارك الله عليك اخي الكريم الله يرحم الوالدين` | Nonsense | Formule de politesse, pas de contenu Religion |
| `الاسلام قال ان الضريبة هي فعلا اعتداء على المواطن` | Religion | Texte qui traite de l'islam comme sujet principal |
| `Daba wach 7:45 nas mtwsta homa ojara2 hadchi maymknch` | Politics_Society | Commentaire critique sur la société/actualité |
| `Khoya bghit nt3alam motion graphic` | Nonsense | Question personnelle hors-sujet, inclassable |

---

### Difficultés rencontrées

**1. Volume élevé de Nonsense**
Plus de 50% des commentaires collectés bruts étaient des `Nonsense` : formules génériques, emojis, insultes, ou commentaires hors-sujet. Cela a nécessité un enrichissement ciblé du dataset pour garantir suffisamment d'exemples positifs par classe.

**2. Ambiguïté des textes mixtes**
Certains textes mélangent plusieurs thématiques (ex: un commentaire sur une vidéo business citant des versets coraniques). La décision de classer selon le sujet dominant reste subjective.

**3. Religion vs Nonsense**
La frontière entre un contenu religieux réel et une simple formule de politesse en arabe est culturellement subtile. Une règle explicite a dû être formalisée pour garantir la cohérence.

**4. Export partiel depuis Label Studio**
Label Studio n'exporte que les textes ayant reçu une annotation manuelle. Les textes non touchés (environ 400 sur 1 000) nécessitaient un script de fusion pour les réintégrer avec leur `labeled_ia` comme label final.

**5. Sous-représentation de la Religion**
Malgré les efforts d'enrichissement, la classe `Religion` reste la moins représentée (48 exemples) car les contenus authentiquement religieux en Darija sont rares : les utilisateurs tendent à basculer vers l'arabe standard (MSA) pour les sujets religieux.

---

## 4.4 🤖 Labellisation Semi-Automatique avec IA

### Méthode utilisée

La labellisation semi-automatique a été réalisée via une approche **navigateur automatisé 
avec injection de prompts**, sans utilisation d'API payante. La pipeline repose sur deux 
scripts Tampermonkey exécutés dans Google Chrome :

- **Script 1 — Gemini Batch Darija Classification (V1.0)** : injecte automatiquement 
les textes à annoter dans l'interface Gemini et envoie le prompt de classification.
- **Script 2 — Gemini Sidebar Extractor to ZIP (V1.4)** : extrait les réponses générées 
par Gemini depuis la sidebar des conversations et les télécharge sous forme de fichiers `.txt`.

### Nom exact du modèle utilisé

**Google Gemini 2.0 Flash** — accessible via l'interface web `https://gemini.google.com`

### Description du processus

**Étape 1 — Préparation des fichiers batch**
À partir du dataset filtré (`filtered_finale_data_enfin_LLM.csv`, environ 49 000 textes), 
un script Python a découpé les données en fichiers JSON de 200 textes chacun 
(`BATCH_SIZE = 200`, générant ~245 fichiers JSON dans le dossier `batch_files/`).

**Étape 2 — Injection automatique dans Gemini via Tampermonkey**
Le script Tampermonkey charge les fichiers JSON depuis une base IndexedDB locale, 
construit le prompt complet (instructions + exemples few-shot + textes à annoter), 
l'injecte dans l'éditeur de Gemini, et envoie automatiquement la requête. 
Après chaque réponse, un nouvel onglet est ouvert pour le fichier suivant.

**Étape 3 — Prompt de classification (Few-Shot)**
Le prompt envoyé à Gemini est structuré en trois blocs :

*Bloc 1 — Définition des 7 labels :*

| Label | Description |
|---|---|
| `Politics_Society` | politique, société, gouvernement, actualité, corruption, élections |
| `Business_Economy` | économie, argent, business, investissement, impôts, salaires |
| `Sports_Fitness` | football, matchs, équipes (Raja, Wydad…), compétitions, fitness |
| `Health_Science` | santé, médecine, maladies, traitements, médicaments |
| `Food_Cuisine` | recettes, plats marocains, ingrédients, préparation des aliments |
| `Religion` | islam, prière, coran, hadith, ramadan, mosquée |
| `Inclassable` | opinions, encouragements, questions, spam, textes trop courts, hors sujet |

*Bloc 2 — Exemples few-shot* extraits du Gold Standard (7 par classe = 49 exemples) :

```json
{"text": "الوداد ضرب الرجاء 3-1 هدف زوين من النصيري", "label": "Sports_Fitness"}
{"text": "الضريبة على المقاول الذاتي واصلة ل 30%", "label": "Business_Economy"}
{"text": "وصفة الكسكس ديال الجدة دجاج بزاف ديال البصل", "label": "Food_Cuisine"}
{"text": "الصلاة عماد الدين والفرق ما بين المسلم والكافر", "label": "Religion"}
{"text": "اصبح الطب في المغرب تجارة", "label": "Health_Science"}
{"text": "أحسن الله إليك", "label": "Inclassable"}
{"text": "ايران اكبر عدو للمغرب بسبب قضية الصحراء", "label": "Politics_Society"}
```

*Bloc 3 — Règles explicites pour les cas ambigus :*
- Opinions, avis personnels, réactions subjectives → `Inclassable`
- Encouragements, félicitations, formules de bienveillance → `Inclassable`
- Questions explicites sans domaine thématique dense → `Inclassable`
- Texte publicitaire ou spam → `Inclassable`
- Texte trop court ou générique → `Inclassable`
- Texte en français/anglais sans contenu thématique → `Inclassable`
- Sujet mixte → classe du sujet dominant

**Étape 4 — Extraction et consolidation des réponses**
Les réponses de Gemini ont été extraites via le script ZIP sous forme de fichiers `.txt`. 
Un script Python de traitement itératif parse le JSON contenu dans chaque fichier `.txt`, 
extrait les labels, et les accumule dans un fichier CSV unique (`annotated_by_llm.csv`). 
Le traitement s'effectue par lots de 10 fichiers à la fois, avec déduplication automatique 
à chaque ajout.

**Étape 5 — Fusion finale**
Les textes classés `Inclassable` par Gemini regroupent toutes les intentions non thématiques 
(opinions, encouragements, questions, spam, bruit). Cette classe unique simplifie le schéma 
et améliore la séparabilité des classes thématiques lors de la modélisation.

**Distribution finale annotée par Gemini :**

| Classe | Nombre d'exemples |
|---|---|
| Inclassable | 8 430 |
| Politics_Society | 4 549 |
| Sports_Fitness | 4 440 |
| Business_Economy | 3 119 |
| Religion | 3 012 |
| Health_Science | 2 889 |
| Food_Cuisine | 2 516 |
| **TOTAL** | **~29 000** |

---

## 4.5 🔍 Vérification et Validation

### Méthode de vérification

L'ensemble du processus de vérification et de validation du dataset final a été réalisé 
via **Label Studio**, en local (`http://localhost:8080`). Les 23 606 textes retenus ont 
fait l'objet d'une relecture humaine en suivant le même protocole d'annotation que celui 
utilisé pour le Gold Standard : chaque texte est affiché avec son label LLM proposé, 
et l'annotateur peut valider, corriger ou rejeter ce label.

### Qui a vérifié ?

La vérification a été réalisée par les membres du groupe, en procédant à une relecture 
par **échantillonnage stratifié** : chaque classe a été contrôlée indépendamment pour 
s'assurer de la cohérence inter-classes. Les classes thématiques à haute précision 
confirmée (`Sports_Fitness`, `Food_Cuisine`, `Health_Science`) ont fait l'objet d'une 
vérification plus légère, tandis que la classe `Inclassable` a été prioritisée.

### Protocole appliqué

1. Import du dataset annoté (`annotated_by_llm.csv`) dans Label Studio au format CSV.
2. Affichage du texte brut et du label proposé par Gemini (`label_initial`).
3. Validation, correction ou rejet par l'annotateur humain.
4. Export des annotations finales depuis Label Studio (format JSON puis reconversion CSV).
5. Fusion finale : `label_final = label_studio si annoté, sinon label_initial`.

---

## 4.6 📊 Analyse des Erreurs de l'IA

Le code de détection des désaccords (`label_initial != label_studio`) a permis 
d'identifier **4 835 erreurs** sur 23 606 textes. L'analyse révèle trois grands 
types d'erreurs.

---

### Type 1 — Mauvaise classification thématique → Inclassable

L'erreur dominante est la **sur-classification vers `Inclassable`** : le LLM détecte 
une réaction personnelle ou une formule de politesse et ignore le contenu thématique réel.

| Classe initiale (LLM) | Reclassée en `Inclassable` |
|---|---|
| Sports_Fitness | 1 008 |
| Politics_Society | 734 |
| Health_Science | 545 |
| Food_Cuisine | 511 |
| Business_Economy | 370 |
| Religion | 358 |

**Exemples réels :**

| Texte original | Label LLM | Label humain | Analyse |
|---|---|---|---|
| `عفاك كلمة إصلاح مستفزة... من افضل استعمال كلمة تغيير` | `Business_Economy` | `Inclassable` | Réaction critique au vocabulaire |
| `Footix de sortie ...` | `Sports_Fitness` | `Inclassable` | Commentaire évaluatif sans contexte sportif explicite |
| `دكتور اكن لكم كل الاحترام ولكن الأطباء في المغرب لايحترمون المرضى` | `Health_Science` | `Politics_Society` | Critique institutionnelle du système médical |
| `واش اخويا من نيتك ولد انت وخرج لينا شي بطل راه أغلبية الشعب مضارب` | `Business_Economy` | `Politics_Society` | Contenu socio-politique déguisé en commentaire économique |

---

### Type 2 — Confusion inter-thématiques

**Confusion `Religion` ↔ `Inclassable`** (358 cas)

Les formules de bienveillance religieuses omniprésentes en Darija sont classées 
`Religion` par le LLM alors qu'elles ne traitent pas de religion comme sujet.

| Texte original | Label LLM | Label humain | Analyse |
|---|---|---|---|
| `جزاك الله خيرا يا شيخنا` | `Religion` | `Inclassable` | Formule de remerciement, pas de contenu religieux |
| `أحبك في الله أستاذ بارك الله في عمرك` | `Religion` | `Inclassable` | Déclaration d'affection avec formules religieuses |
| `ممم ما شاء الله` | `Food_Cuisine` | `Inclassable` | Expression d'admiration générique, aucun contenu culinaire |

---

### Type 3 — Sarcasme et ironie non détectés

| Texte original | Label LLM | Label humain | Analyse |
|---|---|---|---|
| `ههه بغا ثاني اشرح لأنشيلوتي كيفاش غادي يلعب ههه` | `Sports_Fitness` | `Inclassable` | Moquerie ironique — `ههه` signale le sarcasme |
| `مش هو الدعارة والجنس ههه كيراعي للسطولة كابتن مصطفى` | `Politics_Society` | `Inclassable` | Ton moqueur, critique ironique |
| `kat3arrrad l 7amalat inti9adat nta howa trump hhh` | `Politics_Society` | `Inclassable` | Comparaison ironique en Arabizi |

**Observation :** Le marqueur typique du sarcasme en Darija digitale est la répétition 
de `ههه` ou `hhh`. Ces signaux pragmatiques sont ignorés par Gemini 2.0 Flash.

---

### Bilan quantitatif des erreurs

| Type d'erreur | Nb de cas estimés | % des 4 835 erreurs |
|---|---|---|
| Sur-classification vers `Inclassable` | ~3 526 | ~72.9% |
| Confusion inter-thématiques (Politics↔Business, Health↔Politics…) | ~872 | ~18.0% |
| Textes courts / Arabizi mal interprétés | ~437 | ~9.0% |
| **TOTAL** | **4 835** | **100%** |

---

## 4.7 📈 Statistiques de Performance

### Avant correction (labels LLM bruts)

| Indicateur | Valeur |
|---|---|
| **Nombre total de textes soumis au LLM** | ~49 000 |
| **Nombre de textes retenus dans le dataset final** | 23 606 |
| **Nombre de labels divergents détectés** | 4 835 |
| **Taux de correction (désaccord LLM ↔ humain)** | **20.48%** |
| **Accuracy globale (labels identiques)** | **79.52%** |

> **Interprétation clé :** 1 commentaire sur 5 a dû être redressé manuellement, 
ce qui démontre l'indispensabilité de la phase de validation humaine via Label Studio.

### Performances par classe (avant correction manuelle)

| Classe | Précision | Rappel | F1-score | Support |
|---|---|---|---|---|
| Business_Economy | 0.99 | 0.73 | 0.85 | 2 943 |
| Food_Cuisine | 1.00 | 0.76 | 0.86 | 2 371 |
| Health_Science | 1.00 | 0.75 | 0.85 | 2 717 |
| Inclassable | 0.54 | 0.90 | 0.68 | 2 057 |
| Politics_Society | 0.89 | 0.79 | 0.84 | 4 148 |
| Religion | 0.97 | 0.82 | 0.89 | 2 844 |
| Sports_Fitness | 1.00 | 0.73 | 0.84 | 4 149 |
| **Accuracy globale** | | | **0.80** | **23 606** |
| **Macro avg** | 0.91 | 0.78 | 0.83 | |
| **Weighted avg** | 0.91 | 0.80 | 0.83 | |

**Lecture des résultats :**
- Les classes thématiques pures (`Food_Cuisine`, `Health_Science`, `Sports_Fitness`, 
`Business_Economy`) atteignent une précision quasi-parfaite (≥ 0.99) : le LLM est 
très fiable quand il assigne ces labels.
- Le rappel plus faible (~0.73–0.76) indique qu'il en rate une partie en les 
sur-classifiant vers `Inclassable`.
- La classe `Inclassable` présente une précision de **0.54** : elle capte trop 
largement des textes qui ont en réalité un contenu thématique identifiable.

### Après correction (via Label Studio)

| Indicateur | Valeur |
|---|---|
| **Textes vérifiés et corrigés manuellement** | 4 835 |
| **Taux de correction appliqué** | 20.48% |
| **Classe la plus fiable après correction** | `Sports_Fitness`, `Food_Cuisine`, `Health_Science` |
| **Classe la plus incertaine après correction** | `Inclassable` |

---

## 4.8 🔧 Correction des Erreurs

### Processus de correction

Après la labellisation semi-automatique par Gemini 2.0 Flash, l'intégralité du dataset 
annoté a été importée dans **Label Studio** pour une phase de vérification et correction 
humaine systématique.

Le protocole appliqué :

1. Import du dataset annoté (`annotated_by_llm.csv`) dans Label Studio au format CSV.
2. Affichage texte par texte avec le label proposé par le LLM (`label_initial`).
3. Décision humaine : valider, corriger vers une autre classe, ou rejeter.
4. Export JSON depuis Label Studio, puis reconversion CSV.
5. Fusion finale : `label_final = label_studio si annoté, sinon label_initial`.

Cette phase a produit **4 835 modifications** sur 23 606 textes, soit un taux de 
correction de **20.48%**.

---

### Difficultés rencontrées

**1. Volume à vérifier important**
Avec 23 606 textes à passer en revue, une vérification exhaustive était humainement 
irréalisable. Une stratégie d'**échantillonnage stratifié** a été adoptée : les classes 
à faible précision (`Inclassable`) ont été prioritisées. Les classes à haute précision 
confirmée (`Sports_Fitness`, `Food_Cuisine`, `Health_Science`) ont fait l'objet d'une 
vérification plus légère.

**2. Commentaires avec thème clair mais forme ambiguë**

| Texte | Difficulté | Décision finale |
|---|---|---|
| `ههه بغا ثاني اشرح لأنشيلوتي كيفاش غادي يلعب ههه` | Ton ironique sur le football | `Inclassable` — la forme prime |
| `دكتور اكن لكم كل الاحترام ولكن الأطباء في المغرب لايحترمون المرضى` | Health ou Politics ? | `Politics_Society` — critique institutionnelle |
| `majwbtich 3la la question حل ولا فخّ؟` | Question sur business | `Inclassable` — interpellation rhétorique |

**3. Textes sans mot-clé explicite**

| Texte | Thème compris | Décision |
|---|---|---|
| `Mas maktfr7x b ta3adol` | Réaction à un match | `Inclassable` — trop implicite |
| `ريس الوندال` | Référence politique | `Inclassable` — trop court hors contexte |

**4. Gestion de l'encodage**
La cohabitation de l'alphabet arabe et des caractères latins a provoqué des corruptions 
d'affichage, résolues par l'encodage strict `utf-8-sig`.

---

## 4.9 📊 Statistiques du Dataset Final

### Volume et format

| Indicateur | Valeur |
|---|---|
| **Nombre total d'exemples** | **23 606** |
| **Nombre de classes** | **7** |
| **Format** | CSV, encodage UTF-8 |

---

### Distribution finale des classes

| Classe | Nombre d'exemples | Proportion (%) |
|---|---|---|
| Inclassable | 8 430 | 35.71% |
| Politics_Society | 3 711 | 15.72% |
| Sports_Fitness | 3 027 | 12.82% |
| Religion | 2 426 | 10.28% |
| Business_Economy | 2 176 | 9.22% |
| Health_Science | 2 034 | 8.62% |
| Food_Cuisine | 1 803 | 7.64% |
| **TOTAL** | **23 606** | **100%** |

---

### Type d'écriture (script)

| Script | Nombre | Proportion (%) |
|---|---|---|
| Arabe (alphabet arabe) | 19 762 | 83.72% |
| Latin (Arabizi + français + anglais) | 3 844 | 16.28% |
| **TOTAL** | **23 606** | **100%** |

---

### Diagnostic du déséquilibre

| Indicateur | Valeur |
|---|---|
| Classe majoritaire | `Inclassable` (8 430 exemples) |
| Classe thématique majoritaire | `Politics_Society` (3 711 exemples) |
| Classe thématique minoritaire | `Food_Cuisine` (1 803 exemples) |
| **Ratio thématique (sans Inclassable)** | **2.09x** ✅ déséquilibre modéré |
| **Ratio global (avec Inclassable)** | **4.67x** — naturel et attendu |

Le ratio de **2.09x** entre les classes thématiques indique un dataset bien équilibré 
sur son cœur thématique. La classe `Inclassable` représente naturellement la majorité 
des commentaires YouTube — c'est un reflet fidèle de la réalité des données sociales.

**Traitements appliqués lors de la modélisation :**
- `class_weight='balanced'` pour compenser le déséquilibre résiduel
- Les 6 classes thématiques ne nécessitent pas de sur-échantillonnage (ratio ≤ 2.09x)

---

### ⚖️ Diagnostic du Déséquilibre des Classes

| Indicateur | Valeur |
|---|---|
| Classe majoritaire globale | `Inclassable` (8 430 exemples) |
| Classe thématique majoritaire | `Politics_Society` (3 711 exemples) |
| Classe thématique minoritaire | `Food_Cuisine` (1 803 exemples) |
| **Ratio thématique (sans Inclassable)** | **2,09x** ✅ |
| **Ratio global (avec Inclassable)** | **4,67x** ⚠️ naturel et attendu |

**Conclusion du diagnostic :** Le dataset ne souffre d'aucun déséquilibre sévère 
sur ses 6 classes thématiques. Le ratio de 2,09x entre `Politics_Society` et 
`Food_Cuisine` est largement en dessous du seuil critique de 10x fixé dans la 
littérature NLP. La proportion élevée de la classe `Inclassable` (35,71%) est 
un reflet fidèle de la réalité des commentaires YouTube — la majorité des 
interactions sociales ne portent pas de contenu thématique dense.

**Traitements appliqués lors de la modélisation :**
- `class_weight='balanced'` sur tous les classifieurs scikit-learn
- Aucun sur-échantillonnage nécessaire sur les classes thématiques (ratio ≤ 2,09x)
---

## 4.13 ⚠️ Limites

L’analyse approfondie des erreurs de notre pipeline met en évidence trois barrières structurelles inhérentes au traitement de la Darija numérique :

* **Biais de plateforme (YouTube-Centric) :** L'intégralité du corpus provient de l'écosystème YouTube. Les structures syntaxiques sont intimement liées aux codes de cette plateforme (repères temporels/timestamps, interpellations directes des créateurs). De plus, l'IA a parfois hérité d'un biais contextuel lié aux chaînes d'extraction (un commentaire neutre sous une vidéo médicale dérivait indûment vers `Health_Science` par pur effet de corrélation de la source).
* **Limites linguistiques et variabilité de la Darija :** L'absence de standardisation orthographique en Darija et en Arabizi engendre une multiplication inutile de tokens distincts pour le dictionnaire (ex: *"Zouina"*, *"zwina"*, *"zwiiina"*), diluant l'efficacité sémantique du modèle. De plus, le *Code-Switching* agressif (mélange intra-phrastique de Darija, Français et Anglais) sature parfois le contexte linguistique.
* **Limites du modèle face aux structures hybrides (Thème vs Intention) :** C'est la limite la plus lourde constatée. Lorsqu'un commentaire est formulé sous forme de **Question** ou de **Sarcasme** tout en traitant d'un domaine métier précis (ex: une pique ironique sur une tactique de football), Gemini 2.0 Flash échoue à équilibrer les deux aspects. Le modèle se laisse également tromper par le second degré local en prenant au premier degré des expressions ironiques marocaines qui utilisent un vocabulaire élogieux ou religieux pour critiquer (ex: *"تبارك الله على الفاهم ديالنا"*).

---

## 4.14 🚀 Améliorations

Pour pallier les limites observées et faire progresser ce projet vers une version industrielle, trois axes d'améliorations prioritaires sont préconisés :

* **Au niveau des Données (Diversification et Normalisation) :** Extraire des données en dehors de l'écosystème YouTube (forums communautaires marocains ou sous-serveurs Reddit locaux) pour casser le biais de format court. Intégrer un pipeline de translittération en amont afin de convertir systématiquement l'écriture latine et ses chiffres phonétiques (3, 7, 9) vers un alphabet arabe unifié, réduisant ainsi drastiquement la sparsité du vocabulaire.
* **Au niveau de l'Annotation (Bascule Multi-Label) :** Pour résoudre le conflit persistant entre le thème et l'intention, le schéma de données doit évoluer vers du multi-label. Chaque texte recevrait ainsi deux étiquettes orthogonales et indépendantes : une étiquette *Sémantique/Métier* (ex: `Business_Economy`) et une étiquette *Comportementale/Intention* (ex: `Question` ou `Sarcasme`).
* **Au niveau du Modèle IA (Spécialisation) :** Remplacer l'approche Few-Shot globale par un processus de Fine-Tuning supervisé sur un modèle open-source d'échelle intermédiaire (type Llama-3-8B) en utilisant notre Gold Standard comme base d'alignement. Privilégier également des modèles encodeurs pré-entraînés spécifiquement sur le dialecte maghrébin, tels que *MarBERT* ou *DarijaBERT*, qui possèdent nativement une meilleure sensibilité aux nuances culturelles et à l'argot digital marocain.

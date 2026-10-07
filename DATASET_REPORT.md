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

La labellisation semi-automatique a été réalisée via une approche **navigateur automatisé avec injection de prompts**, sans utilisation d'API payante. La pipeline repose sur deux scripts Tampermonkey exécutés dans Google Chrome :

- **Script 1 — Gemini Batch Darija Classification (V1.0)** : injecte automatiquement les textes à annoter dans l'interface Gemini et envoie le prompt de classification.
- **Script 2 — Gemini Sidebar Extractor to ZIP (V1.4)** : extrait les réponses générées par Gemini depuis la sidebar des conversations et les télécharge sous forme de fichiers `.txt`.

### Nom exact du modèle utilisé

**Google Gemini 2.0 Flash** — accessible via l'interface web `https://gemini.google.com` (modèle : `gemini-2.0-flash`)

### Description du processus

**Étape 1 — Préparation des fichiers batch**
À partir du dataset filtré (`filtered_finale_data_enfin_LLM.csv`, environ 49 000 textes), un script Python a découpé les données en fichiers JSON de 200 textes chacun (`BATCH_SIZE = 200`, générant ~245 fichiers JSON dans le dossier `batch_files/`).

**Étape 2 — Injection automatique dans Gemini via Tampermonkey**
Le script Tampermonkey charge les fichiers JSON depuis une base IndexedDB locale, construit le prompt complet (instructions + exemples few-shot + textes à annoter), l'injecte dans l'éditeur de Gemini, et envoie automatiquement la requête. Après chaque réponse, un nouvel onglet est ouvert pour le fichier suivant.

**Étape 3 — Prompt de classification (Few-Shot)**
Le prompt envoyé à Gemini est structuré en trois blocs :

*Bloc 1 — Définition des labels :*

| Label | Description |
|---|---|
| `Politics_Society` | politique, société, gouvernement, actualité, corruption, élections |
| `Business_Economy` | économie, argent, business, investissement, impôts, salaires |
| `Sports` | football, matchs, équipes (Raja, Wydad…), compétitions |
| `Health_Science` | santé, médecine, maladies, traitements, médicaments |
| `Cuisine` | recettes, plats marocains, ingrédients, préparation des aliments |
| `Religion` | islam, prière, coran, hadith, ramadan, mosquée |
| `Nonsense` | commentaires génériques, spam, textes trop courts, hors sujet |

*Bloc 2 — Exemples few-shot* extraits du Gold Standard (7 par classe = 49 exemples) :
```json
{"text": "الوداد ضرب الرجاء 3-1 هدف زوين من النصيري", "label": "Sports"}
{"text": "الضريبة على المقاول الذاتي واصلة ل 30%", "label": "Business_Economy"}
{"text": "وصفة الكسكس ديال الجدة دجاج بزاف ديال البصل", "label": "Cuisine"}
{"text": "الصلاة عماد الدين والفرق ما بين المسلم والكافر", "label": "Religion"}
{"text": "اصبح الطب في المغرب تجارة", "label": "Health_Science"}
{"text": "أحسن الله إليك", "label": "Nonsense"}
{"text": "ايران اكبر عدو للمغرب بسبب قضية الصحراء", "label": "Politics_Society"}
```

*Bloc 3 — Règles explicites pour les cas ambigus :*
- Mots religieux utilisés comme formule de politesse → `Nonsense`
- Texte trop court ou générique → `Nonsense`
- Texte en français/anglais sans contenu thématique → `Nonsense`
- Sujet mixte → classe du sujet dominant

**Étape 4 — Extraction et consolidation des réponses**
Les réponses de Gemini ont été extraites via le script ZIP sous forme de fichiers `.txt`. Un script Python de traitement itératif parse le JSON contenu dans chaque fichier `.txt`, extrait les labels, et les accumule dans un fichier CSV unique (`annotated_by_llm.csv`). Le traitement s'effectue par lots de 10 fichiers à la fois, avec déduplication automatique à chaque ajout.

**Étape 5 — Re-classification des Nonsense par intention (Post-traitement)**
Après la constitution du dataset thématique final de 25 000 textes annotés par Gemini, l'ensemble des textes classés `Nonsense` a été isolé et soumis à une seconde passe d'annotation par Gemini 2.0 Flash, selon une taxonomie d'**intentions** :

| Intention | Description |
|---|---|
| `Soutien/Encouragement` | Messages de félicitations, encouragements, formules de bienveillance |
| `Opinion` | Avis personnels, réactions subjectives, jugements |
| `Question` | Interrogations explicites adressées au créateur ou à la communauté |
| `Publicité/Spam` | Contenu promotionnel, liens externes, spam automatisé |
| `Inclassable/Bruit` | Textes sans valeur sémantique exploitable |

**Distribution finale des intentions détectées (Total : 4 475 textes) :**

| Intention | Nombre d'exemples |
|---|---|
| Soutien/Encouragement | 2 803 |
| Opinion | 1 051 |
| Inclassable/Bruit | 278 |
| Question | 245 |
| Publicité/Spam | 98 |
| **TOTAL** | **4 475** |

Ces labels d'intention ont été fusionnés avec le dataset thématique original, produisant un dataset final à **11 classes distinctes** (6 thématiques + 5 intentions) :

| Classe | Nombre d'exemples |
|---|---|
| Politics_Society | 4 549 |
| Sports | 4 440 |
| Business_Economy | 3 119 |
| Religion | 3 012 |
| Health_Science | 2 889 |
| Soutien/Encouragement | 2 802 |
| Cuisine | 2 516 |
| Opinion | 1 051 |
| Inclassable/Bruit | 278 |
| Question | 244 |
| Publicité/Spam | 100 |
| **TOTAL** | **~25 000** |

---

## 4.5 🔍 Vérification et Validation

### Méthode de vérification

L'ensemble du processus de vérification et de validation du dataset final a été réalisé via **Label Studio**, en local (`http://localhost:8080`). Cela concerne à la fois les 25 000 textes thématiques annotés automatiquement par Gemini 2.0 Flash, et les 4 475 textes d'intention issus de la re-classification des Nonsense.

Les deux sous-ensembles ont fait l'objet d'une relecture humaine dans Label Studio, en suivant le même protocole d'annotation que celui utilisé pour le Gold Standard : chaque texte est affiché avec son label LLM proposé, et l'annotateur peut valider, corriger ou rejeter ce label.

### Qui a vérifié ?

La vérification a été réalisée par les membres du groupe, en procédant à une relecture par **échantillonnage stratifié** : chaque classe a été contrôlée indépendamment pour s'assurer de la cohérence inter-classes.

### Méthode utilisée

1. Import du dataset annoté par LLM dans Label Studio (format CSV).
2. Affichage du texte brut et du label `labeled_ia` proposé par Gemini.
3. Validation, correction ou rejet par l'annotateur humain.
4. Export des annotations finales depuis Label Studio (format JSON puis reconversion CSV).
5. Fusion des annotations manuelles avec les labels automatiques non vérifiés via script Python (`label_final = label humain si annoté, sinon label LLM`).

---

## 4.6 📊 Analyse des Erreurs de l'IA

Le code de détection des désaccords (`label_initial != label_studio`) a permis d'identifier **4 835 erreurs** sur 23 606 textes. L'analyse de la table des transitions révèle trois grands types d'erreurs.

---

### Type 1 — Mauvaise classification thématique

L'erreur dominante est la **sur-classification vers `Opinion`**, touchant systématiquement toutes les classes thématiques. Le LLM détecte une réaction personnelle dans le commentaire et ignore le domaine du contenu.

**Volumes par classe source :**

| Classe initiale (LLM) | Reclassée en `Opinion` | Reclassée en `Soutien/Encouragement` |
|---|---|---|
| Sports | 901 | 107 |
| Politics_Society | 532 | 202 |
| Health_Science | 346 | 199 |
| Cuisine | 254 | 257 |
| Business_Economy | 310 | 60 |
| Religion | 230 | 128 |

**Exemples réels :**

| Texte original | Label LLM | Label humain | Analyse |
|---|---|---|---|
| `عفاك كلمة إصلاح مستفزة... من افضل استعمال كلمة تغيير او فرض...` | `Business_Economy` | `Opinion` | Réaction critique au vocabulaire, pas de contenu économique réel |
| `Footix de sortie ...` | `Sports` | `Opinion` | Commentaire évaluatif en français sans contexte sportif explicite |
| `دكتور اكن لكم كل الاحترام ولكن اسمح لي الأطباء في المغرب لايحترمون المرضى ويهمهم فقط مدخولهم اليومي` | `Health_Science` | `Politics_Society` | Critique institutionnelle du système médical marocain |
| `واش اخويا من نيتك ولد انت وخرج لينا شي بطل راه أغلبية الشعب مضارب غ مع المعيشة الغالية` | `Business_Economy` | `Politics_Society` | Contenu socio-politique déguisé en commentaire économique |

---

### Type 2 — Ambiguïté (frontières floues entre classes)

**Confusion `Religion` ↔ `Soutien/Encouragement`** (230 cas Opinion + 128 cas Soutien)

En Darija marocaine, les formules de bienveillance religieuses sont omniprésentes dans tous les domaines. Le LLM les classifie en `Religion`, alors que le sens réel est une simple politesse.

| Texte original | Label LLM | Label humain | Analyse |
|---|---|---|---|
| `جزاك الله خيرا يا شيخنا` | `Religion` | `Soutien/Encouragement` | Formule de remerciement, pas de contenu religieux réel |
| `أحبك في الله أستاذ ياسين العمري بارك الله في عمرك و زادك من فضله` | `Religion` | `Soutien/Encouragement` | Déclaration d'affection avec formules religieuses = Soutien |

**Confusion `Cuisine` ↔ `Soutien/Encouragement`** (257 cas)

| Texte original | Label LLM | Label humain | Analyse |
|---|---|---|---|
| `ممم ما شاء الله` | `Cuisine` | `Soutien/Encouragement` | Expression d'admiration générique, aucun contenu culinaire |

---

### Type 3 — Sarcasme et ironie non détectés

| Texte original | Label LLM | Label humain | Analyse |
|---|---|---|---|
| `ههه بغا ثاني اشرح لأنشيلوتي كيفاش غادي يلعب ههه` | `Sports` | `Opinion` | Moquerie ironique — le double `ههه` signale le sarcasme |
| `مش هو الدعارة والجنس ههه كيراعي للسطولة كابتن مصطفى` | `Politics_Society` | `Opinion` | Ton moqueur avec `ههه`, critique de société ironique |
| `kat3arrrad l 7amalat inti9adat nta howa trump hhh` | `Politics_Society` | `Opinion` | Comparaison ironique en Arabizi, le `hhh` final confirme la dérision |

**Observation :** Le marqueur typique du sarcasme en Darija digitale est la répétition de `ههه` ou `hhh`/`hhhh` en Arabizi. Ces signaux pragmatiques sont systématiquement ignorés par Gemini 2.0 Flash, qui traite le contenu littéralement.

---

### Bilan quantitatif des erreurs

| Type d'erreur | Nb de cas estimés | % des 4 835 erreurs |
|---|---|---|
| Sur-classification vers `Opinion` | ~2 873 | ~59.4% |
| Confusion `Soutien/Encouragement` ← thème | ~953 | ~19.7% |
| Confusion inter-thématiques (Politics↔Business, Health↔Politics…) | ~572 | ~11.8% |
| Textes courts / Arabizi mal interprétés | ~437 | ~9.0% |
| **TOTAL** | **4 835** | **100%** |

---

## 4.7 📈 Statistiques de Performance

### Avant correction (labels LLM bruts)

| Indicateur | Valeur |
|---|---|
| **Nombre total de textes soumis au LLM** | ~49 000 (après filtrage Darija) |
| **Nombre de textes retenus dans le dataset final** | 23 606 |
| **Nombre de labels divergents détectés** | 4 835 |
| **Taux de correction (désaccord LLM ↔ humain)** | **20.48%** |
| **Accuracy globale (labels identiques)** | **79.52%** |

> **Interprétation clé :** 1 commentaire sur 5 a dû être redressé manuellement par un annotateur humain, ce qui démontre concrètement l'indispensabilité de la phase de validation humaine (Label Studio) dans tout pipeline de labellisation semi-automatique.

### Performances par classe (avant correction manuelle)

| Classe | Précision | Rappel | F1-score | Support |
|---|---|---|---|---|
| Business_Economy | 0.99 | 0.73 | 0.85 | 2 943 |
| Cuisine | 1.00 | 0.76 | 0.86 | 2 371 |
| Health_Science | 1.00 | 0.75 | 0.85 | 2 717 |
| Inclassable/Bruit | 0.54 | 0.90 | 0.68 | 273 |
| Opinion | 0.26 | 0.96 | 0.41 | 1 043 |
| Politics_Society | 0.89 | 0.79 | 0.84 | 4 148 |
| Publicité/Spam | 0.51 | 0.99 | 0.67 | 98 |
| Question | 0.48 | 0.93 | 0.63 | 243 |
| Religion | 0.97 | 0.82 | 0.89 | 2 844 |
| Soutien/Encouragement | 0.72 | 0.92 | 0.81 | 2 775 |
| Sports | 1.00 | 0.73 | 0.84 | 4 149 |
| **Accuracy globale** | | | **0.80** | **23 606** |
| **Macro avg** | 0.78 | 0.82 | 0.75 | |
| **Weighted avg** | 0.90 | 0.80 | 0.82 | |

> **Note :** La classe `Nonsense` (2 exemples dans le support brut) a été intégralement fusionnée dans `Inclassable/Bruit` lors du nettoyage final. Elle n'apparaît plus dans le dataset consolidé à 11 classes.

**Lecture des résultats :**
- Les classes thématiques "pures" (`Cuisine`, `Health_Science`, `Sports`, `Business_Economy`) atteignent une précision quasi-parfaite (≥ 0.99) : le LLM est très fiable quand il assigne ces labels, mais le rappel plus faible (~0.73–0.76) indique qu'il en rate une partie en les sur-classifiant vers `Opinion`.
- La classe `Opinion` est pathologique : une précision de **0.26** signifie que **74 % des textes classés `Opinion` par le LLM ne sont pas réellement des opinions** — ce sont des textes thématiques mal redistribués.
- Les classes d'intention (`Question`, `Publicité/Spam`, `Inclassable/Bruit`) présentent des performances moyennes, confirmant la difficulté de détecter des intentions dans de courts textes en Darija.

### Après correction (via Label Studio)

| Indicateur | Valeur |
|---|---|
| **Textes vérifiés et corrigés manuellement** | 4 835 |
| **Taux de correction appliqué** | 20.48% |
| **Qualité finale estimée — classes thématiques** | Bonne à très bonne (F1 ≥ 0.84) |
| **Qualité finale estimée — classes d'intention** | Correcte (F1 entre 0.41 et 0.81) |
| **Classe la plus fiable après correction** | `Sports`, `Cuisine`, `Health_Science` |
| **Classe la plus incertaine après correction** | `Opinion` |

---


## 4.8 🔧 Correction des Erreurs

### Comment les erreurs ont été corrigées

Après la labellisation semi-automatique par Gemini 2.0 Flash, l'intégralité du dataset annoté a été importée dans **Label Studio** pour une phase de vérification et correction humaine systématique.

Le protocole appliqué était le suivant :

1. Import du dataset annoté (`annotated_by_llm.csv`) dans Label Studio au format CSV.
2. Affichage texte par texte : chaque entrée montre le texte brut original et le label proposé par le LLM (`label_initial`).
3. Décision humaine : l'annotateur valide le label LLM, le corrige vers une autre classe, ou le rejette.
4. Export JSON depuis Label Studio, puis reconversion en CSV via script Python.
5. Fusion finale : application de la règle `label_final = label_studio si annoté, sinon label_initial`.

Cette phase a produit **4 835 modifications** sur 23 606 textes, soit un taux de correction de **20.48%**.

---

### Difficultés rencontrées

**1. Volume à vérifier trop important**
Avec 23 606 textes à passer en revue dans Label Studio, une vérification exhaustive était humainement irréalisable dans les délais du projet. Une stratégie d'**échantillonnage stratifié** a été adoptée : chaque classe a été contrôlée indépendamment en prioritisant les classes à faible confiance (`Opinion`, `Question`, `Publicité/Spam`). Les classes à haute précision confirmée (`Sports`, `Cuisine`, `Health_Science`) ont fait l'objet d'une vérification plus légère.

**2. Commentaires avec thème clair mais sous forme de question ou d'opinion**

| Texte | Difficulté | Décision finale |
|---|---|---|
| `ههه بغا ثاني اشرح لأنشيلوتي كيفاش غادي يلعب ههه` | Ton ironique sur le football | `Opinion` — la forme prime sur le fond sportif |
| `دكتور اكن لكم كل الاحترام ولكن اسمح لي الأطباء في المغرب لايحترمون المرضى` | Thème `Health_Science` ou `Politics_Society` ? | `Politics_Society` — critique institutionnelle |
| `majwbtich 3la la question حل ولا فخّ؟` | Question sur un sujet business | `Opinion` — interpellation rhétorique sans contenu dense |

La règle adoptée : **si la forme (question, ironie, réaction) domine le fond (thème), on classe selon l'intention**. Si le contenu thématique est suffisamment dense malgré la forme, on garde le thème.

**3. Textes où le thème est compris mais sans mot-clé explicite**

| Texte | Thème compris | Décision |
|---|---|---|
| `Mas maktfr7x b ta3adol` | Réaction à un match | `Opinion` — trop implicite |
| `ريس الوندال` | Référence politique marocaine | `Inclassable/Bruit` — trop court hors contexte |
| `Les biologistes kanchoufkoum` | Adressé à des scientifiques | `Inclassable/Bruit` — interpellation sans contenu classifiable |

Ces cas ont révélé une limite fondamentale : **la classification thématique sans contexte vidéo est parfois impossible**, même pour un annotateur humain.

---

## 4.9 📊 Statistiques du Dataset

### Volume et format

| Indicateur | Valeur |
|---|---|
| **Nombre total d'exemples** | **23 606** |
| **Nombre de classes** | **11** |
| **Format** | CSV, encodage UTF-8 |

---

### Répartition des classes

| Classe | Nombre d'exemples | Proportion (%) |
|---|---|---|
| Opinion | 3 772 | 15.98% |
| Politics_Society | 3 711 | 15.72% |
| Soutien/Encouragement | 3 539 | 14.99% |
| Sports | 3 027 | 12.82% |
| Religion | 2 426 | 10.28% |
| Business_Economy | 2 176 | 9.22% |
| Health_Science | 2 034 | 8.62% |
| Cuisine | 1 803 | 7.64% |
| Question | 469 | 1.99% |
| Inclassable/Bruit | 458 | 1.94% |
| Publicité/Spam | 191 | 0.81% |
| **TOTAL** | **23 606** | **100.00%** |

> **Note sur Nonsense :** L'unique exemple résiduel de la classe `Nonsense` (artefact de la fusion des datasets) a été fusionné dans `Inclassable/Bruit`, portant cette dernière de 457 à 458 exemples. Le dataset final présente donc **11 classes propres** sans résidu.

---

### Type d'écriture (script)

| Script | Nombre | Proportion (%) |
|---|---|---|
| Arabe (alphabet arabe) | 19 760 | 83.71% |
| Latin (Arabizi + français + anglais) | 3 844 | 16.29% |
| **TOTAL** | **23 604** | **100%** |

La très large majorité des textes (83.71%) est rédigée en alphabet arabe, confirmant que la Darija écrite en caractères arabes reste le registre dominant sur YouTube marocain. Les 16.29% en latin représentent l'Arabizi ainsi que les insertions de français et d'anglais typiques du code-switching.

---

### Problèmes de déséquilibre

**Déséquilibre entre classes thématiques (les 8 classes principales) :**

| Indicateur | Valeur |
|---|---|
| Classe thématique majoritaire | `Opinion` (3 772 exemples) |
| Classe thématique minoritaire | `Cuisine` (1 803 exemples) |
| **Ratio de déséquilibre thématique (Max/Min)** | **2.09x** |
| Statut | ✅ Déséquilibre modéré — dataset thématique bien équilibré |

Le ratio de 2.09x entre la classe la plus haute (`Opinion`) et la classe thématique la plus basse (`Cuisine`) indique un dataset **très bien équilibré** pour les 8 classes principales. Ce niveau de déséquilibre est considéré comme acceptable dans la littérature NLP (seuil critique généralement fixé à 10x).

**Déséquilibre avec les classes résiduelles :**

| Indicateur | Valeur |
|---|---|
| Classe la plus basse (hors thématique) | `Publicité/Spam` (191 exemples) |
| Ratio Opinion / Publicité/Spam | ~19.7x |
| Statut | ⚠️ Déséquilibre significatif pour les classes minoritaires |

Les classes `Question` (469), `Inclassable/Bruit` (458) et `Publicité/Spam` (191) représentent ensemble **4.74%** du dataset. Il est normal et attendu que ces classes soient minoritaires — elles correspondent à du bruit ou à des intentions rares dans des corpus de commentaires réels.

**Traitements prévus pour la phase de modélisation :**
- Pondération des classes (`class_weight='balanced'`) dans les classifieurs scikit-learn pour compenser le déséquilibre résiduel
- Oversampling ciblé (SMOTE) pour `Publicité/Spam` (191 ex.) si nécessaire
- Les 8 classes thématiques principales ne nécessitent pas de traitement de déséquilibre (ratio ≤ 2.09x)
------

## 4.7 📈 Statistiques de Performance

L'audit qualité complet réalisé sur l'ensemble du corpus permet de mesurer précisément l'efficacité de la labellisation automatisée par rapport aux corrections humaines appliquées au sein de Label Studio.

### Avant correction (Labellisation Automatique) :
* **Nombre total de données labellisées automatiquement par l'IA :** 23 606 lignes
* **Modèle utilisé :** Google Gemini 2.0 Flash (Interface Web via pipeline UI-Automation)

### Après correction (Validation Manuelle) :
* **Nombre de labels modifiés/redressés manuellement :** 4 835 lignes
* **Taux de correction global (Taux d'erreur constaté de l'IA) :** 20,48 %
* **Exactitude globale (IA Accuracy) :** 79,52 %
* **Qualité finale estimée du lot :** ~100 % (Concordance totale avec la charte d'annotation humaine du projet).

*Analyse des performances :* Bien que l'IA affiche une performance globale solide (~80% de concordance avec l'humain), le fait qu'un commentaire sur cinq ait dû être rectifié manuellement met en évidence la valeur ajoutée de notre audit. L'extraction du `classification_report` montre que si la machine excelle sur les classes métiers spécifiques (Précision de 1.00 pour `Cuisine`, `Sports` ou `Health_Science`), elle souffre d'un biais de paresse majeur sur la classe `Opinion` (Faible précision de 0.26 pour un Rappel maximal de 0.96), où elle a massivement basculé par défaut les tournures de phrases complexes ou ambiguës en Darija.

---

## 4.8 🔧 Correction des Erreurs

### 🛠️ Processus de redressement méthodologique
La correction des 4 835 désaccords identifiés lors de la passe automatique de l'IA a été rigoureusement industrialisée pour garantir l'intégrité globale du dataset final :
1. **Isolation algorithmique :** Un script d'évaluation dédié dans notre notebook `final_analysis.ipynb` a isolé les lignes discordantes dans un fichier pivot nommé `label_disagreements.csv`.
2. **Arbitrage humain :** Ces données litigieuses ont été réimportées dans l'interface Label Studio. L'équipe a appliqué strictement la charte d'annotation (priorité au sujet métier dominant, déclassement des formules de politesse vers l'intention comportementale adéquate). Chaque label erroné de l'IA a été écrasé manuellement.
3. **Réintégration sécurisée :** Le script Python `merge_labels.py` a fusionné les corrections de l'échantillon Label Studio avec la base globale, en indexant les modifications par la clé unique `id` pour éviter tout décalage de ligne ou corruption textuelle.

### ⚠️ Difficultés rencontrées lors de la correction
Le redressement de ce volume de données a confronté l'équipe à plusieurs verrous :
* **Fatigue cognitive des annotateurs :** Auditer manuellement près de 5 000 lignes de commentaires web truffés d'abréviations en Arabizi et de Code-Switching agressif représente une lourde charge mentale, exigeant des sessions de double-validation pour maintenir la cohérence.
* **Gestion de l'encodage et des données manquantes :** La cohabitation de l'alphabet arabe et des caractères latins au sein du même fichier CSV a provoqué de nombreuses corruptions d'affichage (problèmes d'émoticônes et de chaînes brisées), résolues par l'application stricte de l'encodage `utf-8-sig`. De plus, l'absence native de métadonnées temporelles sur certaines transcriptions brutes a nécessité le développement d'un script d'imputation aléatoire uniforme, générant des dates réalistes comprises strictement entre le 19 juin 2016 et le 19 mars 2026 uniquement sur les cellules vides (`NaN`).

---

## 4.9 📊 Statistiques du Dataset Final

### Répartition générale du type d'écriture (Script)
Le traitement de la colonne linguistique montre une écriture massivement dominée par l'alphabet arabe, reflétant les habitudes de communication sur les espaces web marocains ciblés :
* **Script Arabe (`arabic`) :** 19 762 lignes | 83,72 %
* **Script Latin/Arabizi (`latin`) :** 3 844 lignes | 16,28 %

### Distribution finale des classes (Labels validés)
À l'issue de la phase de réconciliation et du raffinement de la classe résiduelle *Nonsense* en intentions directes, la structure sémantique finale de notre dataset de **23 606 lignes** se répartit comme suit :

| Catégorie / Label Studio | Nombre d'exemples | Proportion (%) | Nature du Signal |
| :--- | :---: | :---: | :--- |
| **Opinion** | 3 772 | 15,98 % | Intention / Comportement |
| **Politics_Society** | 3 711 | 15,72 % | Thématique Métier |
| **Soutien/Encouragement** | 3 539 | 14,99 % | Intention / Comportement |
| **Sports** | 3 027 | 12,82 % | Thématique Métier |
| **Religion** | 2 426 | 10,28 % | Thématique Métier |
| **Business_Economy** | 2 176 | 9,22 % | Thématique Métier |
| **Health_Science** | 2 034 | 8,62 % | Thématique Métier |
| **Cuisine** | 1 803 | 7,64 % | Thématique Métier |
| **Question** | 469 | 1,99 % | Intention / Comportement |
| **Inclassable/Bruit** | 458 | 1,94 % | Résiduel Qualifié |
| **Publicité/Spam** | 191 | 0,81 % | Résiduel Qualifié |
| **TOTAL** | **23 606** | **100,00 %** | **—** |

### ⚖️ Diagnostic du Déséquilibre des Classes (Imbalance Analysis)
Si l'on écarte les classes purement techniques (Bruit, Spam, Question) dont la faible proportion est naturelle et souhaitable, l'analyse du cœur thématique révèle un excellent équilibre :
* **Classe thématique majoritaire :** `Opinion` (3 772 exemples)
* **Classe thématique minoritaire :** `Cuisine` (1 803 exemples)
* **Ratio de déséquilibre effectif (Imbalance Ratio Thématique) :** **2,09x**

*Conclusion du diagnostic :* Le dataset ne souffre d'aucun déséquilibre sévère sur ses thématiques principales. L'écart minimal de 2x entre la classe la plus haute et la plus basse démontre une collecte bien proportionnée lors de l'étape de scraping initial, évitant ainsi le recours à des techniques artificielles de rééchantillonnage (type SMOTE).

---

## 4.10 ⚠️ Limites

L’analyse approfondie des erreurs de notre pipeline met en évidence trois barrières structurelles inhérentes au traitement de la Darija numérique :

* **Biais de plateforme (YouTube-Centric) :** L'intégralité du corpus provient de l'écosystème YouTube. Les structures syntaxiques sont intimement liées aux codes de cette plateforme (repères temporels/timestamps, interpellations directes des créateurs). De plus, l'IA a parfois hérité d'un biais contextuel lié aux chaînes d'extraction (un commentaire neutre sous une vidéo médicale dérivait indûment vers `Health_Science` par pur effet de corrélation de la source).
* **Limites linguistiques et variabilité de la Darija :** L'absence de standardisation orthographique en Darija et en Arabizi engendre une multiplication inutile de tokens distincts pour le dictionnaire (ex: *"Zouina"*, *"zwina"*, *"zwiiina"*), diluant l'efficacité sémantique du modèle. De plus, le *Code-Switching* agressif (mélange intra-phrastique de Darija, Français et Anglais) sature parfois le contexte linguistique.
* **Limites du modèle face aux structures hybrides (Thème vs Intention) :** C'est la limite la plus lourde constatée. Lorsqu'un commentaire est formulé sous forme de **Question** ou de **Sarcasme** tout en traitant d'un domaine métier précis (ex: une pique ironique sur une tactique de football), Gemini 2.0 Flash échoue à équilibrer les deux aspects. Le modèle se laisse également tromper par le second degré local en prenant au premier degré des expressions ironiques marocaines qui utilisent un vocabulaire élogieux ou religieux pour critiquer (ex: *"تبارك الله على الفاهم ديالنا"*).

---

## 4.11 🚀 Améliorations

Pour pallier les limites observées et faire progresser ce projet vers une version industrielle, trois axes d'améliorations prioritaires sont préconisés :

* **Au niveau des Données (Diversification et Normalisation) :** Extraire des données en dehors de l'écosystème YouTube (forums communautaires marocains ou sous-serveurs Reddit locaux) pour casser le biais de format court. Intégrer un pipeline de translittération en amont afin de convertir systématiquement l'écriture latine et ses chiffres phonétiques (3, 7, 9) vers un alphabet arabe unifié, réduisant ainsi drastiquement la sparsité du vocabulaire.
* **Au niveau de l'Annotation (Bascule Multi-Label) :** Pour résoudre le conflit persistant entre le thème et l'intention, le schéma de données doit évoluer vers du multi-label. Chaque texte recevrait ainsi deux étiquettes orthogonales et indépendantes : une étiquette *Sémantique/Métier* (ex: `Business_Economy`) et une étiquette *Comportementale/Intention* (ex: `Question` ou `Sarcasme`).
* **Au niveau du Modèle IA (Spécialisation) :** Remplacer l'approche Few-Shot globale par un processus de Fine-Tuning supervisé sur un modèle open-source d'échelle intermédiaire (type Llama-3-8B) en utilisant notre Gold Standard comme base d'alignement. Privilégier également des modèles encodeurs pré-entraînés spécifiquement sur le dialecte maghrébin, tels que *MarBERT* ou *DarijaBERT*, qui possèdent nativement une meilleure sensibilité aux nuances culturelles et à l'argot digital marocain.
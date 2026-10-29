# Reels « univers » — procédure quotidienne automatique

Ce dépôt produit **un reel Instagram par jour** sur l'espace et l'univers, sans intervention humaine.
Claude écrit l'épisode → GitHub Actions génère la voix (ElevenLabs), fait le rendu et publie le MP4 en release publique
→ Claude programme le reel sur Instagram via le connecteur Metricool.

Langue : tout en français. Format d'épisode et catalogue d'illustrations : `docs/EPISODE_FORMAT.md` (à lire à chaque fois).

## Garde-fous (non négociables)
- **Ne jamais publier sur un compte listé dans `config.json → never_post_to`** (ex. `universenbref`).
- Si `config.json → instagram_username` ou `metricool_blog_id` est `null` : faire tout jusqu'au rendu, **ne rien programmer**, et le signaler.
- Ne jamais publier une vidéo qu'on n'a pas vérifiée (étape 7). En cas d'échec à n'importe quelle étape : ne rien publier, expliquer l'erreur en une phrase dans le message final.
- Chaque chiffre/affirmation doit être vérifié sur une source fiable (NASA, ESA, CNES, IAU, observatoires, publications). Pas de théorie présentée comme un fait.
- Un seul épisode par jour : si `episodes/<date du jour>/` existe déjà avec une release publiée, ne rien refaire.
- Ne jamais afficher ni demander la clé ElevenLabs (elle vit dans les secrets GitHub).

## Étapes
1. **Préparer** : le dépôt doit être cloné (sinon `add_repo` Wily091/reels-univers en accès push, puis clone). `git pull`.
   `npm i --no-save --no-package-lock @fontsource/anton@5.3.0 @fontsource/space-mono@5.3.0` (Playwright et Chromium sont déjà installés dans l'environnement).
2. **Choisir le sujet** : lire `published.json`, éviter tout sujet déjà traité ou trop proche. Varier : planètes, étoiles, trous noirs,
   galaxies, Lune, exploration spatiale, échelles et distances, lumière et temps, phénomènes étranges, histoire de l'astronomie.
   Privilégier un fait surprenant, vrai et facile à comprendre, idéalement avec une idée reçue à démonter.
3. **Rechercher** : WebSearch/WebFetch, au moins une source de référence par chiffre. Noter les URL dans `sources`.
4. **Écrire** `episodes/<AAAA-MM-JJ>/episode.json` en suivant `docs/EPISODE_FORMAT.md` (accroche forte, 45–65 s, 8–12 scènes,
   nombres en lettres dans la voix off, conclusion douce standard). `voice` et `theme` : reprendre `config.json`.
   Légende : 2–4 phrases + question pour les commentaires ; 8–12 hashtags FR pertinents.
5. **Contrôler en local (gratuit)** :
   `node engine/validate.js episodes/<date>` → corriger toute erreur ; avertissements à examiner.
   `python3 engine/tts.py episodes/<date> --mock && node engine/build_timeline.js episodes/<date> && node engine/preview.js episodes/<date>`
   puis **regarder** `episodes/<date>/build/preview.jpg` (Read) : textes lisibles, rien qui déborde ni ne chevauche l'illustration, accents en couleur. Corriger puis recommencer si besoin.
6. **Envoyer** : `git add episodes/<date>/episode.json && git commit -m "Épisode <date> : <titre>" && git push`.
   Le push déclenche le workflow « Rendu du reel » (≈ 6–12 min).
7. **Attendre et vérifier le rendu** : suivre `https://api.github.com/repos/Wily091/reels-univers/actions/runs?per_page=5`
   (run dont `head_sha` = le commit poussé) jusqu'à `status: completed` (max 30 min ; attendre avec l'outil Monitor/until-loop, pas de sleep au premier plan).
   Si `conclusion != success` : arrêter, ne rien publier, signaler (lien du run).
   Sinon télécharger `https://github.com/Wily091/reels-univers/releases/download/ep-<date>/reel.mp4` et `meta.json` (curl -L),
   vérifier avec ffprobe (durée 35–80 s, vidéo 1080x1920, piste audio) et extraire 4 images (ffmpeg) à regarder.
8. **Programmer sur Instagram (Metricool)** :
   - `getBrandSettings` → la marque dont `networksData.instagramData` == `config.instagram_username` (et blogId == `metricool_blog_id`). Sinon : ne rien publier.
   - Heure : `getBestTimeToPostByNetwork` (instagram, aujourd'hui) → meilleur créneau **au moins 1 h après maintenant** ; sinon 19:00 ; si déjà passé, demain même heure.
   - `createScheduledPost` : `media` = [URL de la release], `providers` = [{"network":"instagram"}],
     `instagramData` = {"type":"REEL","showReelOnFeed":true,"isAiGenerated":true}, `videoCoverMilliseconds` = `meta.json → coverMs`,
     `text` = légende + ligne vide + hashtags, `autoPublish` = true, `publicationDate` dans le fuseau `config.timezone`.
9. **Journaliser** : ajouter l'épisode à `published.json` (date, title, topics, posted=true/false, heure programmée), commit + push
   (ce commit ne touche pas `episode.json`, il ne relance pas de rendu).
10. **Message final** (2–3 lignes) : sujet du jour, heure de publication programmée, ou la raison de l'échec.

# Reels « univers » — procédure quotidienne automatique

Ce dépôt produit **un reel Instagram par jour** sur l'espace et l'univers, sans intervention humaine, pour le compte
Instagram indiqué dans `config.json` (via la marque Metricool indiquée).

Fonctionnement :
- `backlog/NNN-slug/` = **stock d'épisodes écrits d'avance**. Chacun a `episode.json` et, une fois générée, sa voix dans `voice/`
  (`voice.mp3` + `alignment.json`). Les voix du stock sont générées en lot par le workflow « Générer les voix du stock »
  (déclenché en modifiant `backlog/GENERER_VOIX.txt`).
- Chaque jour, on publie le **prochain épisode du stock** : on le déplace dans `episodes/<AAAA-MM-JJ>/`, ce qui déclenche le workflow
  « Rendu du reel » (la voix stockée est réutilisée : aucun crédit ElevenLabs), puis on le programme sur Instagram via Metricool.

Langue : tout en français. Format d'épisode et catalogue d'illustrations : `docs/EPISODE_FORMAT.md`.

## Garde-fous (non négociables)
- Ne jamais publier sur un compte listé dans `config.json → never_post_to`.
- Si `config.json → instagram_username` ou `metricool_blog_id` est `null` : ne rien programmer, le signaler.
- Ne jamais publier une vidéo non vérifiée (étape 5). En cas d'échec à n'importe quelle étape : ne rien publier, expliquer l'erreur en une phrase.
- Un seul reel par jour : si `episodes/<date du jour>/` existe déjà et que `published.json` indique posted=true pour cette date, ne rien refaire.
- Ne jamais afficher ni demander la clé ElevenLabs (elle vit dans les secrets GitHub).
- Ne jamais consommer de crédits ElevenLabs dans la tâche quotidienne : ne prendre que des épisodes du stock **qui ont déjà leur voix**.

## Tâche quotidienne
1. **Préparer** : le dépôt doit être cloné (sinon `add_repo` Wily091/reels-univers en accès push, puis clone). `git pull`.
2. **Choisir** l'épisode : le plus petit `backlog/NNN-*` qui contient `voice/alignment.json` et `voice/voice.mp3`.
   S'il n'y en a aucun : ne rien publier ; message final « Stock épuisé : il faut écrire de nouveaux épisodes et générer leurs voix ».
3. **Activer** : `git mv backlog/<NNN-slug> episodes/<AAAA-MM-JJ>` (date du jour, Europe/Paris), mettre `"date": "<AAAA-MM-JJ>"` dans `episode.json`
   (ne pas toucher au texte de `say`, sinon la voix stockée n'est plus valable), commit « Épisode <date> : <titre> » et push.
   Le push déclenche « Rendu du reel » (≈ 5–10 min).
4. **Attendre** : suivre `https://api.github.com/repos/Wily091/reels-univers/actions/runs?per_page=5` (run dont `head_sha` = le commit poussé)
   jusqu'à `status: completed` (max 30 min ; attendre avec Bash `run_in_background` + boucle until, pas de sleep au premier plan).
   Si `conclusion != success` : lire les annotations d'échec (`/actions/runs/<id>/jobs` → `check_run_url` + `/annotations`),
   ne rien publier, signaler l'erreur.
5. **Vérifier** : télécharger `https://github.com/Wily091/reels-univers/releases/download/ep-<date>/reel.mp4` et `meta.json` (curl -L) ;
   ffprobe (durée 35–80 s, 1080x1920, piste audio présente) ; extraire 4 images (ffmpeg) et les regarder.
6. **Programmer sur Instagram (Metricool)** :
   - `getBrandSettings` → la marque dont l'id == `config.metricool_blog_id` ET `networksData.instagramData` == `config.instagram_username`. Sinon : ne rien publier.
   - Heure : `getBestTimeToPostByNetwork` (instagram, aujourd'hui, fuseau `config.timezone`) → meilleur créneau **au moins 1 h après maintenant** ;
     à défaut 19:00 ; si déjà passé, demain même heure.
   - `createScheduledPost` : `blogId` = config, `media` = [URL de la release reel.mp4], `providers` = [{"network":"instagram"}],
     `instagramData` = {"type":"REEL","showReelOnFeed":true,"isAiGenerated":true}, `videoCoverMilliseconds` = `meta.json → coverMs`,
     `text` = légende + ligne vide + hashtags (séparés par des espaces), `autoPublish` = true, `draft` = false,
     `publicationDate` = {"dateTime": "...", "timezone": config.timezone}.
7. **Journaliser** : ajouter l'épisode à `published.json` (date, title, topics, posted=true/false, heure programmée, plannerUrl), commit + push.
8. **Message final** (2–3 lignes) : sujet du jour, heure de publication programmée, nombre d'épisodes restant en stock avec voix
   (alerte si < 10), ou la raison de l'échec.

## Écrire de nouveaux épisodes pour le stock (sur demande, pas dans la tâche quotidienne)
- Numérotation : `backlog/NNN-slug/episode.json`, NNN à la suite du plus grand numéro existant (y compris ceux déjà passés dans `episodes/`, voir `published.json`).
- Sujet : jamais traité (vérifier `published.json` et tout `backlog/`). Varier : planètes, étoiles, trous noirs, galaxies, Lune, exploration spatiale,
  échelles et distances, lumière et temps, phénomènes étranges, histoire de l'astronomie. Un fait surprenant, vrai, facile à comprendre.
- Chaque chiffre/affirmation vérifié sur une source fiable (NASA, ESA, CNES, IAU, observatoires, publications), URL dans `sources`.
- Respecter `docs/EPISODE_FORMAT.md` (accroche, 45–65 s, nombres en lettres dans la voix off, conclusion douce standard). `voice`/`theme` : `config.json`.
- Contrôle gratuit : `node engine/validate.js <dir>` puis `python3 engine/tts.py <dir> --mock && node engine/build_timeline.js <dir> && node engine/preview.js <dir>`
  et regarder `<dir>/build/preview.jpg`.
- Générer les voix (consomme des crédits) : modifier `backlog/GENERER_VOIX.txt` (ex. y écrire la date) et pousser.

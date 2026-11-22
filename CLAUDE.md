# Reels « univers » — procédure quotidienne automatique

Ce dépôt produit **deux reels Instagram par jour** (12:00 et 19:00) sur l'espace et l'univers, sans intervention humaine, pour le compte
Instagram indiqué dans `config.json` (via la marque Metricool indiquée).

> **⚠️ Novembre 2026 — DA officielle validée le 16/11 : voir `docs/STYLE_PLANCHE.md` et la vidéo `docs/reference/univers_en_bref_reference_DA.mp4` (planche noire, photos NASA annotées, ouverture en plan rapproché, voix Koraly Storyteller sans silences, texte parlé) — à garder pour tous les posts jusqu’à ce que William demande de changer.**
> L'ancien rendu (`engine/engine.html`) et les anciens textes de `backlog/` (sans `"format": "planche"`) ne sont **jamais** publiés.
> Rendu automatique : `engine/build.sh` (moteur générique `engine/planche/planche.html`), format des épisodes : `docs/FORMAT_PLANCHE.md`.
> **Musique : TOUJOURS et UNIQUEMENT « orbite » (`assets/music/orbite.wav`), répétée en boucle jusqu'à la fin du reel (`engine/planche/music_loop.py`), très basse sous la voix (`engine/planche/mix.sh`).**
> **Son : niveaux fixes identiques pour toutes les vidéos (voix −16 LUFS, musique −32 LUFS + sidechain, mix final ≈ −16 LUFS, aucun bruitage) — voir `docs/STYLE_PLANCHE.md` § 8 bis. Avant chaque publication, `engine/planche/check_audio.sh reel.mp4` doit afficher OK, sinon ne rien publier.**

> **Format (validé par William le 22/11) : vidéos courtes de 20 à 30 s, accroche écrite en très gros dès la 1re image (champ `hook`), fin courte — voir `docs/STYLE_PLANCHE.md` § 0.**

> **Rythme et publication (exigences de William, 16/11) : 2 reels par jour, programmés à 12:00 et à 19:00 (Europe/Paris), deux sujets différents.**
> **L'agent agit en expert réseaux sociaux et marketing : légende avec accroche, explication du fait de la vidéo, mots-clés SEO, appel à l'action, 5 hashtags maximum — règles complètes dans `docs/LEGENDES.md`.**

Fonctionnement :
- `backlog/NNN-slug/` = **stock d'épisodes écrits d'avance** (format `planche`). Un épisode est **publiable** seulement si :
  `"format": "planche"`, `"valide": true` (texte validé par William) et sa voix est dans `voice/` (`voice.mp3` + `alignment.json`).
  Les voix sont générées en lot par le workflow « Générer les voix du stock » (déclenché en modifiant `backlog/GENERER_VOIX.txt`),
  uniquement pour les épisodes validés, après un contrôle gratuit de mise en page.
- Chaque matin, on prend **deux** épisodes publiables, on les déplace dans `episodes/<AAAA-MM-JJ>-12h/` et `episodes/<AAAA-MM-JJ>-19h/`,
  ce qui déclenche le workflow « Rendu du reel » (voix stockée réutilisée : aucun crédit ElevenLabs) ; puis on les programme sur Instagram via Metricool.

Langue : tout en français.

## Travail d'équipe (demandé par Christella, 18/11)
Objectif commun : faire monter @universenbref le plus vite possible en vues et en abonnés.
Les agents (publication, montage) se parlent dans **`equipe/DISCUSSION.md`** (règles en tête du fichier), lisible par l'équipe humaine.
- **Au début de chaque session**, lire les messages adressés à son rôle depuis son dernier passage et y répondre dans le fichier.
- Quand on a quelque chose d'utile à dire à l'autre agent (stats, problème de rendu, idée, demande), l'écrire là, en bas, puis commit « Discussion : … » + push.
- Rien qui touche à la DA, à la voix, à la musique ou au rythme n'est appliqué sans l'accord de William (marquer « → À valider par William »).
- Tâche quotidienne de l'agent publication : à l'étape 10, si les stats Metricool des reels de la veille apportent un enseignement, le poster dans `equipe/DISCUSSION.md`.

## Garde-fous (non négociables)
- Ne jamais publier sur un compte listé dans `config.json → never_post_to`.
- Si `config.json → instagram_username` ou `metricool_blog_id` est `null` : ne rien programmer, le signaler.
- Ne jamais publier une vidéo non vérifiée (étape 6). En cas d'échec d'un reel : ne pas le publier, expliquer l'erreur en une phrase (l'autre reel peut partir s'il est OK).
- Pas de doublon : si `published.json` contient déjà une entrée `posted: true` pour `<date>-12h` (ou `-19h`), ne pas refaire ce créneau ;
  vérifier aussi avec `getScheduledPosts` qu'aucun reel n'est déjà programmé à cette heure-là.
- Ne jamais afficher ni demander la clé ElevenLabs (elle vit dans les secrets GitHub).
- Ne jamais consommer de crédits ElevenLabs dans la tâche quotidienne : ne prendre que des épisodes publiables (voix déjà stockée).
- Ne jamais modifier le texte de `say` d'un épisode du stock (sinon la voix stockée n'est plus valable).

## Tâche quotidienne (chaque matin)
1. **Préparer** : le dépôt doit être cloné (sinon `add_repo` Wily091/reels-univers en accès push, puis clone). `git pull`. Date du jour D (Europe/Paris).
2. **Choisir** : les deux plus petits `backlog/NNN-*` publiables, de **sujets différents** (`subject`), ni l'un ni l'autre déjà publiés (voir `published.json`).
   - Un seul disponible : le programmer à 19:00 seulement. Aucun : ne rien publier ; message final « Stock épuisé : il faut écrire de nouveaux épisodes, les faire valider et générer leurs voix ».
3. **Activer** : `git mv backlog/<NNN-a> episodes/<D>-12h` et `git mv backlog/<NNN-b> episodes/<D>-19h`, mettre `"date": "<D>"` et `"slot": "12:00"` / `"19:00"`
   dans chaque `episode.json` (ne pas toucher au reste), **un seul** commit « Reels <D> : <titre a> / <titre b> » et push.
   Le push déclenche « Rendu du reel », qui rend les deux épisodes l'un après l'autre (≈ 10–20 min) et publie les releases `ep-<D>-12h` et `ep-<D>-19h`.
4. **Attendre** : suivre `https://api.github.com/repos/Wily091/reels-univers/actions/runs?per_page=5` (run « Rendu du reel » dont `head_sha` = le commit poussé)
   jusqu'à `status: completed` (max 45 min ; attendre avec Bash `run_in_background` + boucle until, pas de sleep au premier plan).
   Si `conclusion != success` : lire les annotations (`/actions/runs/<id>/jobs` → `check_run_url` + `/annotations`) ; publier seulement les releases qui existent et passent l'étape 6.
5. **Télécharger** : pour chaque créneau, `https://github.com/Wily091/reels-univers/releases/download/ep-<D>-<12h|19h>/reel.mp4` et `meta.json` (curl -L).
6. **Vérifier** chaque reel : ffprobe (durée 18–35 s, 1080x1920, piste audio présente) ; `bash engine/planche/check_audio.sh reel.mp4` → **OK** ;
   extraire 4 images (ffmpeg) et les regarder (planche noire, photo officielle, textes lisibles, rien qui se chevauche).
7. **Légende (expert réseaux sociaux)** : relire `caption` et `hashtags` de l'épisode selon `docs/LEGENDES.md` et les améliorer si besoin
   (1re ligne ≤ 125 caractères avec le mot-clé, 600–1 200 caractères, faits uniquement tirés de `sources`, 5 hashtags max dont #universenbref,
   ne pas réutiliser exactement le même bloc de hashtags que l'autre reel du jour ni que la veille). Texte publié = légende + ligne vide + hashtags séparés par des espaces.
8. **Programmer sur Instagram (Metricool)** :
   - `getBrandSettings` → la marque dont l'id == `config.metricool_blog_id` ET `networksData.instagramData` == `config.instagram_username`. Sinon : ne rien publier.
   - Heures **fixes** : 12:00 et 19:00 (Europe/Paris) le jour D. Si une heure est déjà passée (ou dans moins de 15 min), programmer ce reel à maintenant + 30 min
     (et le signaler) ; si 19:00 est déjà passé aussi, le décaler au lendemain 12:00 et ne pas en activer de nouveau ce jour-là.
   - `createScheduledPost` : `blogId` = config, `date` = « <D>T12:00:00+01:00 » (ou +02:00 en heure d'été), `info` = {`media`: [URL de la release reel.mp4],
     `providers`: [{"network":"instagram"}], `instagramData`: {"type":"REEL","showReelOnFeed":true,"isAiGenerated":true},
     `videoCoverMilliseconds`: `meta.json → coverMs` (dernière image = planche complète), `text`: légende + hashtags, `autoPublish`: true, `draft`: false,
     `publicationDate`: {"dateTime": "<D>T12:00:00", "timezone": config.timezone}}.
9. **Journaliser** : pour chaque reel, ajouter à `published.json` {date, slot, folder, num, title, subject, topics, posted, scheduledAt, plannerUrl, caption finale}, commit + push.
10. **Message final** (2–4 lignes) : les deux sujets et leurs heures, le nombre d'épisodes publiables restants (alerte si < 10, c.-à-d. moins de 5 jours),
    le nombre d'épisodes écrits mais pas encore validés, ou la raison d'un échec.

## Écrire de nouveaux épisodes pour le stock (sur demande, pas dans la tâche quotidienne)
- Format et exemples : `docs/FORMAT_PLANCHE.md` (+ `docs/STYLE_PLANCHE.md` pour la DA et le ton, `docs/LEGENDES.md` pour la légende).
- Numérotation : `backlog/NNN-slug/episode.json`, NNN à la suite du plus grand numéro existant (y compris ceux déjà passés dans `episodes/`, voir `published.json`).
- Sujet : jamais traité (vérifier `published.json` et tout `backlog/`). Un fait surprenant, vrai, facile à comprendre, avec une vraie photo officielle.
- Chaque chiffre/affirmation vérifié sur une source fiable (NASA, ESA, ESO, CNES, IAU…), URL dans `sources`. Photos : `tools/IMAGES.json` puis push.
- `"valide": false` tant que William n'a pas validé le texte. **Toujours lui montrer les textes avant de générer les voix.**
- Contrôle gratuit : `bash engine/build.sh backlog/<NNN-slug> --mock` (texte, photos, mise en page, anti-chevauchement) puis regarder `build/preview.jpg`.
- `"voix_plus_tard": true` dans un épisode = écrit et validé, mais voix volontairement différée (budget ElevenLabs) : le workflow le saute. Pour le débloquer, retirer ce champ puis relancer les voix.
- Générer les voix (consomme des crédits, épisodes validés uniquement) : modifier `backlog/GENERER_VOIX.txt` (ex. y écrire la date) et pousser.

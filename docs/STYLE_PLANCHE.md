# Style validé : « planche de notes » (novembre 2026)

C'est le style retenu par William pour toutes les vidéos d'Univers en bref. Il remplace l'ancien style (titres cinétiques « nébuleuse » de `engine/engine.html`), qui n'est **plus** à utiliser.
Vidéo de référence validée : épisode Vénus (« univers_en_bref_001_venus_final.mp4 », 48 s, voix Koraly). Le prototype qui l'a produite est dans `engine/planche/`.

## Concept
- Une **grande planche de notes de scientifique** (2160 × 3840 px, soit 2 × l'écran du téléphone), vue à travers un cadrage 1080 × 1920.
- **Début** : la planche entière vue de loin, presque vide. Le thème (« Vénus ») s'écrit au centre avec son croquis.
- **Ensuite** : la caméra va sur une zone de la planche, la note correspondante **s'écrit toute seule** (sans main visible) au rythme de la voix, puis la caméra passe à la note suivante.
- **Fin** : un seul dézoom sur la planche entièrement remplie, avec « Si ça t'a plu, abonne-toi » et « … et partage-la » qui s'écrivent en bas.
- **Notes éparpillées** (pas de carte mentale reliée par des flèches).

## Direction artistique
- Papier **violet nuit** : dégradé #2a1a52 → #170e33, quadrillage léger, grain, taches douces, petites étoiles éparpillées (jamais sous un texte).
- Écriture **blanc crème** #f3ead8 ; mots importants en **rose** #ff8fc0 et **jaune doré** #ffd27a ; texte secondaire crème à 60 %.
- Polices : **Caveat 700** (notes manuscrites), **Kalam** (petites annotations), **Special Elite** (en-tête « PLANCHE N° 001 » / « UNIVERS EN BREF », pied « @universenbref »). Toutes via @fontsource.
- Croquis au trait légèrement tremblé : planète hachurée, horloge, orbite, thermomètre qui se remplit, lever de Soleil, flèche de rotation, nuages ; mots entourés ou soulignés à la main ; bouts de scotch.
- Chiffres à l'écran en chiffres (243, 225 j, + de 460 °C) ; dans la voix, en lettres.

## Caméra (règles validées après plusieurs essais — ne pas revenir en arrière)
1. **Un seul dézoom au début et un seul à la fin.** Entre les notes : **pas de zoom/dézoom** (ça donnait mal à la tête). La caméra reste à la même distance (échelle 0,95) et **glisse** d'une note à l'autre.
2. Glissements **lents et doux** : 1,8 à 2,4 s, courbe sinus (départ et arrivée en douceur).
3. La caméra **reste immobile** pendant l'écriture, et **ne repart qu'une fois la note entièrement écrite** (+ ~0,4 s pour lire).
4. La note suivante ne commence à s'écrire **qu'une fois la caméra arrivée** (ou en toute fin d'arrivée).
5. Chaque glissement part de la position réelle de la caméra, en ligne droite, vers une cible **déjà bornée** aux limites de la planche (sinon : à-coups). Test : la vitesse de la caméra ne doit jamais varier de plus de ~2 px d'une image à l'autre.
6. Pour garder la voix synchronisée, on **insère de courtes respirations dans la voix** (silence) **entre deux phrases ou sur une virgule, jamais au milieu d'une phrase**, quand la caméra a besoin de temps. La vidéo s'allonge (Vénus : 39 s de voix → 48 s).

## Voix et texte
- Voix : **Koraly – Storyteller** (`TojRWZatQyy9dujEdiQ1`, voix de la bibliothèque ElevenLabs, abonnement Creator), modèle eleven_multilingual_v2, vitesse API 1,1 puis tempo ×1,1, pauses resserrées par `engine/tts.py`.
- Texte : **comme un humain qui raconte**. Longues phrases liées (« en fait », « et le plus fou », « du coup », « alors que »), **pas de points de suspension, pas de phrases courtes hachées**, peu de points. Une question d'accroche au début. Fin douce : « Si ça t'a plu, abonne-toi pour d'autres histoires sur l'univers, et si tu connais quelqu'un que ça pourrait faire rêver, partage-lui la vidéo. »
- Dans `episode.json`, découper le texte en phrases (une par élément `say`) aux virgules/points : ce découpage sert au calage des notes et aux respirations ; la voix est générée d'un seul trait (texte joint).
- Toujours faire valider le texte par William avant de générer (≈ 900 crédits par épisode).

## Son
- Voix normalisée seule d'abord (loudnorm −16 LUFS ; certaines voix sortent très faibles), musique de `engine/music.py` à 0,22 avec sidechain sous la voix, limiteur ; résultat ≈ −16 LUFS.
- **Pas de bruitages** (ils étaient trop forts ; s'ils reviennent : très discrets, ~20 dB sous la voix).

## Export
- 1080 × 1920, 30 i/s, H.264 high, `-crf 18 -maxrate 10M -bufsize 20M` (sinon le grain du papier donne des fichiers de 170 Mo), AAC 192k, faststart. Couverture = dernière image (planche complète).

## Prototype (engine/planche/)
- `planche_anim.html` : planche + notes de Vénus **écrites à la main dans le code** (positions et dessins), animation par `window.renderAt(t)` ; calage via `venus_cues.js` (CUES = instants des mots dans la voix, SHOTS = cadrages, BOUND = silences entre phrases) ; la fonction `plan()` décale caméra/écriture et calcule les respirations (`window.INS`).
- `plan.js` : affiche le planning et les respirations à insérer ; `render_frames.js <dossier> <début> <fin>` : rend les images (Playwright) ; `planche_statique.html` : planche fixe (aperçu).
- Étapes utilisées pour Vénus (à automatiser) : `tts.py` (voix stockée) → `phrases.json` → instants des mots clés → `venus_cues.js` → `plan.js` (respirations) → voix avec silences insérés → `music.py` sur la nouvelle durée → mixage ffmpeg → rendu des images (3 processus en parallèle) → encodage.

## Reste à faire (prochaine étape)
1. **Généraliser** : décrire les notes de chaque épisode dans `episode.json` (texte, dessin, emplacement, mot de la voix déclencheur) au lieu de les coder en dur, avec une mise en page automatique des notes éparpillées autour du thème central.
2. Brancher ce rendu dans `engine/build.sh` / le workflow GitHub « Rendu du reel » à la place de `engine.html`.
3. Réécrire les 60 épisodes de `backlog/` dans le ton parlé (leurs textes actuels sont dans l'ancien style haché) et y mettre la voix Koraly, puis les faire valider, puis générer les voix en lot.
4. Créer la tâche planifiée quotidienne (procédure de CLAUDE.md) une fois le stock prêt.

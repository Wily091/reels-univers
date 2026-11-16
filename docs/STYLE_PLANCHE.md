# Style validé : « planche de notes » sur fond noir (10 novembre 2026)

**C'est LE style de toutes les vidéos d'Univers en bref, jusqu'à ce que William dise de changer.** Ne rien modifier (fond, couleurs, caméra, voix, son, rythme) sans son accord.
Vidéo de référence validée : `univers_en_bref_001_venus_noir.mp4` (Vénus, 38,5 s, voix Koraly Storyteller d'un seul trait, fond noir). Image finale : `docs/reference_venus_noir.jpg`.
Le prototype exact qui l'a produite est dans `engine/planche/` (voir plus bas).

## Concept
- Une **grande planche de notes de scientifique** (2160 × 3840 px, 2 × l'écran), vue à travers un cadrage 1080 × 1920.
- **Début** : planche entière vue de loin, presque vide ; le thème (« Vénus ») s'écrit au centre avec son croquis.
- **Ensuite** : la caméra va sur une zone, la note correspondante **s'écrit toute seule** (sans main visible) au rythme de la voix, puis la caméra glisse vers la note suivante.
- **Fin** : un seul dézoom sur la planche remplie, « Si ça t'a plu, abonne-toi ✶ » et « … et partage-la » s'écrivent en bas.
- **Notes éparpillées** autour du thème (pas de carte mentale avec flèches), sur un **parcours en serpentin** (haut gauche → haut droite → milieu droite → bas droite → milieu gauche → bas gauche → fin) pour que les glissements restent courts. Aucune note ne doit en chevaucher une autre (vérifier l'image finale).
- Deux idées très courtes et liées peuvent **partager un même cadrage** (Vénus : « elle tourne à l'envers » + « le Soleil se lève à l'ouest ») pour ne pas écrire trop vite.

## Direction artistique
- **Fond noir** : dégradé radial #161616 → #050505, quadrillage blanc à 5 %, voile de taches gris neutre très léger, grain blanc à 6 %, petites étoiles crème/dorées éparpillées (jamais sous un texte).
  (Le violet nuit #2a1a52 → #170e33 était la version précédente : ne plus l'utiliser.)
- Écriture **blanc crème** #f3ead8 ; mots importants en **rose** #ff8fc0 et **jaune doré** #ffd27a ; texte secondaire crème à 60 %.
- Polices : **Caveat 700** (notes), **Kalam** (petites annotations), **Special Elite** (en-tête « PLANCHE N° 00X » / « UNIVERS EN BREF », pied « @universenbref »). Via @fontsource.
- Croquis au trait légèrement tremblé : planète hachurée, horloge, orbite, thermomètre qui se remplit, lever de Soleil, flèche de rotation, nuages ; mots entourés/soulignés à la main ; bouts de scotch.
- Chiffres à l'écran en chiffres (243, 225 j, + de 460 °C) ; dans la voix, en lettres.

## Photos officielles (demandé par William le 16/11/2026)
- Quand ça illustre mieux le propos **et** qu'une vraie image existe, ajouter **une ou deux photos officielles** (NASA en priorité, sinon ESA, ESO, JAXA…) : vraie surface, vraie planète, image de télescope (Hubble, James Webb, sondes).
- Intégration dans la DA : la photo est **scotchée sur la planche comme un tirage photo** (bord crème, léger angle, bout de scotch), elle apparaît quand la voix en parle (fondu « qui se développe »), dans le même cadrage que sa note. Jamais en plein écran, jamais à la place des notes.
- **Une photo ne remplace jamais les explications** : il y a toujours des petites notes manuscrites à côté, quoi qu'il arrive.
- Quand il y a une photo, **pas de croquis du même objet** : soit on écrit directement les explications à côté, soit on **dessine/annote sur la photo** au trait manuscrit (flèche, cercle autour d'un détail, mot écrit dessus), qui s'écrit au rythme de la voix comme les autres notes.
- Petite légende manuscrite + **crédit obligatoire** en petit sous la photo (ex. « NASA/JPL-Caltech », « ESA/Webb »).
- Ne jamais mettre de logo NASA/ESA ni laisser croire que la chaîne est liée à la NASA. NASA : images en général libres de droits (vérifier la page de l'image, certaines appartiennent à des tiers). ESA : souvent CC BY-SA 3.0 IGO (crédit exact obligatoire).
- Source et URL de chaque image dans `episode.json` (`images` : fichier, crédit, URL, licence). Images téléchargées par le workflow GitHub (le bac à sable ne peut pas les récupérer).
- Pas d'image inventée/générée présentée comme réelle. Si aucune vraie image ne convient : seulement les croquis.

## Effet « wow » (pour tout le monde, même sans connaître l'espace)
- **Accroche** : la 1re phrase est le fait le plus fou, posé comme une question simple (« Tu savais que… ? »).
- **Comparaisons du quotidien** pour rendre les chiffres sensibles : taille, distance, chaleur, durée ramenées à des choses connues (four, avion, terrain de foot, vie humaine…).
- **Au moins un retournement** par épisode (« et le plus fou… », « alors que… ») qui contredit ce qu'on croirait.
- **Révélation visuelle** : la vraie photo officielle apparaît, puis les annotations manuscrites s'écrivent dessus ou à côté (« voilà à quoi ça ressemble vraiment »).
- Les chiffres clés peuvent **défiler en comptant** jusqu'à leur valeur (ex. 0 → 460 °C) pendant que la voix les dit.
- Pas de jargon ; si un mot technique est inévitable, l'expliquer en une demi-phrase.
- Le style (fond noir, caméra, voix, rythme sans silences) ne change pas : le « wow » vient du contenu, des photos et des révélations, pas d'effets tape-à-l'œil.

## Caméra (règles validées — ne pas revenir en arrière)
1. **Un seul dézoom au début, un seul à la fin.** Entre les notes : **aucun zoom/dézoom** (mal de tête). Échelle fixe 0,95, la caméra **glisse**.
2. Glissement en ligne droite, courbe sinus (départ/arrivée doux), durée 1,3 à 2,2 s selon la distance (distance/750 px).
3. La caméra **sait où elle va** : elle est **immobile** pendant l'écriture (aucune dérive), et ne part qu'une fois la note **entièrement écrite** (+ 0,25 s).
4. La note suivante commence à s'écrire **quand la caméra arrive** (≈ 0,35 s avant la fin du glissement).
5. Cibles **bornées d'avance** aux limites de la planche, chaque glissement part de la position réelle (sinon à-coups). Test : `node camtest.js` (saut de vitesse max ≈ 5 px/image, pas de pic).

## Voix, rythme et texte
- **Voix : Koraly – Storyteller** (`TojRWZatQyy9dujEdiQ1`, bibliothèque ElevenLabs), eleven_multilingual_v2, vitesse API 1,1 puis tempo ×1,1, pauses resserrées par `engine/tts.py`. (La version « Expressive and Engaging » `F1toM6PcP54s45kOOAyV` a été testée et écartée.)
- **Jamais de silences ajoutés** (ça coupe le watchtime) : la voix passe **d'un seul trait**, c'est **la caméra et l'écriture qui s'adaptent à la voix**. Quand le temps manque, l'écriture d'une note est accélérée (compressée entre l'arrivée de la caméra et le départ suivant), jamais la voix ralentie.
- Texte : **comme un humain qui raconte**. Longues phrases liées (« en fait », « et le plus fou », « du coup », « alors que »), pas de points de suspension, pas de phrases courtes hachées. Question d'accroche au début. Fin : « Si ça t'a plu, abonne-toi pour d'autres histoires sur l'univers, et si tu connais quelqu'un que ça pourrait faire rêver, partage-lui la vidéo. »
- Durée visée ≈ 35–45 s.
- Dans `episode.json`, une phrase par élément `say` (sert au calage des notes) ; la voix est générée d'un seul trait (texte joint).
- Faire valider le texte par William avant de générer (≈ 900 crédits par épisode).

## Son
- Voix normalisée seule (loudnorm −16 LUFS), musique `engine/music.py` à 0,22 avec sidechain sous la voix, fondu final 1,2 s, limiteur → ≈ −16 LUFS. Script : `engine/planche/mix.sh`.
- **Pas de bruitages.**

## Export
- 1080 × 1920, 30 i/s, H.264 high, `-preset slow -crf 18 -maxrate 10M -bufsize 20M`, AAC 192k, faststart (`engine/planche/encode.sh`). Couverture = dernière image (planche complète).

## Prototype (engine/planche/) — Vénus, version validée
- `planche_anim.html` : planche noire + notes de Vénus **codées à la main** (positions, dessins, groupes n1…n7 avec translations), `window.renderAt(t)`. Contient `plan()` : calcule départs/durées des glissements et compresse l'écriture (pas de pauses : `window.INS=[]`).
- `venus_cues.js` : CUES (instants des mots clés dans la voix Storyteller, END = fin de la dernière phrase + 0,7 s), SHOTS (cadrages : c/c2/fin à 0,5 ; notes à 0,95).
- `venus_ref/` : voix Storyteller de référence (`voice.mp3`) et son `phrases.json` (phrases + temps de chaque caractère `cs`).
- `plan.js` (affiche le planning), `camtest.js` (régularité caméra), `render_frames.js <dossier> <début> <fin>` (images, 3 processus en parallèle), `mix.sh`, `encode.sh`.
- Calage des CUES : le texte est identique, donc on retrouve l'instant d'un mot via l'index de caractère dans `cs`.
- Chaîne : `tts.py` → `phrases.json` → CUES → `plan.js`/`camtest.js` → `music.py` (durée END) → `mix.sh` → `render_frames.js` ×3 → `encode.sh`.

## Reste à faire (automatisation)
1. **Généraliser** : décrire les notes de chaque épisode dans `episode.json` (texte, type de croquis, mot déclencheur dans la voix) avec mise en page automatique en serpentin autour du thème central, contrôle anti-chevauchement, calcul auto des CUES depuis `cs`.
2. Brancher ce rendu dans `engine/build.sh` / le workflow « Rendu du reel » à la place de `engine.html`.
3. Réécrire les 60 épisodes de `backlog/` dans le ton parlé (voix Storyteller), les faire valider, puis générer les voix en lot.
4. Créer la tâche planifiée quotidienne (CLAUDE.md) une fois le stock prêt.

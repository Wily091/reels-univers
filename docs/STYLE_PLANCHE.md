# DA officielle d'Univers en bref — « planche de notes » noire avec photos officielles

**Validée par William le 16 novembre 2026 (« C'est magnifique, on reste comme ça »).**
**C'est LA DA de toutes les vidéos, jusqu'à ce que William dise de changer.** Ne rien modifier (fond, couleurs, polices, caméra, voix, son, rythme, photos) sans son accord explicite.

## Références (à regarder avant tout travail)
- Vidéo de référence : `docs/reference/univers_en_bref_reference_DA.mp4` (Vénus, 38,5 s).
- Images clés : `docs/reference/1_debut.jpg` (1re image), `2_note_photo.jpg` (une note avec photo annotée), `3_planche_finale.jpg` (dernière image = couverture).
- Code exact qui l'a produite : `engine/planche/planche_anim.html` (+ `venus_cues.js`, `img/`, `venus_ref/`). Ancienne version sans photo : `engine/planche/archive/`.

---

## 1. Concept et déroulé
- Une **grande planche de notes de scientifique** de 2160 × 3840 px (2 × l'écran), filmée par une caméra virtuelle à travers un cadre 1080 × 1920 (format Reel).
- **Ouverture (0 → 2,5 s)** : la vidéo démarre **directement en plan rapproché** (échelle 1,1, centrée sur x 1080, y 1990) sur la **photo officielle du thème, déjà affichée dès la 1re image** (pas d'écran vide, pas de fondu d'entrée). Le titre (« Vénus ») s'écrit au-dessus pendant que la voix commence. La caméra tient ~0,6 s puis fait **un seul dézoom doux** (1,9 s, courbe sinus) jusqu'à la planche entière (échelle 0,5). Sans photo disponible : même ouverture sur le croquis central.
- **Corps** : la caméra glisse vers une zone de la planche, la note correspondante **s'écrit toute seule** (sans main visible) au rythme exact de la voix, puis la caméra glisse vers la note suivante.
- **Fin** : un seul dézoom sur la planche entièrement remplie ; « Si ça t'a plu, abonne-toi ✶ » (doré) puis « … et partage-la » (rose) s'écrivent en bas à gauche. La dernière image (planche complète) sert de couverture.
- **Notes éparpillées** autour du thème central (pas de carte mentale, pas de flèches entre les notes), sur un **parcours en serpentin** pour des glissements courts : haut gauche → haut droite → milieu droite → bas droite → milieu gauche → bas gauche → fin.
- **Aucun chevauchement** : aucune note, photo ou croquis ne doit en toucher un autre (vérifier l'image finale à chaque fois).
- Deux idées très courtes et liées peuvent **partager un même cadrage** (Vénus : « elle tourne à l'envers » + « le Soleil se lève à l'ouest ») pour ne pas écrire trop vite.

## 2. Fond et couleurs
- **Fond noir** : dégradé radial (centre 50 %/45 %, rayon 80 %) **#161616 → #050505**, débordant de 400 px autour de la planche.
- Quadrillage : carreaux de 80 px, trait 2 px, **blanc à 5 %**.
- Voile de taches : bruit fractal très large (baseFrequency 0,004), gris neutre, opacité 0,6 (alpha 0,25).
- Grain papier : bruit fractal fin (baseFrequency 0,85, 3 octaves), **blanc à 6 %**.
- Étoiles : ~70 éléments aléatoires (25 % petites étoiles à 8 branches crème #f3ead8 ou dorées #ffd27a, sinon points crème 2–5 px à 30–80 %), **retirées automatiquement si elles tombent sous un texte, un dessin ou une photo**, et absentes du centre.
- En-tête en **Special Elite 40 px, crème à 60 %** : « PLANCHE N° 00X » (haut gauche) et « UNIVERS EN BREF » (haut droite) ; pied « @universenbref » (bas droite).
- Couleurs des notes :
  - **Crème #f3ead8** : texte principal et traits.
  - **Rose #ff8fc0** : mots forts, retournements, flèches d'annotation, cercles.
  - **Jaune doré #ffd27a** : chiffres clés, Soleil, soulignements secondaires.
  - **Crème à 60 %** : texte secondaire, petites annotations.
  - **Blanc #ffffff** : texte écrit **sur** une photo.
  - Scotch : rectangle 200 × 60 crème (rgba 255,230,180, 0,22), légèrement incliné.
- Ancien fond violet (#2a1a52 → #170e33) : **abandonné**, ne plus l'utiliser.

## 3. Écriture et croquis
- Polices (@fontsource, installées dans `node_modules`) :
  - **Caveat 700** : toutes les notes manuscrites (titre 260 px, notes 90–190 px).
  - **Kalam** : petites annotations (46–62 px) et crédits photo.
  - **Special Elite** : en-tête et pied uniquement.
- Les textes **s'écrivent de gauche à droite** (révélation progressive), durée ≈ 0,045 s par caractère (entre 0,35 et 1,3 s). Légère inclinaison de chaque note (−8° à +4°).
- Croquis au **trait légèrement tremblé**, qui se tracent comme au stylo : horloge, orbite en pointillés avec Soleil doré, thermomètre qui se remplit, lever de Soleil avec rayons, flèche de rotation, nuages superposés.
- Gestes manuscrits : mots **entourés** (ellipse tremblée), **soulignés** (double trait), flèches, bouts de scotch.
- Chiffres à l'écran **en chiffres** (243, 225 j, + de 460 °C) ; dans la voix, **en lettres**.

## 4. Photos officielles
- Dès qu'une vraie image existe et illustre mieux le propos : **1 à 2 photos officielles par vidéo** (NASA en priorité, sinon ESA, ESO, JAXA…). La photo du thème sert d'ouverture (au centre).
- **Format « tirage photo »** :
  - cadre crème #f3ead8, bord de 20 px, et bande du bas plus haute pour le crédit ;
  - légère inclinaison (−2° à +3°) et un bout de scotch en haut ;
  - photo centrale : cadre 620 × 680 avec une image de 580 × 580 ;
  - photo secondaire : cadre 480 × 400 avec une image de 440 × 330.
- **Crédit obligatoire** dans la bande du bas : Kalam 23 px, gris #5a5048, centré. Exemples : « Vénus vue par Mariner 10 · NASA/JPL-Caltech », « Vénus · radar Magellan (relief ×10) · NASA/JPL ». Si l'image est retouchée, le dire (relief exagéré, couleurs simulées, etc.).
- Apparition : photo d'ouverture visible dès la 1re image ; les autres apparaissent quand la voix en parle, par un fondu de 0,8 s (« qui se développe »), dans le cadrage de leur note.
- **Une photo ne remplace jamais les explications** : il y a toujours des notes manuscrites à côté.
- Avec une photo, **pas de croquis du même objet**. On écrit les explications à côté, ou on **annote directement sur la photo** au trait manuscrit, au rythme de la voix. Exemples : « vraie photo ! » rose + soulignement, « un volcan » + flèche vers le sommet, « sol à 460 °C » en blanc sur l'image.
- Un petit objet dessiné peut devenir la vraie photo **découpée en rond**, avec la flèche ou le dessin tracé par-dessus (Vénus : la petite planète qui « tourne à l'envers »).
- Jamais en plein écran, jamais de logo NASA/ESA, rien qui laisse croire que la chaîne est liée à la NASA. Jamais d'image générée présentée comme réelle.
- Licences : NASA en général libre de droits (vérifier la page de l'image) ; ESA souvent CC BY-SA 3.0 IGO (crédit exact).
- Téléchargement : écrire les images dans `tools/IMAGES.json` (fichier, id NASA « PIA… » ou urls, crédit, page) et pousser. Le workflow « Télécharger des images officielles » les met dans `assets/images/` (le bac à sable ne peut pas joindre la NASA). Ensuite, recadrer et réduire dans `engine/planche/img/` (≈ 800 px).
- Dans `episode.json`, renseigner `images` : fichier, crédit, URL de la page, licence.

## 5. Effet « wow » (pour tout le monde, même sans rien connaître à l'espace)
- **Accroche** : la 1re phrase est le fait le plus fou, posé comme une question simple (« Tu savais que… ? »).
- **Comparaisons du quotidien** pour rendre les chiffres concrets : four, avion, terrain de foot, vie humaine…
- **Au moins un retournement** par épisode (« et le plus fou… », « alors que… »).
- **Révélation visuelle** : la vraie photo, puis les annotations qui s'écrivent dessus.
- **Compteurs** : un chiffre clé défile de 0 à sa valeur (≈ 1,4 s, ralentissement en fin de course) pendant que la voix le dit, synchronisé avec le dessin associé (ex. le thermomètre se remplit pendant que « + de 0… 460 °C » défile).
- Pas de jargon ; un mot technique inévitable s'explique en une demi-phrase.
- Le « wow » vient du contenu, des photos et des révélations, **pas d'effets tape-à-l'œil**.

## 6. Caméra (règles validées — ne pas revenir en arrière)
1. **Un seul dézoom au début, un seul à la fin.** Entre les notes : **aucun zoom ni dézoom** (ça donne mal à la tête). Échelle fixe 0,95, la caméra **glisse**.
2. Glissement en ligne droite, courbe sinus (départ et arrivée doux), durée 1,3 à 2,2 s selon la distance (distance / 750 px).
3. La caméra **sait où elle va** : elle est **parfaitement immobile** pendant l'écriture (aucune dérive) et ne repart qu'une fois la note **entièrement écrite** (+ 0,25 s).
4. La note suivante commence à s'écrire **quand la caméra arrive** (≈ 0,35 s avant la fin du glissement).
5. Cibles **bornées d'avance** aux limites de la planche, chaque glissement part de la position réelle (sinon à-coups). Test : `PAGE=planche_anim.html node camtest.js` (saut de vitesse max ≈ 5 px/image, pas de pic).

## 7. Voix, rythme et texte
- **Voix : Koraly – Storyteller** (`TojRWZatQyy9dujEdiQ1`, bibliothèque ElevenLabs), eleven_multilingual_v2, vitesse API 1,1 puis tempo ×1,1, pauses resserrées par `engine/tts.py`. La version « Expressive and Engaging » (`F1toM6PcP54s45kOOAyV`) a été testée et **écartée**.
- **Jamais de silences ajoutés** (ça coupe le watchtime) : la voix passe **d'un seul trait**, et ce sont **la caméra et l'écriture qui s'adaptent**. Quand le temps manque, l'écriture d'une note est accélérée, la voix n'est jamais ralentie ni coupée.
- Texte **comme un humain qui raconte** :
  - longues phrases liées (« en fait », « et le plus fou », « du coup », « alors que ») ;
  - pas de points de suspension, pas de phrases courtes hachées ;
  - une question d'accroche ;
  - fin standard : « Si ça t'a plu, abonne-toi pour d'autres histoires sur l'univers, et si tu connais quelqu'un que ça pourrait faire rêver, partage-lui la vidéo. »
- Durée visée : **35 à 45 s**.
- Dans `episode.json`, une phrase par élément `say` (sert au calage des notes). La voix est générée d'un seul trait (texte joint).
- **Toujours faire valider le texte par William avant de générer la voix** (≈ 900 crédits par épisode).

## 8. Son
- Voix normalisée seule (highpass 70 Hz, loudnorm −16 LUFS), musique `engine/music.py` à 0,22 avec sidechain sous la voix, fondu final 1,2 s, limiteur 0,89. Résultat ≈ −16 LUFS. Script : `engine/planche/mix.sh voix.wav musique.wav END sortie.wav`.
- **Pas de bruitages.**

## 9. Export
- 1080 × 1920, 30 images/s, H.264 high, `-preset slow -crf 18 -maxrate 10M -bufsize 20M`, yuv420p, AAC 192k, faststart (`engine/planche/encode.sh images/ mix.wav sortie.mp4`). Environ 17 Mo pour 38 s.
- Couverture = dernière image (planche complète).

## 10. Code de référence (engine/planche/)
- `planche_anim.html` : planche + notes + photos de Vénus **codées à la main**, animation par `window.renderAt(t)`.
  - Éléments : `X` (texte qui s'écrit), `P` (trait qui se trace), `F` (bloc qui apparaît en fondu, durée réglable), `arrow`, `under`, `tape`. Un texte avec `cnt` fait défiler un compteur.
  - Groupes n1…n7 avec translations.
  - En tête du script : `SHOTS[0]` (plan rapproché d'ouverture, 1,1) et `SHOTS[1]` (dézoom de 0,6 à 2,5 s).
  - `plan()` calcule les glissements et compresse l'écriture (aucune pause : `window.INS=[]`).
- `venus_cues.js` : CUES (instants des mots clés dans la voix, END = fin de la dernière phrase + 0,7 s) et SHOTS des notes (0,95). Calage : le texte étant identique, l'instant d'un mot se retrouve par son index de caractère dans `phrases.json → cs`.
- `img/` : photos recadrées (`venus.jpg` = moitié gauche de PIA23791 en couleurs naturelles, `maat_mons.jpg` = PIA00254). `venus_ref/` : voix Storyteller de référence + `phrases.json`.
- Outils : `plan.js`, `camtest.js`, `render_frames.js <dossier> <début> <fin>` (lancer 3 processus en parallèle ; la variable `PAGE` choisit la page), `mix.sh`, `encode.sh`.
- Chaîne complète : `tts.py` → `phrases.json` → CUES → `plan.js` + `camtest.js` → `music.py` (durée END) → `mix.sh` → `render_frames.js` ×3 → `encode.sh` → vérifier 4 images + l'image finale.

## 11. Reste à faire (automatisation)
1. **Généraliser** : décrire les notes et les photos de chaque épisode dans `episode.json` (texte, croquis ou photo, annotations, mot déclencheur dans la voix), avec mise en page automatique en serpentin, contrôle anti-chevauchement et calcul automatique des CUES depuis `cs`.
2. Brancher ce rendu dans `engine/build.sh` et le workflow « Rendu du reel », à la place de `engine.html`.
3. Réécrire les 60 épisodes de `backlog/` dans le ton parlé avec l'effet « wow » et les photos, les faire valider, puis générer les voix en lot.
4. Créer la tâche planifiée quotidienne (CLAUDE.md) une fois le stock prêt.

# Format d'un épisode (`episodes/AAAA-MM-JJ/episode.json`)

Un épisode = une suite de **scènes**. Chaque scène a :
- `say` : la ou les phrases de voix off de la scène (chaque élément = un appel ElevenLabs).
- `lines` : les gros titres à l'écran, calés sur ces phrases.
- optionnel : `hit` (fond plein bleu électrique, texte sombre, impact sonore), `ghost` (grand mot en filigrane),
  `kicker` (petite mention en haut, style « source »), `il` (illustration au trait).

```json
{
  "date": "2026-10-30",
  "title": "Titre interne",
  "theme": "nebuleuse",
  "voice": { "id": "pFZP5JQG7iQjIQuC4Bku", "model": "eleven_multilingual_v2", "speed": 1.08 },
  "caption": "Légende Instagram (2–4 phrases, 1–2 emojis max, une question pour les commentaires)",
  "hashtags": ["#espace", "#univers", "..."],
  "sources": ["https://science.nasa.gov/..."],
  "scenes": [
    {
      "say": ["Phrase une.", "Phrase deux…"],
      "ghost": "MOT", "kicker": "PETITE MENTION · CHIFFRE",
      "il": { "type": "planet", "label": "VÉNUS" },
      "lines": [
        { "text": "TITRE EN [ACCENT]", "at": 0 },
        { "text": "[243 JOURS]", "at": [1, 0.3], "punch": true,
          "count": { "from": 0, "to": 243, "fmt": "[{v} JOURS]", "dur": 0.9, "dec": 0 } }
      ]
    }
  ]
}
```

## Règles des champs
- `at` : moment où la ligne apparaît. `0` = début de la phrase 0 de la scène ; `[1, 0.5]` = milieu de la phrase 1.
  Viser le mot prononcé : la fraction ≈ position du mot dans la phrase.
- `[...]` dans `text` = mot(s) en couleur d'accent (sur une scène `hit`, l'accent devient blanc).
- `punch: true` = petit zoom + secousse (mots forts, 1 à 2 par scène max).
- `max` = taille max en px (défaut 330). Les lignes sont ajustées à la largeur ; une ligne courte devient énorme → mettre `max: 150–250`.
- `gap` = espace en px avant la ligne. `align: "c"` = centré. `strike` (même format que `at`) = barre la ligne en couleur.
- `count` = compteur animé ; `fmt` contient `{v}` ; `dec` = décimales (virgule française).
- `kicker` : texte, ou liste `[{ "at": 0, "text": "..." }, { "at": 1, "text": "..." }]`.
- `il.sw` (format `at`) = moment de bascule pour `crossStar` (l'étoile se fait barrer) et `blobToGalaxy` (la tache devient galaxie).
- Phrase de voix off : chaîne, ou `{ "text": "...", "pause": 0.6 }` pour forcer la pause après.
- Scène `hit` sans illustration : titres centrés plus bas (y = 600 par défaut). On peut forcer `"y": 520`.

## Illustrations disponibles (`il.type`)
| type | rendu | paramètres |
|---|---|---|
| `none` | rien | |
| `stars` | ciel étoilé | |
| `constellation` | constellation qui se trace | |
| `crossStar` | étoile, barrée au moment `sw` | `sw` |
| `starsPulse` | plusieurs étoiles qui pulsent | |
| `question` / `exclaim` | grand « ? » / « ! » au trait | |
| `clock` | horloge (aiguilles à rebours) | `forward: true` pour l'endroit |
| `lightTravel` | rayon de lumière d'un astre à un autre | `from`, `to` (libellés) |
| `sun` | soleil rayonnant | |
| `distance` | petit point → étoile, pointillés + libellé | `label` |
| `blobToGalaxy` | tache floue qui devient galaxie | `sw` |
| `galaxy` | galaxie spirale | |
| `timeline` | frise avec deux repères | `left`, `leftSub`, `right`, `rightSub` |
| `telescope` | miroir hexagonal type James Webb | |
| `tunnel` | galaxies qui défilent vers toi | |
| `burst` | explosion / Big Bang | |
| `horizon` | montagnes, petit personnage, étoile filante | |
| `deep` | champ d'étoiles en mouvement + petite galaxie | |
| `planet` | planète à bandes (`ring: true` = anneaux) | `label`, `ring`, `r` |
| `globe` | sphère qui tourne (méridiens) | `label` |
| `moon` | lune à cratères | `label` |
| `blackhole` | trou noir + disque d'accrétion | `label` |
| `orbit` | astre central + objet en orbite | `center`, `rx`, `speed` |
| `sizeCompare` | gros cercle vs petit cercle à l'échelle | `big`, `small`, `ratio` |
| `comet` | comète avec queue | `label` |
| `waves` | ondes gravitationnelles (deux corps qui tournent) | `label` |
| `thermo` | thermomètre qui monte | `label`, `level` (0–1) |
| `rocket` | fusée qui décolle | |

Les libellés d'illustration et `kicker` utilisent une police mono : majuscules, pas d'emoji, pas d'indices (écrire CO2, pas CO₂).
Les titres utilisent Anton : lettres latines accentuées, chiffres, ponctuation courante, `°`, `%`. Pas d'emoji, pas de symboles rares.

## Style éditorial
- **Accroche** dès la première phrase (fait surprenant, idée reçue à démonter, question).
- Rythme : phrases courtes, pauses avec `…`, une scène `hit` toutes les 3–4 scènes pour relancer.
- 45–65 s au total (≈ 650–1 000 caractères de voix off), 8–12 scènes.
- Nombres **en lettres** dans `say` (« deux cent quarante-trois »), en chiffres à l'écran.
- Tutoiement, ton « je te raconte un truc fou », jamais racoleur ni faux.
- Chaque chiffre vient d'une source fiable (NASA, ESA, CNES, IAU, publications) listée dans `sources`. En cas de doute → arrondir prudemment (« environ », « plus de ») ou retirer.
- Dernière scène = la conclusion douce standard :
  - say : « Si ça t'a plu, tu peux t'abonner pour d'autres histoires sur l'univers. » / « Et si tu connais quelqu'un que ça pourrait faire rêver… partage-lui. »
  - lines : « SI ÇA T'A PLU… », « D'AUTRES HISTOIRES », « [SUR L'UNIVERS.] », « [PARTAGE-LA.] » (gap 30, max 140)

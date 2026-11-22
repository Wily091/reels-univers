# Format d'un épisode « planche » (`backlog/NNN-slug/episode.json`)

Le moteur `engine/planche/planche.html` dessine tout seul la planche de la DA officielle (`docs/STYLE_PLANCHE.md`) à partir de ce fichier :
titre central + photo officielle (visible dès la 1re image), 4 à 6 notes placées en serpentin, fin « abonne-toi / partage-la ».
Exemple complet : `backlog/001-venus-jour-annee/episode.json` (même planche que la vidéo de référence).

```json
{
 "format": "planche",
 "valide": false,                       // true quand William a validé le texte (sinon : pas de voix, pas de publication)
 "num": 12,                             // « PLANCHE N° 012 »
 "title": "Titre interne",
 "subject": "Saturne",                  // grand titre central (≤ 14 caractères)
 "voice": {"id": "TojRWZatQyy9dujEdiQ1", "model": "eleven_multilingual_v2", "tempo": 1.1, "api_speed": 1.1},
 "images": [{"id": "saturne", "file": "assets/images/saturne_cassini.jpg", "nasa_id": "PIA06193",
             "credit": "Saturne vue par Cassini · NASA/JPL/Space Science Institute", "page": "https://…", "license": "Domaine public (NASA)",
             "crop": [x, y, largeur, hauteur],   // optionnel, en fractions de l'image
             "pad": true}],                       // optionnel : complète en carré noir (image très large)
 "hook": {"until": 3.0, "top": 200, "lines": [                // OBLIGATOIRE : accroche écrite en très gros dès la 1re image (1 à 3 lignes)
   {"text": "Les anneaux de Saturne", "size": 118, "color": "ink"},
   {"text": "font à peine", "size": 118, "color": "ink"},
   {"text": "10 m d'épaisseur ?!", "size": 170, "color": "pink", "under": true, "underColor": "gold"}]},   // dernière ligne = le choc
 "center": {"photo": "saturne",
            "annot": [{"text": "vraie photo !", "color": "pink", "under": true, "pos": "tl"}],   // optionnel (valeur par défaut)
            "tagline": {"text": "elle flotterait !", "on": "flotter"}},                           // sous la photo, calée sur un mot de la 1re phrase
 "scenes": [
  {"say": ["Tu savais que … ?"]},                                    // 1re phrase = question d'accroche (centre)
  {"say": ["En fait, …,"], "note": [ … éléments … ]},                 // une scène avec "note" = une nouvelle zone de la planche
  {"say": ["donc …"]},                                                // sans "note" : la voix continue sur la note précédente
  {"fin": true, "say": ["Abonne-toi pour d'autres histoires sur l'univers, et envoie la vidéo à quelqu'un que ça va faire rêver."]}
 ],
 "caption": "…", "hashtags": ["#saturne", "#espace", "#planetes", "#science", "#universenbref"],
 "sources": ["https://science.nasa.gov/…"]
}
```

## Éléments d'une note (dans l'ordre, de haut en bas)
Tous acceptent `"on": "mot"` = l'élément s'écrit quand la voix prononce ce mot (cherché dans la phrase de la note puis les suivantes),
sinon il suit l'élément précédent ; et `"row": "same"` = à droite de l'élément précédent au lieu d'une nouvelle ligne.

| élément | champs |
|---|---|
| texte | `{"t":"text","text":"= 243 jours","size":"xl|l|m|s|xs","color":"ink|pink|gold|soft|white","circle":true,"under":true,"count":{"to":460,"fmt":"+ de {n} °C","dec":0}}` |
| croquis | `{"t":"sketch","kind":"…","scale":0.8}` — `clock`, `orbit`, `thermo` (se remplit avec le compteur de la note), `sunrise`, `sun`, `rotation`, `clouds`, `planet` (`ring`), `compare` (`big`, `small`, `ratio`), `ray` (`from`, `to`), `ruler` (`label`), `mountains` (`big`, `small`), `horizon`, `hourglass`, `rocket`, `constellation`, `moon`, `wave`, `star`, `arrowdown` |
| photo secondaire | `{"t":"photo","img":"id","annot":[{"text":"sol à 460 °C","pos":"tl|tr|bl|br|c","color":"white","arrow":[0.6,0.4]}]}` |
| photo ronde | `{"t":"round","img":"id","flip":true,"arrow":false}` (découpée en rond, flèche de rotation par défaut) |

Tailles : `xl` 190 px, `l` 120, `m` 92 (Caveat), `s` 62, `xs` 48 (Kalam). Une ligne trop large est réduite automatiquement.
Chiffres **en chiffres à l'écran**, **en lettres dans la voix** ; pas de points de suspension dans la voix ; **20–30 s (≈ 460–680 caractères au total, fin comprise)**, 4 notes.

## Contrôle (gratuit, sans voix)
`bash engine/build.sh backlog/NNN-slug --mock` : vérifie le texte, la légende, les photos, la mise en page et l'absence de chevauchement,
puis écrit `build/preview.jpg` (image finale = couverture) et `build/key_*.jpg`.

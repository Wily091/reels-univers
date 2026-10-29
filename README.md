# reels-univers

Reels Instagram automatiques sur l'univers : un épisode JSON → voix ElevenLabs → vidéo motion design (style « Nébuleuse »).

- `engine/` : moteur de rendu (Playwright + Canvas), voix (`tts.py`), musique originale générée, mixage (`build.sh`)
- `episodes/AAAA-MM-JJ/episode.json` : un épisode (format : `docs/EPISODE_FORMAT.md`)
- `.github/workflows/build.yml` : à chaque nouvel épisode poussé, rendu + publication du MP4 en release
- `CLAUDE.md` : procédure quotidienne suivie par la tâche programmée

Secret requis : `ELEVENLABS_API_KEY` (Settings → Secrets and variables → Actions).

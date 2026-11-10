#!/bin/bash
# Mixage validé : voix seule normalisée, musique 0,22 en sidechain sous la voix, fondu final, limiteur. Aucun silence ajouté.
# usage : mix.sh voice.wav music.wav END out.wav
V=$1; M=$2; E=$3; O=$4; F=$(python3 -c "print($E-1.3)")
ffmpeg -y -v error -i "$V" -i "$M" -filter_complex "[0:a]highpass=f=70,loudnorm=I=-16:TP=-2:LRA=7,aresample=48000,apad=whole_dur=$E,asplit=2[v][vk];[1:a]aresample=48000,volume=0.22,apad=whole_dur=$E,atrim=0:$E[m];[m][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[md];[v][md]amix=inputs=2:normalize=0:duration=first,atrim=0:$E,afade=t=out:st=$F:d=1.2,alimiter=limit=0.89[o]" -map "[o]" -ac 2 -ar 48000 "$O"

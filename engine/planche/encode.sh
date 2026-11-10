#!/bin/bash
# usage : encode.sh dossier_images mix.wav sortie.mp4
ffmpeg -y -v error -framerate 30 -i "$1/%04d.jpg" -i "$2" -c:v libx264 -profile:v high -preset slow -crf 18 -maxrate 10M -bufsize 20M -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart "$3"

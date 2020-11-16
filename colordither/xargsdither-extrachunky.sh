xargs -i bash -c "RAND=\$(python3 alternate.py)
./dither.py '{}' > dither.ppm && convert -filter point -resize 800% dither.ppm dither\$RAND.png && eom dither\$RAND.png"

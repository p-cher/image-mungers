xargs -i bash -c "./dither.py '{}' > dither.ppm && convert dither.ppm dither\$(python3 alternate.py).png && eom dither.ppm"

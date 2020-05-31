#!/usr/bin/env bash
convert -verbose "$1" -colorspace Gray -colorspace RGB "$2" "$3" -virtual-pixel Tile -fx "v.p{u[2].p*v.w,u.p*v.h}" "$4"

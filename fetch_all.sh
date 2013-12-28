#!/bin/bash

for location in 33114 33125 33650 33720 33730 33770 33830 40160 40210 40410 40460
do
  python fetch_pubs.py --avendre-alouer --paru-vendu --logic-immo --se-loger --le-bon-coin --pages-jaunes --immo-street $location &
done

wait
python update_locations.py

for location in 33830 33380 33160 33980 33480 33680 33138 33680 33740 33950 33970 33510
do
  python fetch_pubs.py --avendre-alouer --paru-vendu --logic-immo --se-loger --le-bon-coin --pages-jaunes --immo-street $location &
done

wait
python update_locations.py

for location in 40110 40160 40170 40200 40210 40260 40560 40600
do
  python fetch_pubs.py --avendre-alouer --paru-vendu --logic-immo --se-loger --le-bon-coin --pages-jaunes --immo-street $location &
done

wait
python update_locations.py

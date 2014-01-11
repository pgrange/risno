#!/bin/bash

. $HOME/.config/risno

nb_running=0
for location in $POSTAL_CODE
do
  python fetch_pubs.py --avendre-alouer --paru-vendu --logic-immo --se-loger --le-bon-coin --pages-jaunes --immo-street $location &
  nb_running=$((nb_running + 1))
  if [ $nb_running -eq 8 ]
  then
    # 8 parallel fetches max
    nb_running=0
    wait
    python update_locations.py
  fi
done

wait
python update_locations.py

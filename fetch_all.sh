#!/bin/bash

. etc/risnorc

#Fetching for zip code in parallel
nb_running=0
for location in $POSTAL_CODE
do
  python fetch_pubs.py --avendre-alouer --paru-vendu --logic-immo --se-loger --le-bon-coin --pages-jaunes --immo-street --zip $location &
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

#fetching for region
python fetch_pubs.py --avendre-alouer --paru-vendu --logic-immo --se-loger --le-bon-coin --pages-jaunes --immo-street --region $REGION 

python update_locations.py

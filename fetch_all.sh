#!/bin/bash

# Load configuration
[[ -f /etc/opt/risno ]] && . /etc/opt/risno
[[ -f $HOME/.config/risno ]] && . $HOME/.config/risno

#Fetching for zip code in parallel
nb_running=0
for location in $POSTAL_CODE
do
  python -u fetch_pubs.py --avendre-alouer --paru-vendu --logic-immo --se-loger --le-bon-coin --pages-jaunes --immo-street --belle-immobilier --zip $location &
  nb_running=$((nb_running + 1))
  if [ $nb_running -eq 8 ]
  then
    # 8 parallel fetches max
    nb_running=0
    wait
    python -u update_locations.py
  fi
done
wait
python -u update_locations.py &

#fetching for region
(python -u fetch_pubs.py --avendre-alouer --region $REGION; python -u update_locations.py) &
(python -u fetch_pubs.py --logic-immo --region $REGION; python -u update_locations.py) &
(python -u fetch_pubs.py --se-loger --region $REGION; python -u update_locations.py) &
(python -u fetch_pubs.py --le-bon-coin --region $REGION; python -u update_locations.py) &
(python -u fetch_pubs.py --pages-jaunes --region $REGION; python -u update_locations.py) &
(python -u fetch_pubs.py --immo-street --region $REGION; python -u update_locations.py) &
(python -u fetch_pubs.py --belle-immobilier --region $REGION; python -u update_locations.py) &

wait
python -u update_locations.py

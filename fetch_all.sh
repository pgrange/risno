#!/bin/bash

. etc/risnorc

for location in $POSTAL_CODE
do
    python fetch_pubs.py --avendre-alouer --paru-vendu --logic-immo --se-loger --le-bon-coin --pages-jaunes --immo-street $location &
done
wait
python update_locations.py

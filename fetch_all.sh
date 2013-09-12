#!/bin/bash

for location in 33114 33125 33650 33720 33730 33770 33830 40160 40210 40410 40460
do
  python fetch_paruvendu.py $location
  python fetch_logic_immo.py $location
  python fetch_se_loger.py $location
  python fetch_le_bon_coin.py $location
done

for location in 33830 33380 33160 33980 33480 33680 33138 33680 33740 33950 33970 33510
do
  python fetch_paruvendu.py $location
  python fetch_logic_immo.py $location
  python fetch_se_loger.py $location
  python fetch_le_bon_coin.py $location
done


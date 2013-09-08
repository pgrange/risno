#!/bin/bash

for location in 33114 33125 33650 33720 33730 33770 33830 40160 40210 40410 40460
do
  python fetch_le_bon_coin.py $location
  python fetch_logic_immo.py $location
done

python fetch_se_loger.py

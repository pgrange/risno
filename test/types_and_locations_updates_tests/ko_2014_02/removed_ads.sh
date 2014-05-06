#!/bin/bash

comm -23 \
  <(cat sample_data_2014_02.csv | cut -d';' -f1 | sort) \
  <(cat ../sample_data/*.csv | grep -v '#OK' | grep -v '#Ok' | cut -d';' -f1 | sort)

#!/bin/bash
set -eo pipefail

mkdir -p output/logs

# Remove extra whitespace
cat data/ammo.csv | sed -r "s/^\ +//g" | sed -r "s/\ *,\ */,/g" > output/ammo.csv

# RML mapping
$RML -m mapping.ttl -o output/ammo_.ttl -d
$RML -m mapping_hisco.ttl -o output/hisco.ttl -d -v

# Post-process
python src/postprocess.py add_altlabels data/coo1980.ttl output/coo1980.ttl --logfile output/logs/postprocess.log
python src/postprocess.py remove_empty_literals output/ammo_.ttl output/ammo_2.ttl --logfile output/logs/postprocess.log
cat output/ammo_2.ttl output/coo1980.ttl output/hisco.ttl | rapper - "http://ldf.fi/ammo/" -i turtle -o turtle > output/ammo_combined.ttl

python src/postprocess.py remove_unused_hisco output/ammo_combined.ttl output/ammo_.ttl --logfile output/logs/postprocess.log

rapper -i turtle -o turtle output/ammo_.ttl > output/ammo.ttl

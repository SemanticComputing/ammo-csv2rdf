#!/bin/bash
set -eo pipefail

mkdir -p output/logs

# Remove extra whitespace
cat data/ammo.csv | sed -r "s/^\ +//g" | sed -r "s/\ *,\ */,/g" > output/ammo.csv

# Change hisco_45 value 0 to 00
cat data/hisco_45.csv | sed -r "s/^([0-9]+),0,/\1,00,/g" > output/hisco_45.csv

# RML mapping
$RML -m mapping.ttl -o output/_ammo.ttl -d
$RML -m mapping_hisco.ttl -o output/_hisco.ttl -d -v

# Post-process
python src/postprocess.py add_altlabels data/coo1980.ttl output/coo1980.ttl --logfile output/logs/postprocess.log

python src/postprocess.py get_localnames output/_ammo.ttl output/_ammo_2.ttl --logfile output/logs/postprocess.log
python src/postprocess.py remove_empty_literals output/_ammo_2.ttl output/_ammo_3.ttl --logfile output/logs/postprocess.log
cat output/_ammo_3.ttl output/coo1980.ttl output/_hisco.ttl | rapper - "http://ldf.fi/ammo/" -i turtle -o turtle > output/_ammo_combined.ttl

# python src/postprocess.py add_en_labels output/_ammo_combined.ttl output/_ammo_combined_2.ttl --logfile output/logs/postprocess.log
python src/postprocess.py remove_unused_hisco output/_ammo_combined.ttl output/_ammo_.ttl --logfile output/logs/postprocess.log

rapper -i turtle -o turtle output/_ammo_.ttl > output/ammo.ttl

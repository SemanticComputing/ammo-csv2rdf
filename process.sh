#!/bin/bash
set -eo pipefail

mkdir -p output/logs

$RML -m mapping.ttl -o output/ammo_.ttl -d
$RML -m mapping_hisco.ttl -o output/hisco_.ttl -d -v

python src/postprocess.py add_altlabels data/coo1980_.ttl output/coo1980.ttl
python src/postprocess.py remove_empty_literals output/ammo_.ttl output/ammo_2.ttl
cat output/ammo_2.ttl output/coo1980.ttl output/hisco.ttl | rapper - "http://ldf.fi/ammo/" -i turtle -o turtle > output/ammo_combined.ttl

python src/postprocess.py remove_unused_hisco output/ammo_combined.ttl output/ammo_.ttl

rapper -i turtle -o turtle output/ammo_.ttl > output/ammo.ttl

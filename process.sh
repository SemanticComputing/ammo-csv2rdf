#!/bin/bash
set -eo pipefail

mkdir -p output/logs

$RML -m mapping.ttl -o output/ammo_.ttl -d -v
$RML -m mapping_hisco.ttl -o output/hisco_.ttl -d -v

python src/postprocess.py add_altlabels data/coo1980_.ttl output/coo1980.ttl
python src/postprocess.py remove_empty_literals output/ammo_.ttl output/ammo.ttl
python src/postprocess.py remove_empty_literals output/hisco_.ttl output/hisco.ttl  # To prettify the file with namespaces

# rapper -i turtle -o turtle output/hisco_.ttl > output/hisco.ttl

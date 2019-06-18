#!/bin/bash
set -eo pipefail

mkdir -p output/logs

#rml -m mapping.ttl -o output/ammo.ttl -d -v

python src/postprocess.py add_altlabels data/coo1980.ttl output/coo1980_final.ttl
python src/postprocess.py remove_empty_literals output/ammo.ttl output/ammo_final.ttl

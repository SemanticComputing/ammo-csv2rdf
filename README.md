# AMMO CSV-RDF conversion.

Requires [rmlmapper-java](https://github.com/RMLio/rmlmapper-java).

Run the conversion with environment variable `RML` set:
```
RML="path to rmlmapper-java" ./process.sh
```

Input data required:
- AMMO spreadsheet _(data/ammo.csv)_ as CSV
- HISCO tables from http://hdl.handle.net/10622/ja9b8o
- HISCAM U1 table _(data/hiscam_u1.csv)_ from http://www.camsis.stir.ac.uk/hiscam/
- Classification of Occupations 1980 upper ontology _(data/coo1980.ttl)_ derived from http://www.doria.fi/handle/10024/98855

# AMMO CSV-RDF conversion.

Requires [rmlmapper-java](https://github.com/RMLio/rmlmapper-java).

Preprocess the data:
```
# Remove whitespace once
sed -i -r "s/^\ +//g" data/ammo.csv &&
sed -i -r "s/\ *,\ */,/g" data/ammo.csv
```

Run the conversion with environment variable `RML` set:
```
RML="path to rmlmapper-java" ./process.sh
```

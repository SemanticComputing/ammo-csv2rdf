# AMMO CSV-RDF conversion.

Requires [rmlmapper-java](https://github.com/RMLio/rmlmapper-java).

Add `rml` as an alias to `java -jar rmlmapper-4.3.2-r92.jar`, with the correct path to the JAR file. 

Preprocess the data:
```
# Remove whitespace once
sed -i -r "s/^\ +//g" data/ammo.csv &&
sed -i -r "s/\ *,\ */,/g" data/ammo.csv
```

Run the conversion:
```
./process.sh
```

# AMMO CSV-RDF conversion.

Requires [rmlmapper-java](https://github.com/RMLio/rmlmapper-java).

Usage:

```
# Remove whitespace once
sed -i -r "s/(\"\ +)|(\ +\")/\"/g" data/ammo.csv

# Run the RML conversion
java -jar rmlmapper-4.3.2-r92.jar -m mapping.ttl -o ammo.ttl
```

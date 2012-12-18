Yo gral..

Make a few tweaks for comments..

1) added airports.2 yaml

This is same idea, but the fields are now an array
and there's more data in there eg
table name, credits etc etc

NOTE..
Check down for aptrange...
we could be clever here and include the mapnick and style data, openlayers ??
would this be the right place to put itt ?



2) new config..
this loads up the database and need to be configred on each load with the "-c" connection option
eg
create_tables -c database.yaml


3) oo Helper..

The yaml is laoded adn case as an object..
so 
yaml_dic['fields'] 
becomes
yaml_oo.fields

yaml_dic.fields.[4].name

 

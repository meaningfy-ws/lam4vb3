This folder contains a series of LinkedPipes ETL transformation workflows.

To run them, fist install and run the [LinkedPiped ETL](https://linkedpipes.com/). The installation instructions are available [here](https://etl.linkedpipes.com/installation/).
 
## The ontology metadata
The ontology annotations and metadata supported by the PyLode Tool are:

* dc:contributor
* dc:creator
* dc:date
* dc:description, used with a literal as object, if you want to add a textual description to the ontology, or with a resource as object, if you want to trasclude that resource (e.g., a picture) as description of an entity.
* dc:publisher
* dc:rights
* dc:title
* owl:backwardCompatibleWith
* owl:incompatibleWith
* owl:versionInfo
* owl:versionIRI
* rdfs:comment - description 
* rdfs:isDefinedBy
* rdfs:label
* skos:scopeNote
* 
# Introduction
 this file contains definition of custom forms for the LAM project in VB3. The imports specified 
 below are needed for a clearer user experience.  

# Imports

* LAM-SKOS-AP model
* EuVoc ontology
* CDM ontology
* CDM annotations ontology
* SHACL
* DC Terms

Prefix definitions:
```turtle
prefix cdm:  <http://publications.europa.eu/ontology/cdm#>
prefix ann:  <http://publications.europa.eu/ontology/annotation#> 
prefix dct:  <http://purl.org/dc/terms/>
prefix euvoc: <http://publications.europa.eu/ontology/euvoc#> 
prefix sh:   <http://www.w3.org/ns/shacl#> 
prefix lam: <http://publications.europa.eu/ontology/lam-skos-ap#> 
prefix skos: <http://www.w3.org/2004/02/skos/core#>
```

# Custom forms (PEARL definitions)

## Properties annotation configuration
Id: annotationConfiguration

Show property: shacl:name

Used for: lam:hasAnnotationConfiguration

Ref: 
```turtle

prefix lam: <http://publications.europa.eu/ontology/lam-skos-ap#> 
prefix sh:   <http://www.w3.org/ns/shacl#> 
prefix dct:  <http://purl.org/dc/terms/> 
prefix euvoc: <http://publications.europa.eu/ontology/euvoc#> 
prefix cdm:  <http://publications.europa.eu/ontology/cdm#> 
prefix ann:  <http://publications.europa.eu/ontology/annotation#> 
prefix skos: <http://www.w3.org/2004/02/skos/core#>

prefix	xsd: 	<http://www.w3.org/2001/XMLSchema#>
prefix	rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix	dc:		<http://purl.org/dc/terms/>
prefix	coda: 	<http://art.uniroma2.it/coda/contracts/>
			
rule it.uniroma2.art.semanticturkey.customform.form.annotationConfiguration id:annotationConfiguration {
	nodes = {
 		shapeId uri(coda:randIdGen("res", {})) .
		nameLang literal userPrompt/lang .
		nameLit literal(coda:langString($nameLang)) userPrompt/name .
		path uri userPrompt/path .
		min literal^^xsd:integer userPrompt/min .
		max literal^^xsd:integer userPrompt/max .
		description literal userPrompt/description .
		hasValue uri userPrompt/hasValue .
		pattern literal userPrompt/pattern .
		editorialNote literal userPrompt/editorialNote .
		class uri userPrompt/class .
	}
	graph = {
		$shapeId a lam:AnnotationConfiguration .
		$shapeId sh:name $nameLit .
		$shapeId lam:path $path .
		OPTIONAL{
			$shapeId sh:minCount $min .
		}
		OPTIONAL{
			$shapeId sh:maxCount $max .
		}
		OPTIONAL{
			$shapeId sh:description $description .
		}
		OPTIONAL{
			$shapeId sh:hasValue $hasValue .
		}
		OPTIONAL{
			$shapeId sh:pattern $pattern .
		}
		OPTIONAL{
			$shapeId skos:editorialNote $editorialNote .
		}
		OPTIONAL{
			$shapeId sh:class $class .
		}
	}
}
```

## Classes property configuration
Id: propertyConfiguration

Show property: shacl:name

Used for: lam:hasPropertyConfiguration

Ref: 
```turtle

prefix lam: <http://publications.europa.eu/ontology/lam-skos-ap#> 
prefix sh:   <http://www.w3.org/ns/shacl#> 
prefix dct:  <http://purl.org/dc/terms/> 
prefix euvoc: <http://publications.europa.eu/ontology/euvoc#> 
prefix cdm:  <http://publications.europa.eu/ontology/cdm#> 
prefix ann:  <http://publications.europa.eu/ontology/annotation#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>

prefix	xsd: 	<http://www.w3.org/2001/XMLSchema#>
prefix	rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix	dc:		<http://purl.org/dc/terms/>
prefix	coda: 	<http://art.uniroma2.it/coda/contracts/>
			
rule it.uniroma2.art.semanticturkey.customform.form.propertyConfiguration id:propertyConfiguration {
	nodes = {
 		shapeId uri(coda:randIdGen("res", {})) .
		nameLang literal userPrompt/lang .
		nameLit literal(coda:langString($nameLang)) userPrompt/name .
		path uri userPrompt/path .
		min literal^^xsd:integer userPrompt/min .
		max literal^^xsd:integer userPrompt/max .
		description literal userPrompt/description .
		hasValue uri userPrompt/hasValue .
		pattern literal userPrompt/pattern .
		editorialNote literal userPrompt/editorialNote .
	}
	graph = {
		$shapeId a lam:PropertyConfiguration .
		$shapeId sh:name $nameLit .
		$shapeId lam:path $path .
		OPTIONAL{
			$shapeId sh:minCount $min .
		}
		OPTIONAL{
			$shapeId sh:maxCount $max .
		}
		OPTIONAL{
			$shapeId sh:description $description .
		}
		OPTIONAL{
			$shapeId sh:hasValue $hasValue .
		}
		OPTIONAL{
			$shapeId sh:pattern $pattern .
		}
		OPTIONAL{
			$shapeId skos:editorialNote $editorialNote .
		}
	}
}
``` 

## Classes mapping property configuration
Id: mappingPropertyConfiguration

Show property: shacl:name

Used for: lam:classifyWith

Ref: 
```turtle
prefix lam: <http://publications.europa.eu/ontology/lam-skos-ap#> 
prefix sh:   <http://www.w3.org/ns/shacl#> 
prefix dct:  <http://purl.org/dc/terms/> 
prefix euvoc: <http://publications.europa.eu/ontology/euvoc#> 
prefix cdm:  <http://publications.europa.eu/ontology/cdm#> 
prefix ann:  <http://publications.europa.eu/ontology/annotation#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>

prefix	xsd: 	<http://www.w3.org/2001/XMLSchema#>
prefix	rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix	dc:		<http://purl.org/dc/terms/>
prefix	coda: 	<http://art.uniroma2.it/coda/contracts/>
			
rule it.uniroma2.art.semanticturkey.customform.form.mappingPropertyConfiguration id:mappingPropertyConfiguration {
	nodes = {
 		shapeId uri(coda:randIdGen("res", {})) .
		nameLang literal userPrompt/lang .
		nameLit literal(coda:langString($nameLang)) userPrompt/name .
		path uri userPrompt/path .
		min literal^^xsd:integer userPrompt/min .
		max literal^^xsd:integer userPrompt/max .
		description literal userPrompt/description .
		hasValue uri userPrompt/hasValue .
		pattern literal userPrompt/pattern .
		editorialNote literal userPrompt/editorialNote .
	}
	graph = {
		$shapeId a lam:MappingPropertyConfiguration .
		$shapeId sh:name $nameLit .
		$shapeId lam:path $path .
		OPTIONAL{
			$shapeId sh:minCount $min .
		}
		OPTIONAL{
			$shapeId sh:maxCount $max .
		}
		OPTIONAL{
			$shapeId sh:description $description .
		}
		OPTIONAL{
			$shapeId sh:hasValue $hasValue .
		}
		OPTIONAL{
			$shapeId sh:pattern $pattern .
		}
		OPTIONAL{
			$shapeId skos:editorialNote $editorialNote .
		}
	}
}
``` 

## LAM path configuration
Id: lamPathConfiguration

Show property: shacl:name

Used for: lam:path

Ref: 
```turtle
prefix lam: <http://publications.europa.eu/ontology/lam-skos-ap#>
prefix sh:   <http://www.w3.org/ns/shacl#>
prefix dct:  <http://purl.org/dc/terms/>
prefix euvoc: <http://publications.europa.eu/ontology/euvoc#>
prefix cdm:  <http://publications.europa.eu/ontology/cdm#>
prefix ann:  <http://publications.europa.eu/ontology/annotation#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>

prefix	xsd: 	<http://www.w3.org/2001/XMLSchema#>
prefix	rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix	dc:		<http://purl.org/dc/terms/>
prefix	coda: 	<http://art.uniroma2.it/coda/contracts/>

rule it.uniroma2.art.semanticturkey.customform.form.lamPathConfiguration id:lamPathConfiguration {
	nodes = {
 		shapeId uri(coda:randIdGen("res", {})) .
		nameLang literal userPrompt/lang .
		nameLit literal(coda:langString($nameLang)) userPrompt/name .
		uriPath uri userPrompt/uriPath .
	}
	graph = {
		$shapeId a lam:path .
		$shapeId sh:name $nameLit .
		$shapeId lam:path $uriPath .
	}
}
```
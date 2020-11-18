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
		class uri userPrompt/class .
		value uri userPrompt/value .
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
			$shapeId sh:class $class .
		}
		OPTIONAL{
			$shapeId sh:value $value .
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
		class uri userPrompt/class .
		value uri userPrompt/value .
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
			$shapeId sh:class $class .
		}
		OPTIONAL{
			$shapeId sh:value $value .
		}
	}
}
``` 

## Classes mapping configuration
Id: mappingConfiguration

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

prefix	xsd: 	<http://www.w3.org/2001/XMLSchema#>
prefix	rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix	dc:		<http://purl.org/dc/terms/>
prefix	coda: 	<http://art.uniroma2.it/coda/contracts/>
			
rule it.uniroma2.art.semanticturkey.customform.form.mappingConfiguration id:mappingConfiguration {
	nodes = {
 		shapeId uri(coda:randIdGen("res", {})) .
		nameLang literal userPrompt/lang .
		nameLit literal(coda:langString($nameLang)) userPrompt/name .
		path uri userPrompt/path .
		min literal^^xsd:integer userPrompt/min .
		max literal^^xsd:integer userPrompt/max .
		class uri userPrompt/class .
		value uri userPrompt/value .
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
			$shapeId sh:class $class .
		}
		OPTIONAL{
			$shapeId sh:value $value .
		}
	}
}
``` 
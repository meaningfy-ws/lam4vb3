# Initiative for Modeling the Legal Analysis Methodology


The aim of the project is to provide a level of formalisation to the Legal Analise Methodology used at the European Publications Office for the legal document metadata. 

The formalisation steps are as follows: 
- from unstructured text (e.g. word files) to controlled tabular structure (e.g. Excel)
- from controlled tabular structure to a tailor made SKOS representation, called LAM-SKOS-AP
- from LAM-SKOS-AP representation to OWL2 formal ontology
- from LAM-SKOS-AP representation to a structured technical documentation and a user manual

  
| Key | Value |
| :--- | :--- | 
| Project start| June 2019 |
| Project expected end| December 2019 |
| Authors | Eugeniu Costetchi |
| Contributors | Juraj Kuba, Marcin Baryn |
 
 
# Project deliverables 

The project is split into two phases aiming at providing three kinds of deliverables: documents, transformation scripts and formal data/models. The originally planned deliverables are as follows. 

## Phase 1
| Key | Value |
| :--- | :--- | 
| Status | ongoing |
| Expected delivery| October 2019|

| Work package | Description |
| :--- | :--- |
|  WP1.1 | (Doc1) Requirements specification - A preliminary requirement specification for LAM project (based on the preliminary analisys) |
|  WP1.2 | (Model spec1) LAM-SKOS-AP model - A model to structure LAM data suitable for loading into VocBench3 |
|  WP1.3 | (Script1) Excel to LAM-SKOS-AP transformation script  - A command line script to transform the Structured Excel files into LAM-SKOS-AP suitable for loading into VB3 |
|  WP1.4 | (Doc2) Documentation of Excel structure - Specification of how the excel files should be structured in order to undergo the transformation, i.e. the description of the input data for the script. |
|  WP1.5 | (Data1) LAM data and loading it into VocBench 3 – Load and setup data in VocBench3 OP environment |

## Phase 2
| Key | Value |
| :--- | :--- |
|Status| planned|
|Expected delivery| December 2019| 


| Work package  | Description |
| :--- | :--- |
|  WP2.1 | (BugFix1) Bug fixes in LAM-SKOS-AP (errata) and transformation script (Script1) – based on the new findings |
|  WP2.2 | (Assistance1) Assistance/training for LAM team to edit data in VocBench3 |
|  WP2.3 | (Model spec2) Transformation rules from LAM-SKOS-AP data into formal LAM ontology and SHACL shapes |
|  WP2.4 | (Script2) Script to transform LAM-SKOS-AP data into formal LAM OWL ontology  – the desired LAM ontology |
|  WP2.5 | (Script3) Script to transform LAM-SKOS-AP data into formal LAM SHACL shapes– the desired shapes for validation purposes |
|  WP2.6 | (Script4) Script to transform LAM-SKOS-AP data into a structured document (e.g. DITA) for PDF/HTML/DocBook disseminations |
|  WP2.7 | (Data2) test release of LAM OWL ontology |
|  WP2.8 | (Data3) test release of LAM SHACL shapes |
|  WP2.9 | (Data4) test release of LAM XML & PDF documentation |


# Running the scripts 

Running all the cells from the lam2vb3 jupyter notebook will generate the current RDF representation of the LAM project.

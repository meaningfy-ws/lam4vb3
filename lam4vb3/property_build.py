"""
property_build
Date: 29.06.19
Author: Eugeniu Costetchi
Email: costezki.eugen@gmail.com

This module deals with loading and generating RDF structures for the metadata/property worksheets

"""

# Mapping LAM and CELEX metadata worksheet columns¶ (LAM and CELEX have identical property definitions)

LAM_PROPERTIES_DESCRIPTIVE_COLUMNS = {
    'Code': 'skos:notation',
    'Label': 'skos:prefLabel@en',
    'property': 'sh:path',
    'controlled value _property': 'sh:class',
    'Definition': 'skos:definition@en',
    'Example - cellar notice': 'skos:example',
    'Analytical methodology': 'skos:scopeNote@en',
    'Specific cases': 'skos:historyNote@en',
    'Comments': 'skos:editorialNote@en',
    'Changes to be done': 'skos:editorialNote@en',
}

LAM_PROPERTIES_ANNOTATION_COLUMNS = [('annotation_1', 'controlled value_annotation_1'),
                                     ('annotation_2', 'controlled value_annotation_2'),
                                     ('annotation_3', 'controlled value_annotation_3'),
                                     ('annotation_4', 'controlled value_annotation_4'),
                                     ('annotation_5', 'controlled value_annotation_5'),
                                     ('annotation_6', 'controlled value_annotation_6'),
                                     ('annotation_7', 'controlled value_annotation_7'), ]

LAM_COLLECTION_COLUMNS = ["Classification level 1", "Classification level 2", "Classification level 3"]

# Mapping CELEX metadata worksheet columns¶

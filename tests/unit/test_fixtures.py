import rdflib
from rdflib import RDF, SKOS


def test_get_celex_classes_rdf(lam_celex_classes_graph):
    graph = lam_celex_classes_graph
    collections_in_graph = []
    concepts_in_graph = []
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Collection):
        collections_in_graph.append(subj)
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
        concepts_in_graph.append(subj)
    assert isinstance(graph, rdflib.Graph)
    # number of "triples" in the Graph
    assert len(graph) == 2341
    assert len(collections_in_graph) == 24
    assert len(concepts_in_graph) == 276


def test_get_lam_proprieties_rdf(lam_properties_graph):
    graph = lam_properties_graph
    collections_in_graph = []
    concepts_in_graph = []
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Collection):
        collections_in_graph.append(subj)
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
        concepts_in_graph.append(subj)
    assert isinstance(graph, rdflib.Graph)
    # number of "triples" in the Graph
    assert len(graph) == 3895
    assert len(collections_in_graph) == 21
    assert len(concepts_in_graph) == 154


def test_get_lam_classes_rdf(lam_classes_graph):
    graph = lam_classes_graph
    collections_in_graph = []
    concepts_in_graph = []
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Collection):
        collections_in_graph.append(subj)
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
        concepts_in_graph.append(subj)
    assert isinstance(graph, rdflib.Graph)
    # number of "triples" in the Graph
    assert len(graph) == 3366
    assert len(collections_in_graph) == 20
    assert len(concepts_in_graph) == 20

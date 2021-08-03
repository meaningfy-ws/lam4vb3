import rdflib
from rdflib import RDF, SKOS


def test_get_celex_classes_rdf(get_celex_classes_rdf):
    graph = get_celex_classes_rdf
    collections_in_graph = []
    concepts_in_graph = []
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Collection):
        collections_in_graph.append(subj)
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
        concepts_in_graph.append(subj)
    assert isinstance(graph, rdflib.Graph)
    # number of "triples" in the Graph
    assert len(graph) == 6804
    assert len(collections_in_graph) == 24
    assert len(concepts_in_graph) == 276


def test_get_lam_proprieties_rdf(get_lam_proprieties_rdf):
    graph = get_lam_proprieties_rdf
    collections_in_graph = []
    concepts_in_graph = []
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Collection):
        collections_in_graph.append(subj)
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
        concepts_in_graph.append(subj)
    assert isinstance(graph, rdflib.Graph)
    # number of "triples" in the Graph
    assert len(graph) == 3424
    assert len(collections_in_graph) == 21
    assert len(concepts_in_graph) == 149


def test_get_lam_classes_rdf(get_lam_classes_rdf):
    graph = get_lam_classes_rdf
    collections_in_graph = []
    concepts_in_graph = []
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Collection):
        collections_in_graph.append(subj)
    for subj in graph.subjects(predicate=RDF.type, object=SKOS.Concept):
        concepts_in_graph.append(subj)
    assert isinstance(graph, rdflib.Graph)
    # number of "triples" in the Graph
    assert len(graph) == 2930
    assert len(collections_in_graph) == 20
    assert len(concepts_in_graph) == 20

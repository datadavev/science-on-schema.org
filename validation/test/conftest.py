'''

'''
import logging
import pytest
import os
import sosov.verify
import rdflib
import pyshacl.rdfutil

SOSO = "http://science-on-schema.org/1.1.0/validation/shacl"
BASE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def inflateSubgraph(g, sg, ts, depth=0, max_depth=100):
    """
    Inflate the subgraph sg to contain all children of sg appearing in g.

    Args:
        g (Graph): The master graph from which the subgraph is extracted
        sg (Graph): The subgraph, modified in place
        ts (iterable of triples): list of triples, the objects of which identify subjects to copy from g
        depth (integer): tracks depth of recursion
        max_depth (integer): maximum recursion depth for retrieving terms

    Returns:
        None
    """
    new_trips = []
    for t in ts:
        if isinstance(t[2], rdflib.term.Identifier):
            trips = g.triples((t[2], None, None))
            for trip in trips:
                if not trip in sg:
                    sg.add(trip)
                    new_trips.append(trip)
    if len(new_trips) > 0:
        depth += 1
        if depth > max_depth:
            return
        inflateSubgraph(g, sg, new_trips, depth=depth)
    return


def getSubgraph(g, subject=None, predicate=None, max_depth=100):
    """
    Retrieve the subgraph of g with subject and predicate.

    Given the graph ``g``, extract the subgraph identified
    as the object of the triple with subject ``subject`` and predicate ``predicate``.

    Args:
        g (Graph): Source graph
        subject (URIRef): Subject of the root of the subgraph to retrieve
        predicate (URIRef): Predicate of the root of the subgraph to retrieve
        max_depth (integer): Maximum recursion depth

    Returns:
        (Graph) A subgraph of g

    """
    sg = rdflib.ConjunctiveGraph()
    sg.namespace_manager = rdflib.namespace.NamespaceManager(g)
    sg += g.triples((subject, predicate, None))
    inflateSubgraph(g, sg, sg, max_depth=max_depth)
    return sg




def getShapeGraph(name):
    fname = os.path.join(BASE_FOLDER,"SHACL",name)
    return sosov.loadGraph(fname)

def getDataGraph(name):
    fname = os.path.join(BASE_FOLDER,"data",name)
    return sosov.loadGraph(fname)

def getResultWithSourceShape(result_graph, source_shape, data_graph):
    '''
    Given a SHACL validation result graph, get the ValidationResults with specified sourceShape
    '''
    #ss = rdflib.URIRef(source_shape)
    ss = source_shape
    vr = rdflib.URIRef("http://www.w3.org/ns/shacl#ValidationResult")
    fn = rdflib.URIRef("http://www.w3.org/ns/shacl#focusNode")
    for s in result_graph.subjects(rdflib.URIRef("http://www.w3.org/ns/shacl#sourceShape"), ss):
        fng = getSubgraph(result_graph, subject=s, predicate=fn)
        print("*"*20)
        print(fng.serialize(format="turtle", indent=2).decode())
        print("*"*20)
        # should only ever be one
        foc_node = next(fng.objects(s, fn))
        print(f"focus node = {foc_node}")
        is_bnode = isinstance(foc_node, rdflib.BNode)
        print(f"focus node is bnode: {is_bnode}")
        #exn = "unknown"
        #if is_bnode:
        #    exn = next(fng.objects(foc_node, rdflib.URIRef("http://science-on-schema.org/1.1.0/validation/shacl#test_fails")))
        #    for oo in fng.objects(foc_node, rdflib.URIRef("http://science-on-schema.org/1.1.0/validation/shacl#test_fails")):
        #        print(f"test_fails: {oo}")
        #else:
        #    exn = next(data_graph.objects(foc_node, rdflib.URIRef("http://science-on-schema.org/1.1.0/validation/shacl#test_fails")))
        #    for oo in data_graph.objects(foc_node,
        #                          rdflib.URIRef("http://science-on-schema.org/1.1.0/validation/shacl#test_fails")):
        #        print(f"test_fails: {oo}")
        #print(f"Expected value = {exn}")


## Test cases start with "test_"

'''
def test_id():
    return
    sg = getShapeGraph("test_id.ttl")
    print("SHAPE:")
    print(sg.serialize(format="turtle", indent=2).decode())
    dg = getDataGraph("test_id/id_ok.json")
    print("DATA:")
    print(dg.serialize(format="turtle", indent=2).decode())
    conforms, result_graph, result_text = sosov.verify.validateSHACL(
                        dg, shacl_graph=sg, ont_graph=None, advanced=False
                    )
    print(result_graph.serialize(format="turtle", indent=2).decode())
    getResultWithSourceShape(result_graph, "http://science-on-schema.org/1.1.0/validation/shacl#IDShape", dg)
    assert conforms==True


def testcommon():
    return
    sg = getShapeGraph("soso_common.ttl")
    dg = getDataGraph("test_id/id_ok.json")
    conforms, result_graph, result_text = sosov.verify.validateSHACL(
                        dg, shacl_graph=sg, ont_graph=None, advanced=False
                    )
    print(result_graph.serialize(format="turtle", indent=2).decode())
    getResultWithSourceShape(result_graph, "http://science-on-schema.org/1.1.0/validation/shacl#identifierDatasetProperty", dg)
    assert conforms==True

def test_manifest():
    return
    tests = sosov.loadGraph("testcases.json")
    rdftype = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    testtype = rdflib.URIRef(f"{SOSO}#TestCase")
    soso_data = rdflib.URIRef(f"{SOSO}#data")
    soso_shacl = rdflib.URIRef(f"{SOSO}#shacl")
    soso_applytest = rdflib.URIRef(f"{SOSO}#apply")
    for testcase in tests.subjects(rdftype, testtype):
        tg = getSubgraph(tests, subject=testcase)
        doapply = next(tg.objects(testcase, soso_applytest)).toPython()
        if doapply:
            print("="*40)
            print(tg.serialize(format="turtle", indent=2).decode())
            dg = rdflib.ConjunctiveGraph()
            dg.parse(next(tg.objects(testcase,soso_data)), format="json-ld")
            sg = rdflib.ConjunctiveGraph()
            sg.parse(next(tg.objects(testcase,soso_shacl)), format="turtle")
            print("*** DATA ***")
            print(dg.serialize(format="turtle", indent=2).decode())
            print("*** SHACL ***")
            print(sg.serialize(format="turtle", indent=2).decode())
            conforms, result_graph, result_text = sosov.verify.validateSHACL(
                dg, shacl_graph=sg, ont_graph=None, advanced=False
            )
            print("*** RESULT ***")
            print(result_graph.serialize(format="turtle", indent=2).decode())
    assert False
'''

def getValidationResultSourceShapes(result_graph):
    '''

    Args:
        result_graph:

    Returns:
        list of sh:sourceShape object URIs
    '''
    logging.debug("getValidationResultSourceShapes")
    vr = rdflib.URIRef("http://www.w3.org/ns/shacl#ValidationResult")
    fn = rdflib.URIRef("http://www.w3.org/ns/shacl#focusNode")
    rdftype = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    ss = rdflib.URIRef("http://www.w3.org/ns/shacl#sourceShape")
    #vro = result_graph.subjects()
    res = []
    for s in result_graph.subjects(rdftype, vr):
        logging.debug("validation_result = %s", s)
        source_shape = next(result_graph.objects(s, ss))
        logging.debug("source_shape: %s", source_shape)
        res.append(source_shape)
        pass
    return res


class ShaclTestItem(pytest.Item):
    def __init__(self, name, parent, test_case, test_graph, expected_failures):
        logging.debug("ShaclTestItem.__init__")
        super().__init__(name, parent)
        self.test_case = test_case
        self.test_graph = test_graph
        self.expected_failures = expected_failures

    def runtest(self):
        logging.debug("ShaclTestItem.runtest")
        soso_data = rdflib.URIRef(f"{SOSO}#data")
        soso_shacl = rdflib.URIRef(f"{SOSO}#shacl")
        print("=" * 40)
        print(self.test_graph.serialize(format="turtle", indent=2).decode())

        # Load the data
        dg = rdflib.ConjunctiveGraph()
        dg.parse(next(self.test_graph.objects(self.test_case, soso_data)), format="json-ld")

        # Load the SHACL
        sg = rdflib.ConjunctiveGraph()
        sg.parse(next(self.test_graph.objects(self.test_case, soso_shacl)), format="turtle")
        print("*** DATA ***")
        print(dg.serialize(format="turtle", indent=2).decode())
        print("*** SHACL ***")
        print(sg.serialize(format="turtle", indent=2).decode())

        # Evaluate
        conforms, result_graph, result_text = sosov.verify.validateSHACL(
            dg, shacl_graph=sg, ont_graph=None, advanced=False
        )
        print("*** RESULT ***")
        print(result_graph.serialize(format="nt", indent=2).decode())
        #
        # Now need to compare each failure with the expected failures.
        # These should match (unordered)
        # Error conditions are:
        #   1. more validation failures than expected
        #   2. less validation failures than expected
        # Get list of expected
        # Get list of actual
        actual_sourceShapes = getValidationResultSourceShapes(result_graph)
        # Verify each actual in expected
        # Verify each expected in actual
        n_ex_fails = 0
        n_actual_fails = 0
        for ex_fail in self.expected_failures:
            print(f"Expected failure: {ex_fail}")
            if ex_fail in actual_sourceShapes:
                n_actual_fails += 1
            #getResultWithSourceShape(result_graph, ex_fail, dg)
            n_ex_fails += 1
        print(f"Number of expected failures = {n_ex_fails}")
        assert n_ex_fails == n_actual_fails


class ShaclTestCases(pytest.File):
    def collect(self):
        logging.debug("ShaclTestCases.collect")
        tests = sosov.loadGraph(str(self.fspath))
        rdftype = rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        testtype = rdflib.URIRef(f"{SOSO}#TestCase")
        soso_applytest = rdflib.URIRef(f"{SOSO}#apply")
        for testcase in tests.subjects(rdftype, testtype):
            tg = getSubgraph(tests, subject=testcase)
            ex_fails = tests.objects(testcase, rdflib.URIRef(f"{SOSO}#fails"))
            doapply = next(tg.objects(testcase, soso_applytest)).toPython()
            if doapply:
                yield ShaclTestItem.from_parent(self, name=str(testcase), test_case=testcase, test_graph=tg, expected_failures=ex_fails)


def pytest_collect_file(parent, path):
    if path.ext == ".json" and path.basename.startswith("test"):
        print("pytest_collect_file path= " + str(path))
        return ShaclTestCases.from_parent(parent, fspath=path)



from src.LabeledGraph import LabeledGraph
from src.MyCNF import MyCNF


def test_manual(manual_suite, algo, tmp_path):
    graph_file = tmp_path / 'graph.txt'
    graph_file.write_text('\n'.join(manual_suite['edges']))

    g = LabeledGraph.from_txt(graph_file)

    gr = MyCNF.from_text(manual_suite['cnf'])

    actual = algo(g, gr)

    expected = manual_suite['expected']

    assert actual == expected
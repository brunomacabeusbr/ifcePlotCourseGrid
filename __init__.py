if __name__ == '__main__':
    import networkx as nx
    from coursegrid import ifce_computer_enginner
    from collegesystem import qacademico
    import grahdraw
    import sys

    graph = nx.DiGraph()

    if len(sys.argv) == 3:
        qacademico.read(graph, *sys.argv[1:])
    else:
        # todo: fazer para ser configurável o curso que vai mostrar a grade
        ifce_computer_enginner.load(graph)

    grahdraw.draw(graph)

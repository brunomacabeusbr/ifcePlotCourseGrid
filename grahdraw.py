import networkx as nx
import matplotlib.pyplot as plt
import math
from discipline import DisciplineStatus


def draw(graph):
    pos = dict()

    def get_points(r, nodes):
        teta = 360 / len(nodes)
        teta = math.radians(teta)

        x = 0
        for i in nodes:
            pos[i] = (
                (r * 1) * (math.cos(teta * x)),
                (r * 1) * (math.sin(teta * x))
            )
            x += 1

    semesters = {1: [], 2: [], 3: [], 4: [], 5: []}
    for i in graph.nodes():
        semesters[i.semester].append(i)

    for k, v in semesters.items():
        get_points(k, v)

    # Colorir nodes e apagar edges desnecessárias
    color_list = []

    for i in graph.nodes():
        if i.status == DisciplineStatus.passado:
            color_list.append('blue')
            for i2 in graph.in_edges(i):
                graph.remove_edge(*i2)
        elif i.status == DisciplineStatus.reprovado:
            color_list.append('red')
        elif i.status == DisciplineStatus.cursando:
            color_list.append('green')
        else:
            color_list.append('black')

    # Draw
    nx.draw(graph, pos=pos, with_labels=True,
            font_size=10, font_color='r',
            node_color=color_list, node_size=1000, alpha=0.25)

    # Desenhar círculos dos semestres
    fig = plt.gcf()

    fig.gca().add_artist(plt.Circle((0, 0), 1.5, color='green', fill=False, alpha=0.25))
    fig.gca().add_artist(plt.Circle((0, 0), 2.5, color='green', fill=False, alpha=0.25))
    fig.gca().add_artist(plt.Circle((0, 0), 3.5, color='green', fill=False, alpha=0.25))
    fig.gca().add_artist(plt.Circle((0, 0), 4.5, color='green', fill=False, alpha=0.25))
    fig.gca().add_artist(plt.Circle((0, 0), 5.5, color='green', fill=False, alpha=0.25))

    # Exibir
    plt.show()

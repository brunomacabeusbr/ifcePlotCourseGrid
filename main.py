import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors
import math
from abc import ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from enum import Enum


class MatterStatus(Enum):
    nothing = 1
    cursando = 2
    reprovado = 3
    passado = 4

class Matter:
    list_objects = {}

    @staticmethod
    def get_object(name):
        return Matter.list_objects[name]

    def __init__(self, name, semester):
        self.name = name
        self.semester = semester
        self.status = MatterStatus.nothing
        Matter.list_objects[name] = self

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return self.name

graph = nx.DiGraph()

# 1
md = Matter('Matemática Discreta', 1)
lp1 = Matter('Lógica De Programação I', 1)
ed = Matter('Eletronica Digital', 1)
c1 = Matter('Calculo I', 1)
graph.add_node(lp1)
graph.add_node(md)
graph.add_node(ed)
graph.add_node(c1)

# 2
lm = Matter('Lógica Matemática', 2)
lp2 = Matter('Lógica De Programação Ii', 2)
ea = Matter('Eletronica Analógica', 2)
c2 = Matter('Cálculo Ii', 2)
f1 = Matter('Física I', 2)
graph.add_node(lm)
graph.add_node(lp2)
graph.add_node(ea)
graph.add_node(c2)
graph.add_node(f1)
graph.add_edge(lp1, lp2)
graph.add_edge(c1, c2)

# 3
iaa = Matter('Introdução A Análise De Algorítimos', 3)
eda = Matter('Estrutura De Dados', 3)
ac = Matter('Arquitetura De Computadores', 3)
edi = Matter('Equações Diferenciais', 3)
f2 = Matter('Física Ii', 3)
graph.add_node(iaa)
graph.add_node(eda)
graph.add_node(ac)
graph.add_node(edi)
graph.add_node(f2)
graph.add_edge(md, iaa)
graph.add_edge(lm, iaa)
graph.add_edge(lp2, ed)
graph.add_edge(ed, ac)
graph.add_edge(c2, ed)
graph.add_edge(c1, f2)
graph.add_edge(f1, f2)

# 4
atc = Matter('Aspectos Teóricos Da Computação', 4)
po = Matter('Pesquisa E Ordenação', 4)
pp = Matter('Paradígmas Da Programação', 4)
mm = Matter('Microcontroladores E Miroprocessadores', 4)
mct = Matter('Metodologia Científica E Tecnologica', 4)
graph.add_node(atc)
graph.add_node(po)
graph.add_node(pp)
graph.add_node(mm)
graph.add_node(mct)
graph.add_edge(iaa, atc)
graph.add_edge(eda, po)
graph.add_edge(eda, pp)
graph.add_edge(ac, mm)
graph.add_edge(ea, mm)

# ?
rccd = Matter('Rede De Computadores E Comunicação De Dados', 5)
so1 = Matter('Sistemas Operacionais I', 5)
pe = Matter('Probabilidade E Estatística', 5)
graph.add_node(rccd)
graph.add_node(so1)
graph.add_node(pe)

# Q-Academico
phantom = webdriver.PhantomJS()
phantom.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=1001')

form = phantom.find_element_by_id('txtLogin')
form.send_keys(coloque sua matricula do qacademico, Keys.TAB, coloque sua senha do qacademico)
phantom.find_element_by_id('btnOk').click()

phantom.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=2032')

def get_element_set_semester_year():
    return phantom.find_element_by_id('cmbanos')

def get_element_set_semester_period():
    return phantom.find_element_by_id('cmbperiodos')

total_semester_year = len(get_element_set_semester_year().find_elements_by_tag_name('option'))
total_semester_period = len(get_element_set_semester_period().find_elements_by_tag_name('option'))

for current_semester_year in range(total_semester_year):
    for current_semester_period in range(total_semester_period):
        get_element_set_semester_year().find_elements_by_tag_name('option')[::-1][current_semester_year].click()
        get_element_set_semester_period().find_elements_by_tag_name('option')[::-1][current_semester_period].click()
        phantom.find_element_by_id('Exibir').click()

        for i in phantom.find_elements_by_css_selector('tbody > .conteudoTexto '):
            matter_name = i.find_elements_by_tag_name('td')[0].text.title()
            matter_status = i.find_elements_by_tag_name('td')[13].text.title()
            if matter_status == 'Aprovado':
                Matter.get_object(matter_name).set_status(MatterStatus.passado)
            elif matter_status == 'Cursando':
                Matter.get_object(matter_name).set_status(MatterStatus.cursando)
            elif matter_status == 'Reprovado':
                Matter.get_object(matter_name).set_status(MatterStatus.reprovado)

# Posicionar
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
    if i.status == MatterStatus.passado:
        color_list.append('blue')
        for i2 in graph.in_edges(i):
            graph.remove_edge(*i2)
    elif i.status == MatterStatus.reprovado:
        color_list.append('red')
    elif i.status == MatterStatus.cursando:
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

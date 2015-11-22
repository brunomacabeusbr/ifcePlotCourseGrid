import sys
import os
import re
import unicodedata

def replace_accents(string):
    return ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))

my_path = os.path.dirname(os.path.realpath(__file__))
coursegrid_folder = my_path + '/coursegrid/'

dict_translate = {}
dict_dependencies = {}

with open(sys.argv[1], 'r') as f:
    content = f.readlines()

regexp_discipline = re.compile(r'\[(\d+)] (.*)')
regexp_dependence = re.compile(r'(.*?) > ')
for i in content:
    search_result = regexp_discipline.search(i)
    if search_result is not None:
        semester, discipline = search_result.groups()
    else:
        continue

    discipline_variable = ''.join([i for i in replace_accents(discipline).lower().split(' ')])
    if discipline not in dict_translate:
        dict_translate[discipline] = (int(semester), discipline_variable)


    search_result = regexp_dependence.search(i)
    if search_result is None:
        continue

    dependencies = search_result.groups()[0]
    dict_dependencies[discipline] = dependencies.split(' + ')


def get_discipline_by_semester(semester):
    return [(k, v[1]) for k, v in dict_translate.items() if v[0] == semester]

with open(coursegrid_folder + sys.argv[2] + '.py', 'x') as f:
    content = \
"""from discipline import Discipline


def load(graph):
"""
    current_semester = 0
    while True:
        current_semester += 1
        current_disciplines = get_discipline_by_semester(current_semester)

        if len(get_discipline_by_semester(current_semester)) == 0:
            break

        content += "    # " + str(current_semester) + "\n"

        for i in current_disciplines:
            content += "    " + i[1] + " = Discipline('" + i[0] + "', " + str(current_semester) + ")\n"

        for i in current_disciplines:
            content += "    graph.add_node(" + i[1] + ")\n"

        for i in current_disciplines:
            if i[0] in dict_dependencies:
                for i2 in dict_dependencies[i[0]]:
                    content += "    graph.add_edge(" + dict_translate[i2][1] + ", " + i[1] + ")\n"

    f.write(content)

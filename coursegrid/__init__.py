from . import ifce_computer_enginner

def select_course_grid(graph, college, code_course):
    if college == 'ifce' and code_course == '01502':
        ifce_computer_enginner.load(graph)
    else:
        raise ValueError('O seu curso ainda não foi catalogado! Ajude-me catalgando-o ou então comprando um brownie para mim')
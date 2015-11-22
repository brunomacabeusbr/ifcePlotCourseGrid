from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from discipline import Discipline, DisciplineStatus
from coursegrid import select_course_grid
import re


def read(graph, login, password):
    phantom = webdriver.PhantomJS()
    phantom.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=1001')

    form = phantom.find_element_by_id('txtLogin')
    form.send_keys(login, Keys.TAB, password)
    phantom.find_element_by_id('btnOk').click()

    phantom.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=2032')

    regexp_code_course = re.compile(r'\(\d{5}(\d{5})')
    code_course = regexp_code_course.search(
        phantom.find_elements_by_css_selector('[face="Verdana, Arial, Helvetica, sans-serif"]')[1].text.strip()
    ).groups()[0]
    select_course_grid(graph, 'ifce', code_course)

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
                    Discipline.get_object(matter_name).set_status(DisciplineStatus.passado)
                elif matter_status == 'Cursando':
                    Discipline.get_object(matter_name).set_status(DisciplineStatus.cursando)
                elif matter_status == 'Reprovado':
                    Discipline.get_object(matter_name).set_status(DisciplineStatus.reprovado)
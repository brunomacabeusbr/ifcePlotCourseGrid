# ifcePlotCourseGrid
Generator image of course grid

<img src="http://i.imgur.com/CJfN8Td.png">

## Dependências
* python3 `sudo apt-get install python3`
* phantomjs `sudo apt-get install phantomjs`
* networkx `sudo pip3 install networkx`
* matplotlib `sudo pip3 install matplotlib`

## Como usar o ifPCG
* Exibir a grade normalmente de Engenharia da Computação `python3 __init__.py`
* Exibir a grade do seu curso, com destaque nas cadeiras já cursadas/cursando `python3 __init__.py (sua matrícula no qacadêmico) (sua senha)`, por exemplo `python3 __init__.py 20130015020072 macabeusgalã`

## Eu quero o meu curso!
* Caso o seu curso não esteja catalogado, você mesmo pode facilmente fazer isso! Basta criar o arquivo CGP (Course Grid Pre-Processed)
* <a href="https://github.com/brunomacabeusbr/ifcePlotCourseGrid/blob/master/example.cgp">Exemplo de um CGP</a>

### Explicação detalhada do CGP
    [1] Lógica De Programação I

Desse modo, irá criar uma cadeira do primeiro semestre chamada "Lógica De Programação I".
Primeiro deve-se escrever os cochetes contendo o semestre da cadeira e depois o nome da cadeira.

    Lógica De Programação I > [2] Lógica De Programação Ii

Desse modo, além de criar a cadeira "Lógica De Programação Ii", seguindo as mesmas regras apresentadas acima, irá dizer que o pré-requisito dela é a "Lógica De Programação I".
O pré-requisito já tem que ter sido criado anteriormente!

O terror de todos os estudantes são as cadeiras com vários pré-requisitos. Pois é, elas infelizmente existem. Para dizer para o ifPCG que uma cadeira tem vários pré-requisitos, basta usar o sinal de mais

    Calculo I + Física I > [3] Física Ii

É obrigatório haver exatamente um espaço em volta do `>` e do `+`. É obrigatório haver um espaço após o `]`.

Após gerar o CGP, use o script `cgp2py.py` da seguinte forma: `python3 cgp2py.py example.cgp nomedoarquivopy`. Ele irá gerar o py já na pasta `coursegrid/`. Depois disso, edite o arquivo `coursegrid/__init__.py` para carregar o py gerado.

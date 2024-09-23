# import
import random
import math
import itertools
from random import choices
import timeit
import pandas as pd

# definição das variáveis
dist = 0  # distância para coletar os medicamentos solicitados
# variáveis que armazenam as coordenadas dos medicamentos (usadas para calcular as distâncias entre eles)
x1 = 0
y1 = 0
x2 = 0
y2 = 0
dist_converg = [] # armazena a distância para gerar o gráfico de convergência
seq_converg = [] # armazena a sequência que gerou cada distância para gerar o gráfico da trajetória
med_pedidos = []  # lista de medicamentos solicitados pelo profissional da farmácia
coord_pedidos = []  # lista de coordenadas dos medicamentos solicitados
elemento = []  # lista criada para realizar a permutação e definir todas as sequências possíveis para quando a quantidade de medicamento é menor que 10
listas = []  # lista que irá conter as possíveis sequências-soluções de medicamentos
lista_dist = []  # lista que armazena as distâncias das sequências criadas
lista_dist_filhos = []  # lista que armazena as distâncias dos descendentes gerados
pais_selecionados = []  # lista das sequências selecionadas para gerar novos descendentes
dist_pais_selecionados = [] # lista que armazena as distâncias das sequências selecionadas para gerar novos descendentes
coordenadas_4coleta = [] # coordenadas da sequência que obteve menor distância
filhos = []  # lista dos descendentes obtidos após o cruzamento
# lista de medicamentos disponíveis nas prateleiras
lista_med = ['acetilcisteina', 'albendazol', 'buscopan', 'captopril', 'diazepam', 'eritromicina', 'estradiol', 'fentonila', 'fluoxetina', 'gardenal', 'glucagon',
             'heparina', 'hidrocodona', 'ibuprofeno', 'ivermectina', 'levotiroxina 25', 'losartana', 'metadona', 'nistatina', 'omeprazol', 'paracetamol', 'propanolol',
             'ranitidina', 'risperidona', 'tilenol']
lista_med_solicitado = []  # lista dos medicamentos solicitados
# lista das coordenadas dos medicamentos disponíveis nas prateleiras
coord_med = [(1, 1), (1, 4), (1, 10), (1, 21), (2, 5), (2, 17), (2, 24), (3, 5.5), (3, 11.5), (3, 19.5), (3, 23.5),
             (4, 1.5), (4, 5.5), (4, 13.5), (4, 21.5), (5, 3.5), (5, 7.5), (5, 17.5), (5, 19.5), (5, 23.5), (6, 1.5), (6, 5.5),
             (6, 15.5), (6, 21.5), (7, 18.5)]

# cria a função fitness que será aplicada nas sequências geradas para verificar seus desempenhos (calcular a distância que o robô irá percorrer)
def dist(lista_indiv, coord_pedidos, qtd_medicamento):
    for j in range(len(lista_indiv)):
        seq = lista_indiv[j]
        # calcula a distância inicial do robô (0,0) até o primeiro medicamento
        x1, y1 = coord_pedidos[seq[0]-1]
        dist = math.sqrt((abs(x1 - 0)**2 + (abs(y1 - 0))**2))

        # calcula a distância entre os medicamentos definidos na sequência seq
        for i in range((qtd_medicamento-1)):
            x1, y1 = coord_pedidos[(seq[i]-1)]
            x2, y2 = coord_pedidos[(seq[i+1]-1)]
            dist = math.sqrt((abs(x2 - x1)**2 + (abs(y2 - y1))**2)) + dist

        # calcula a distância do último medicamento até o ponto inicial que o robô deverá retornar (0,0)
        x2, y2 = coord_pedidos[seq[-1]-1]
        dist = math.sqrt((abs(x2 - 0)**2 + (abs(y2 - 0))**2)) + dist

        lista_dist.append(dist)
    return lista_dist

# profissional define a quantidade de medicamentos a ser coletada
qtd_medicamento = int(
    input('Digite a quantidade de medicamentos a ser coletada: '))

# profissional informa quais os medicamentos deverão ser coletados
h = 1
qtd_medicamento_loop = qtd_medicamento
while h <= qtd_medicamento_loop:
    med = input('Medicamento: ')
    if med in lista_med:  # medicamento solicitado é procurado na lista de medicamentos disponíveis
        if med not in lista_med_solicitado:
            # recupera a poição do medicamento solicitado na lista dos disponíveis
            indice_lista_med = lista_med.index(med)
            # recupera a coordenada do medicamento solicitado na lista de coordenadas dos medicamentos disponíveis (mesmo índice da lista_med)
            coord_pedidos.append(coord_med[indice_lista_med])
            # armazena o medicamento solicitado numa lista
            lista_med_solicitado.append(med)
        # checa se o medicamento já foi solicitado
        else:
            print('{} já solicitado. Digite outro medicamento: ' .format(med))
            qtd_medicamento_loop += 1
    else:
        # se o medicamento não for encontrado na lista (por erro de digitação), é pedido ao profissional que digite novamente o nome do medicamento
        print('{} não encontrado. Digite novamente: ' .format(med))
        qtd_medicamento_loop += 1

    h += 1

# o programa foi alocado dentro de uma função para que se pudesse verificar o tempo de execução dele
def programa():
    listas = []
    lista_dist = []
    lista_dist_filhos = []
    elemento = []
    pais_selecionados = []
    filhos = []
    dist_pais_selecionados = []
    pais_filhos = []
    dist_pais_filhos = []

    # gera a população inicial de forma aleatória
    tam_pop_inicial = 5000 # tamanho da população inicial
    while tam_pop_inicial >= 1:
        elemento = random.sample(
            range(1, (qtd_medicamento+1)), qtd_medicamento)
        if elemento not in listas:
            listas.append(elemento)
            tam_pop_inicial -= 1
        if (elemento in listas) and (qtd_medicamento <= 9):
            tam_pop_inicial -= 1

    # para cada sequência que foi criada é calculada a distância total a ser percorrida (função fitness)
    lista_dist = dist(listas, coord_pedidos, qtd_medicamento)

    # realiza a seleção por elitismo (será escolhida uma fração dos indivíduos gerados, definida pela taxa de seleção)
    taxa_selecao = 0.05 # taxa de seleção
    # se a quantidade de medicamentos for menor que quatro, todos os indivíduos gerados são selecionados
    if (qtd_medicamento <= 3):
        taxa_selecao = 1
    
    quantidade_selecionados = int(taxa_selecao*len(listas))

    # caso em que a quantidade de sequências é par
    if ((quantidade_selecionados % 2) == 0):
        for i in range(quantidade_selecionados):
            dist_pais_selecionados.append(min(lista_dist))
            pais_selecionados.append(listas[lista_dist.index(min(lista_dist))])
            listas.remove(listas[lista_dist.index(min(lista_dist))])
            lista_dist.remove(min(lista_dist))
    # caso em que a quantidade de sequências é ímpar
    if ((quantidade_selecionados % 2) != 0) and (quantidade_selecionados != 1):
        for i in range(quantidade_selecionados+1):
            dist_pais_selecionados.append(min(lista_dist))
            pais_selecionados.append(listas[lista_dist.index(min(lista_dist))])
            listas.remove(listas[lista_dist.index(min(lista_dist))])
            lista_dist.remove(min(lista_dist))
    # caso em que a quantidade de medicamentos é um
    if quantidade_selecionados == 1:
        dist_pais_selecionados.append(min(lista_dist))
        pais_selecionados.append(listas[lista_dist.index(min(lista_dist))])
        listas.remove(listas[lista_dist.index(min(lista_dist))])
        lista_dist.remove(min(lista_dist))
    
    # armazena a menor distância e a sequência da menor distância dentre os indivíduos pais gerados
    menor_dist = min(dist_pais_selecionados)
    seq_menor_dist = pais_selecionados[dist_pais_selecionados.index(
           menor_dist)]
        
    # armazena as distâncias dos pais selecionados para gerar o gráfico de convergência
    dist_converg.append(round(menor_dist,2))

    # realiza o processo de criação de descendentes
    geracao = 120 # quantidade de gerações do processo evolutivo
    while geracao >= 1:
        pais_selecionados_cruzamento = []
        pais_selecionados_intactos = []
        dist_pais_selecionados_cruzamento = []
        dist_pais_selecionados_intactos = []
        taxa_cruzamento = 0.9 # taxa de cruzamento

        # seleciona os pais que passarão pelo processo de cruzamento
        for pai in pais_selecionados:
            sorteio_cruzamento = random.random()
            if sorteio_cruzamento <= taxa_cruzamento:
                pais_selecionados_cruzamento.append(pai)
                dist_pais_selecionados_cruzamento.append(dist_pais_selecionados[pais_selecionados.index(pai)])
            else:
                pais_selecionados_intactos.append(pai)
                dist_pais_selecionados_intactos.append(dist_pais_selecionados[pais_selecionados.index(pai)])
        qtd_pais_selecionados_cruzamento = int(len(pais_selecionados_cruzamento))

        # separa as sequências selecionadas por pares para realizar o cruzamento
        for w in range(0, len(pais_selecionados_cruzamento)-1, 2):
            p1 = pais_selecionados_cruzamento[(w)]
            p2 = pais_selecionados_cruzamento[(w+1)]

            # cria o vetor dos descendentes
            f1 = [0]*qtd_medicamento
            f2 = [0]*qtd_medicamento

            # cria as listas que serão utilizadas no processo de cruzamento e mutação a cada geração criada
            indices_string_bit_1 = []
            elementosp1_posicao_zeros_string_bit = []
            elementosp2_posicao_zeros_string_bit = []
            indices_elementosp1_ordem_p2 = []
            elementosp1_ordem_p2 = []
            indices_elementosp2_ordem_p1 = []
            elementosp2_ordem_p1 = []

            # cria uma lista com bits aleatórios. O tamanho da lista deve ser igual ao tamanho das sequências
            string_bit = random.choices(range(0, 2), k=qtd_medicamento)

            for i in range(len(string_bit)):
                # recupera a posição dos 1s da lista criada
                if string_bit[i] == 1:
                    indices_string_bit_1.append(i)

                # cria uma lista com os elementos das sequências correspondentes aos 0s da lista de bits
                if string_bit[i] == 0:
                    elementosp1_posicao_zeros_string_bit.append(p1[i])
                    elementosp2_posicao_zeros_string_bit.append(p2[i])

            # copia para os descendentes os elementos das sequências referentes às posições dos 1s da lista de bits criada
            for l in indices_string_bit_1:
                f1[l] = p1[l]
                f2[l] = p2[l]

            # cria uma lista dos índices em p2 dos elementos de p1 nas posições dos 0s
            for m in elementosp1_posicao_zeros_string_bit:
                indices_elementosp1_ordem_p2.append(p2.index(m))

            # cria uma lista dos índices em p1 dos elementos de p2 nas posições dos 0s
            for q in elementosp2_posicao_zeros_string_bit:
                indices_elementosp2_ordem_p1.append(p1.index(q))

            # cria uma lista de elementos de p1 nas posições dos 0s, mas na ordem em que aparecem em p2
            for r in range(len(indices_elementosp1_ordem_p2)):
                elementosp1_ordem_p2.append(elementosp1_posicao_zeros_string_bit[indices_elementosp1_ordem_p2.index(
                        min(indices_elementosp1_ordem_p2))])
                indices_elementosp1_ordem_p2[indices_elementosp1_ordem_p2.index(
                        min(indices_elementosp1_ordem_p2))] = 99999999999

            # cria uma lista de elementos de p2 nas posições dos 0s, mas na ordem em que aparecem em p1
            for s in range(len(indices_elementosp2_ordem_p1)):
                elementosp2_ordem_p1.append(elementosp2_posicao_zeros_string_bit[indices_elementosp2_ordem_p1.index(
                        min(indices_elementosp2_ordem_p1))])
                indices_elementosp2_ordem_p1[indices_elementosp2_ordem_p1.index(
                        min(indices_elementosp2_ordem_p1))] = 99999999999

            # adiciona em f1 os elementos de p1 nas posições dos 0s, mas na ordem que aparecem em p2 nas posições onde estão os 0s
            for t in range(len(f1)):
                if f1[t] == 0:
                    f1[t] = elementosp1_ordem_p2[0]
                    elementosp1_ordem_p2.remove(elementosp1_ordem_p2[0])

            # adiciona em f2 os elementos de p2 nas posições dos 0s, mas na ordem que aparecem em p1 nas posições onde estão os 0s
            for u in range(len(f2)):
                if f2[u] == 0:
                    f2[u] = elementosp2_ordem_p1[0]
                    elementosp2_ordem_p1.remove(elementosp2_ordem_p1[0])

            # processo de mutação (com taxa de ocorrência baixa na população)
            taxa_mutacao = 0.05 # taxa de mutação
            sorteio_mutacao1 = random.random()
            sorteio_mutacao2 = random.random()

            # recupera um terço da quantidade de medicamentos contida nos descendentes. A mutação ocorre no terço do meio
            divisao = int(qtd_medicamento/3)

            if sorteio_mutacao1 <= taxa_mutacao:
                # realiza mutação na parte do meio do f1 (embaralha)
                lista_mutacao_f1 = f1[divisao:-divisao]
                random.shuffle(lista_mutacao_f1)
                f1[divisao:-divisao] = lista_mutacao_f1

            if sorteio_mutacao2 <= taxa_mutacao:
                # realiza mutação na parte do meio do f2 (embaralha)
                lista_mutacao_f2 = f2[divisao:-divisao]
                random.shuffle(lista_mutacao_f2)
                f2[divisao:-divisao] = lista_mutacao_f2

            # adiciona os descendentes gerados na lista de filhos
            filhos.append(f1)
            filhos.append(f2)

        #limpa a lista que contém as distâncias das sequências e de seus descendentes (para garantir que valores das gerações anteriores não estarão presentes)
        lista_dist.clear()
        lista_dist_filhos.clear()

        # calcula a distância de todos os descendentes gerados
        lista_dist_filhos = dist(filhos, coord_pedidos, qtd_medicamento)

        # adiciona os pais que realizaram cruzamento à lista para depois selecionar os mais aptos entre a população total
        pais_filhos.extend(pais_selecionados_cruzamento)

        # adiciona as distâncias dos pais que realizaram cruzamento à lista para depois selecionar os mais aptos
        dist_pais_filhos.extend(dist_pais_selecionados_cruzamento)

        # adiciona os filhos à lista para depois selecionar os mais aptos entre a população total
        for item in filhos:
            if item not in pais_filhos:
                pais_filhos.append(item)
                dist_pais_filhos.append(lista_dist_filhos[filhos.index(item)])

        # limpa as listas para a nova geração
        pais_selecionados_cruzamento.clear()
        pais_selecionados.clear()
        filhos.clear()
        dist_pais_selecionados_cruzamento.clear()
        dist_pais_selecionados.clear()
        lista_dist_filhos.clear()

        # adiciona os pais que cruzaram e os filhos e suas distâncias nas listas para selecionar os mais aptos para a próxima geração
        for i in range(qtd_pais_selecionados_cruzamento):
            dist_pais_selecionados.append(min(dist_pais_filhos))
            pais_selecionados.append(pais_filhos[dist_pais_filhos.index(min(dist_pais_filhos))])

            # limpa as listas para a próxima geração
            pais_filhos.remove(pais_filhos[dist_pais_filhos.index(min(dist_pais_filhos))])
            dist_pais_filhos.remove(min(dist_pais_filhos))
            
        # adiciona os pais que não cruzaram e suas distâncias nas listas para selecionar os mais aptos para a próxima geração
        pais_selecionados.extend(pais_selecionados_intactos)
        dist_pais_selecionados.extend(dist_pais_selecionados_intactos)

        # limpa as listas para a próxima geração
        pais_selecionados_intactos.clear()
        pais_filhos.clear()
        dist_pais_filhos.clear()

        # seleciona o indivíduo, entre os pais que cruzaram, os filhos e os pais que não cruzaram, que obteve a menor distância e o valor dela (para cada geração)
        menor_dist = min(dist_pais_selecionados)
        seq_menor_dist = pais_selecionados[dist_pais_selecionados.index(menor_dist)]

        # armazena a menor distância de cada geração para gerar o gráfico de convergência
        dist_converg.append(round(menor_dist,2))
        
        geracao -= 1

    # adiciona o ponto de início na lista de coordenadas do percurso de coleta
    ponto_inicial = (0,0)
    coordenadas_4coleta.append(ponto_inicial)
    # recupera as coordenadas da sequência que obteve a menor distância calculada
    for i in seq_menor_dist:
        coordenadas_4coleta.append(coord_pedidos[i-1])
    coordenadas_4coleta.append(ponto_inicial)

    # cria duas listas para salvar todas as coordenadas em x e y do percurso de coleta 
    coord_x = []
    coord_y = []

    # salva todas as coordenadas em x e y do percuros de coleta nas listas criadas
    for i in coordenadas_4coleta:
        x, y = i
        coord_x.append(x)
        coord_y.append(y)

    # salva todas as distâncias de todas as gerações em um arquivo csv para gerar o gráfico de convergência
    #qtd_geracao_csv = list(range(1, 122))
    #geracao_csv = pd.DataFrame(qtd_geracao_csv, columns=['Geracao'])
    #dist_geracao_csv = pd.DataFrame(dist_converg, columns=['Dist'])
    #geracao_csv.to_csv('C:\\Users\\isabe\\OneDrive\\Área de Trabalho\\Codigos_Projeto_HU\\Gráficos de Desempenho dos Códigos\\geracao_csv_V3_9.csv', index=False)
    #dist_geracao_csv.to_csv('C:\\Users\\isabe\\OneDrive\\Área de Trabalho\\Codigos_Projeto_HU\\Gráficos de Desempenho dos Códigos\\dist_converg_V3_9.csv', index=False)
    
    # salva todas as coordenadas em x e y do percuros de coleta em um arquivo csv
    coordenada_x = pd.DataFrame(coord_x, columns=['x'])
    coordenada_y = pd.DataFrame(coord_y, columns=['y'])
    coordenada_x.to_csv('C:\\Users\\isabe\\OneDrive\\Área de Trabalho\\Codigos_Projeto_HU\\Gráficos de Desempenho dos Códigos\\x_22_2_d.csv', index=False)
    coordenada_y.to_csv('C:\\Users\\isabe\\OneDrive\\Área de Trabalho\\Codigos_Projeto_HU\\Gráficos de Desempenho dos Códigos\\y_22_2_d.csv', index=False)

    # informa ao usuário a menor distância obtida, a sequência correspondente e as coordenadas dos medicamentos da sequência recuperada
    print('A sequência {} obteve a menor distância de {}' .format(
            seq_menor_dist, menor_dist))
    print('Coordenadas finais: {}' .format(coordenadas_4coleta))

# calcula e informa o tempo de execução do função que gerou todas as possíveis sequências e calculou suas distâncias
tempo_execucao = timeit.timeit(stmt=programa, number=1)
print("Tempo médio de execução: {} segundos" .format(tempo_execucao))
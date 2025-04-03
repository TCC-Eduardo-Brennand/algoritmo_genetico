from AlgoritmoGenetico import BuscaGenetica
import pandas as pd


def analiseEstatistica():
    """Método p/ analisar estatisticamente os resultados do AG."""
    # Lista de circuitos
    circuitos = ['Spain', 'Great Britain', 'Italy']

    resultados = {}

    populacao = 50
    mutacao_pb = 0.01
    cruzamento_pb = 0.5
    geracoes = 300
    elitismo_pp = 0.1

    for circuito in circuitos:
        melhores_individuos = []

        for i in range(30):
            print(f"INICIANDO BUSCA GENÉTICA - ITERACAO: {i} - CIRCUITO: {circuito}")
            busca_genetica = BuscaGenetica(
                populacao=populacao,
                mutacao_pb=mutacao_pb,
                cruzamento_pb=cruzamento_pb,
                geracoes=geracoes,
                elitismo_pp=elitismo_pp,
                pais=circuito
            )

            _, melhor_individuo = busca_genetica.inicializarBuscaGenetica()
            melhores_individuos.append(melhor_individuo['Tempo'])

        resultados[circuito] = melhores_individuos

    df = pd.DataFrame(resultados)

    stats = pd.DataFrame({
        'Média': df.mean(),
        'Desvio Padrão': df.std()
    })

    print("\nTabela de Estatísticas:\n")
    print(stats)

    stats.to_csv('analise_estatistica4.csv', index=True)
    print("\nArquivo 'analise_estatistica.csv' gerado com sucesso!")


analiseEstatistica()

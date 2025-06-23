#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
from generatore_colorazione import GeneratoreColorazioneGrafo

def run_experiment(num_experiments, generatore_colorazione):
    """Esegui l'esperimento e raccogli i risultati."""
    results = []
    for _ in range(num_experiments):

        # colorazione = generatore_colorazione.genera_colorazione_gibbs()
        colorazione = generatore_colorazione.genera_colorazione()

        results.append(''.join(str(x) for x in colorazione.values()))
    return results


def create_diagram_1 (frequenze, generatore_colorazione):
    plt.figure(figsize=(10, 5))
    plt.scatter(frequenze.index, frequenze.values)  # s è la dimensione dei punti
    plt.xlabel('Colorazione')
    plt.ylabel('Frequenza')
    plt.title('Frequenza delle colorazioni del grafo, n=' + str(generatore_colorazione.get_n()) + ', ε=' + str(generatore_colorazione.get_epsilon()))

    # Rimuovi le etichette sull'asse x
    plt.xticks([])
    plt.grid(axis='y')

    # Mostra il grafico
    plt.tight_layout()
    plt.savefig('img/grafico_frequenza_colorazioni_n' + str(generatore_colorazione.get_n()) + '.png')  # Salva come file PNG
    plt.close()  # Chiude la figura per liberare memoria

def create_diagram_2 (frequenze, generatore_colorazione):
    """
    Mostra un diagramma a dispersione dei risultati della colorazione del grafo.

    :param results: Lista di risultati della colorazione del grafo.
    """
    # Creazione di un DataFrame con le frequenze
    frequenze_df = frequenze.reset_index()
    frequenze_df.columns = ['Colorazione', 'Occorrenze']

    # Creazione di un dizionario con le stringhe e il numero di occorrenze
    frequenze_dict = dict(zip(frequenze_df['Colorazione'], frequenze_df['Occorrenze']))

    df = pd.DataFrame(frequenze_dict.values(), columns=['Frequenze'])
    frequenze = df['Frequenze'].value_counts().sort_index()

    # Creazione del diagramma di frequenza
    plt.figure(figsize=(10, 5))
    frequenze.plot(kind='bar')
    plt.xlabel('Frequenze di colorazioni')
    plt.ylabel('Numero di colorazioni')
    plt.title('Diagramma del numero di colorazioni del grafo per frequenza, n=' + str(generatore_colorazione.get_n()) + ', ε=' + str(generatore_colorazione.get_epsilon()))
    # plt.xticks([])
    plt.grid(axis='y')

    # Mostra il grafico
    plt.tight_layout()
    plt.savefig('img/grafico_numero_colorazioni_n' + str(generatore_colorazione.get_n()) + '.png')  # Salva come file PNG
    plt.close()  # Chiude la figura per liberare memoria


grafo = {
            'A': ['B', 'C'],
            'B': ['A', 'D'],
            'C': ['A', 'D'],
            'D': ['B', 'C']
        }

generatore_colorazione = GeneratoreColorazioneGrafo(grafo)
num_experiments = 100000
results = run_experiment(num_experiments, generatore_colorazione )  # Esegui l'esperimento 10 volte
df = pd.DataFrame(results, columns=['Colorazioni'])
frequenze = df['Colorazioni'].value_counts()

create_diagram_1(frequenze, generatore_colorazione)
create_diagram_2(frequenze, generatore_colorazione)

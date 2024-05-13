import matplotlib.pyplot as plt
from flet_core.matplotlib_chart import MatplotlibChart
import numpy as np

def __plot_sim_exp__(list_q, qe_sim):
    figuraxy = plt.plot(list_q, qe_sim, 'ro', label='Dados Sincronizados')
    plt.xlabel("q Experimental (mol/kg)")
    plt.ylabel("q Simulado (mol/kg)")
    plt.title("Comparação entre dados experimentais e simulados")
    correlation = np.corrcoef(list_q, qe_sim)[0, 1]
    r2 = float(correlation**2)
    max_value1 = max(list_q)
    max_value2 = max(qe_sim)
    max_value = max(max_value1, max_value2)

    plt.plot([0, max_value], [0, max_value], 'k-')
    plt.text(max_value * 0.05, max_value * 0.9, "r$^2$ = " + str(round(r2, 4)))
    plt.close()
    grafico = MatplotlibChart(figuraxy[0].figure)
    return grafico


import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import math
from flet_core.matplotlib_chart import MatplotlibChart
import scipy.stats as st
from auxiliar import plots

def main(list_T, list_P, list_q, Tref, model, parameters, resultados):
    principal = ft.Column(controls=[ft.Divider()], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO,
                          width=800, spacing=10)

    # define listas
    qmax_list = parameters[0]
    k1_list = parameters[1]
    k2_list = parameters[2]
    outro_list = []
    if len(parameters) > 3:
        outro_list = parameters[3]

    erroQ_list = resultados

    min_error = min(erroQ_list)
    min_error_index = erroQ_list.index(min_error)

    container_width = 150
    container_height = 50

    # Estatística qmax
    q_mean = np.mean(qmax_list)
    q_std = np.std(qmax_list)
    q_min = qmax_list[min_error_index]
    intervalo_qmax = st.t.interval(0.95, len(qmax_list) - 1, loc=np.mean(qmax_list), scale=st.sem(qmax_list))

    coluna_qmax = ft.Column(controls=[ft.Text("Estatísticas do Parâmetro qmax")])
    text_q_media = ft.TextField(label="Média", value=round(q_mean, 4), read_only=True, width=container_width,
                                height=container_height)
    text_q_std = ft.TextField(label="Desvio padrão", value=round(q_std, 4), read_only=True, width=container_width,
                              height=container_height)
    text_q_min = ft.TextField(label="qmax - Menor erro", value=round(q_min, 4), read_only=True, width=container_width,
                              height=container_height)
    linha_q = ft.Row(controls=[text_q_media, text_q_std, text_q_min], spacing=10)
    intervalo_q_str = "(" + str(round(intervalo_qmax[0], 4)) + " , " + str(round(intervalo_qmax[1], 4)) + ")"
    text_intervalo_q = ft.TextField(label="Intervalo de confiança", value=intervalo_q_str, read_only=True,
                                    width=(2 * container_width + 10),
                                    height=container_height)
    coluna_qmax.controls.append(linha_q)
    coluna_qmax.controls.append(text_intervalo_q)

    k1_mean = np.mean(k1_list)
    k1_std = np.std(k1_list)
    k1_min = k1_list[min_error_index]
    intervalo_k1 = st.t.interval(0.95, len(k1_list) - 1, loc=np.mean(k1_list), scale=st.sem(k1_list))
    coluna_k1 = ft.Column(controls=[ft.Text("Estatísticas do Parâmetro K1")])
    text_k1_media = ft.TextField(label="Média", value=round(k1_mean, 4), read_only=True, width=container_width,
                                 height=container_height)
    text_k1_std = ft.TextField(label="Desvio padrão", value=round(k1_std, 4), read_only=True, width=container_width,
                               height=container_height)
    text_k1_min = ft.TextField(label="K1 - Menor erro", value=round(k1_min, 4), read_only=True, width=container_width,
                               height=container_height)
    linha_k1 = ft.Row(controls=[text_k1_media, text_k1_std, text_k1_min], spacing=10)
    intervalo_k1_str = "(" + str(round(intervalo_k1[0], 4)) + " , " + str(round(intervalo_k1[1], 4)) + ")"
    text_intervalo_k1 = ft.TextField(label="Intervalo de confiança", value=intervalo_k1_str, read_only=True,
                                     width=(2 * container_width + 10),
                                     height=container_height)
    coluna_k1.controls.append(linha_k1)
    coluna_k1.controls.append(text_intervalo_k1)

    k2_mean = np.mean(k2_list)
    k2_std = np.std(k2_list)
    k2_min = k2_list[min_error_index]
    intervalo_k2 = st.t.interval(0.95, len(k2_list) - 1, loc=np.mean(k2_list), scale=st.sem(k2_list))
    coluna_k2 = ft.Column(controls=[ft.Text("Estatísticas do Parâmetro K2")])
    text_k2_media = ft.TextField(label="Média", value=round(k2_mean, 4), read_only=True, width=container_width,
                                 height=container_height)
    text_k2_std = ft.TextField(label="Desvio padrão", value=round(k2_std, 4), read_only=True, width=container_width,
                               height=container_height)
    text_k2_min = ft.TextField(label="K2 - Menor erro", value=round(k2_min, 4), read_only=True, width=container_width,
                               height=container_height)
    linha_k2 = ft.Row(controls=[text_k2_media, text_k2_std, text_k2_min], spacing=10)
    intervalo_k2_str = "(" + str(round(intervalo_k2[0], 4)) + " , " + str(round(intervalo_k2[1], 4)) + ")"
    text_intervalo_k2 = ft.TextField(label="Intervalo de confiança", value=intervalo_k2_str, read_only=True,
                                     width=(2 * container_width + 10),
                                     height=container_height)
    coluna_k2.controls.append(linha_k2)
    coluna_k2.controls.append(text_intervalo_k2)

    principal.controls.append(coluna_qmax)
    principal.controls.append(ft.Divider())
    principal.controls.append(coluna_k1)
    principal.controls.append(ft.Divider())
    principal.controls.append(coluna_k2)
    principal.controls.append(ft.Divider())

    outro_mean = 0
    if len(outro_list) > 0:
        outro_mean = np.mean(outro_list)
        outro_std = np.std(outro_list)
        outro_min = outro_list[min_error_index]
        intervalo_outro = st.t.interval(0.95, len(outro_list) - 1, loc=np.mean(outro_list),
                                        scale=st.sem(outro_list))
        parametro = ""
        if model == 1:
            parametro = "ns"
        elif model == 2:
            parametro = "n"
        elif model == 3:
            parametro = "α"
        coluna_outro = ft.Column(controls=[ft.Text("Estatísticas do Parâmetro " + parametro)])
        text_outro_media = ft.TextField(label="Média", value=round(outro_mean, 4), read_only=True,
                                        width=container_width,
                                        height=container_height)
        text_outro_std = ft.TextField(label="Desvio padrão", value=round(outro_std, 4), read_only=True,
                                      width=container_width,
                                      height=container_height)
        text_outro_min = ft.TextField(label=parametro + " - Menor erro", value=round(outro_min, 4), read_only=True,
                                      width=container_width,
                                      height=container_height)
        intervalo_outro_str = "(" + str(round(intervalo_outro[0], 4)) + " , " + str(round(intervalo_outro[1], 4)) + ")"
        text_intervalo_outro = ft.TextField(label="Intervalo de confiança", value=intervalo_outro_str, read_only=True,
                                            width=(2 * container_width + 10),
                                            height=container_height)
        linha_outro = ft.Row(controls=[text_outro_media, text_outro_std, text_outro_min], spacing=10)
        coluna_outro.controls.append(linha_outro)
        coluna_outro.controls.append(text_intervalo_outro)
        principal.controls.append(coluna_outro)
        principal.controls.append(ft.Divider())

    erroQ_mean = np.mean(erroQ_list)
    erroQ_std = np.std(erroQ_list)
    erroQ_min = erroQ_list[min_error_index]
    intervalo_erro = st.t.interval(0.95, len(erroQ_list) - 1, loc=np.mean(erroQ_list), scale=st.sem(erroQ_list))

    coluna_erroQ = ft.Column(controls=[ft.Text("Estatísticas dos Erros Quadráticos")])
    text_erroQ_media = ft.TextField(label="Média", value=round(erroQ_mean, 4), read_only=True, width=container_width,
                                 height=container_height)
    text_erroQ_std = ft.TextField(label="Desvio padrão", value=round(erroQ_std, 4), read_only=True, width=container_width,
                               height=container_height)
    text_erroQ_min = ft.TextField(label="Menor erro", value=round(erroQ_min, 4), read_only=True, width=container_width,
                               height=container_height)
    linha_erroQ = ft.Row(controls=[text_erroQ_media, text_erroQ_std, text_erroQ_min], spacing=10)
    intervalo_erroQ_str = "(" + str(round(intervalo_erro[0], 4)) + " , " + str(round(intervalo_erro[1], 4)) + ")"
    text_intervalo_erroQ = ft.TextField(label="Intervalo de confiança", value=intervalo_erroQ_str, read_only=True,
                                     width=(2 * container_width + 10),
                                     height=container_height)
    coluna_erroQ.controls.append(linha_erroQ)
    coluna_erroQ.controls.append(text_intervalo_erroQ)

    principal.controls.append(coluna_erroQ)
    principal.controls.append(ft.Divider())

    # Estatísticas modelo menor erro
    qe_sim_min = __call_model(model, [q_min, k1_min, k2_min, outro_min], list_T, list_P, Tref)
    erros_list_min = []
    for i in range(len(qe_sim_min)):
        erros_list_min.append(abs(qe_sim_min[i] - list_q[i]))
    media_erros_min = np.mean(erros_list_min)
    std_erros_min = np.std(erros_list_min)
    max_erro_min = np.max(erros_list_min)
    min_erro_min = np.min(erros_list_min)
    intervalo_min = st.t.interval(0.95, len(erros_list_min) - 1, loc=np.mean(erros_list_min), scale=st.sem(erros_list_min))
    text_media_erros_min = ft.TextField(label="Média", value=round(media_erros_min, 4), read_only=True, width=container_width,
                                    height=container_height)
    text_std_erros_min = ft.TextField(label="Desvio padrão", value=round(std_erros_min, 4), read_only=True,
                                  width=container_width,
                                  height=container_height)

    text_erro_min_min = ft.TextField(label="Erro mínimo", value=round(min_erro_min, 4), read_only=True, width=container_width,
                                 height=container_height)
    text_erro_max_min = ft.TextField(label="Erro máximo", value=round(max_erro_min, 4), read_only=True, width=container_width,
                                 height=container_height)
    intervalo_str_min = "(" + str(round(intervalo_min[0], 4)) + " , " + str(round(intervalo_min[1], 4)) + ")"
    text_intervalo_min = ft.TextField(label="Intervalo de confiança", value=intervalo_str_min, read_only=True,
                                  width=(2 * container_width + 10),
                                  height=container_height)
    linha_est_erros1_min = ft.Row([text_media_erros_min, text_std_erros_min])
    linha_est_erros2_min = ft.Row([text_erro_min_min, text_erro_max_min])
    linha_est_erros3_min = ft.Row([text_intervalo_min])

    principal.controls.append(ft.Text("Estatística dos Resíduos - Parâmetros com Menor Erro"))
    principal.controls.append(linha_est_erros1_min)
    principal.controls.append(linha_est_erros2_min)
    principal.controls.append(linha_est_erros3_min)
    principal.controls.append(ft.Container(content=plots.__plot_sim_exp__(list_q, qe_sim_min), width=500))
    principal.controls.append(ft.Divider())

    # Estatísticas modelo média
    qe_sim = __call_model(model, [q_mean, k1_mean, k2_mean, outro_mean], list_T, list_P, Tref)
    erros_list = []
    for i in range(len(qe_sim)):
        erros_list.append(abs(qe_sim[i] - list_q[i]))
    media_erros = np.mean(erros_list)
    std_erros = np.std(erros_list, ddof=1)
    max_erro = np.max(erros_list)
    min_erro = np.min(erros_list)
    intervalo = st.t.interval(0.95, len(erros_list) - 1, loc=np.mean(erros_list), scale=st.sem(erros_list))
    text_media_erros = ft.TextField(label="Média", value=round(media_erros, 4), read_only=True, width=container_width,
                                    height=container_height)
    text_std_erros = ft.TextField(label="Desvio padrão", value=round(std_erros, 4), read_only=True,
                                  width=container_width,
                                  height=container_height)

    text_erro_min = ft.TextField(label="Erro mínimo", value=round(min_erro, 4), read_only=True, width=container_width,
                                 height=container_height)
    text_erro_max = ft.TextField(label="Erro máximo", value=round(max_erro, 4), read_only=True, width=container_width,
                                 height=container_height)
    intervalo_str = "(" + str(round(intervalo[0], 4)) + " , " + str(round(intervalo[1], 4)) + ")"
    text_intervalo = ft.TextField(label="Intervalo de confiança", value=intervalo_str, read_only=True,
                                  width=(2 * container_width + 10),
                                  height=container_height)
    linha_est_erros1 = ft.Row([text_media_erros, text_std_erros])
    linha_est_erros2 = ft.Row([text_erro_min, text_erro_max])
    linha_est_erros3 = ft.Row([text_intervalo])

    principal.controls.append(ft.Text("Estatística dos Resíduos - Média dos Parâmetros"))
    principal.controls.append(linha_est_erros1)
    principal.controls.append(linha_est_erros2)
    principal.controls.append(linha_est_erros3)
    principal.controls.append(ft.Container(content=plots.__plot_sim_exp__(list_q, qe_sim), width=500))
    principal.controls.append(ft.Divider())

    return principal


def __call_model(value, x, T, P, Tref):
    if value == 0:
        return __langmuir(x, T, P, Tref)
    elif value == 1:
        return __sips(x, T, P, Tref)
    elif value == 2:
        return __toth(x, T, P, Tref)
    elif value == 3:
        return __toth(x, T, P, Tref)


def __langmuir(x, T, P, Tref):
    qe_sim = []
    for i in range(len(P)):
        np.seterr(all='ignore')
        qe_sim.append((x[0] * x[1] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * P[i]) / (
                1 + x[1] * math.exp(x[2] * (1 / T[i] - 1 / Tref)) * P[i]))
    return qe_sim


def __sips(x, T, P, Tref):
    qe_sim = []
    for i in range(len(P)):
        np.seterr(all='ignore')
        qe_sim.append((x[0] * (math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * x[1] * P[i]) ** (1 / x[3])) / (
                1 + (math.exp(x[2] * (1 / T[i] - 1 / Tref)) * x[1] * P[i]) ** (1 / x[3])))
    return qe_sim


def __toth(x, T, P, Tref):
    qe_sim = []
    for i in range(len(P)):
        np.seterr(all='ignore')
        qe_sim.append((x[0] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref)))
                       * x[1] * P[i]) / (math.pow(1 + math.pow(math.exp(x[2] * (1 / T[i] - 1 / Tref))
                                                               * x[1] * P[i], (x[3])), (1 / x[3]))))
    return qe_sim

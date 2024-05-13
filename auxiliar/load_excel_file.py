import flet as ft
import pandas as pd
import xlsxwriter
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from io import BytesIO
from interface import resultado_est


def __seleciona_arquivo__(e: ft.FilePickerResultEvent):
    if e.files is not None:
        for f in e.files:
            arquivo = f.path
    excel = pd.read_excel(arquivo)

    vetorTempoT = []
    vetorT = []
    vetorTempoQ = []
    vetorQ = []
    vetorTempoy = []
    vetory = []

    for index, row in excel.iterrows():

        for col, value in row.items():
            if col == 'tempoT' and value >= 0:
                vetorTempoT.append(value)
            elif col == 'T' and value >= 0:
                vetorT.append(value)
            elif col == 'tempoQ' and value >= 0:
                vetorTempoQ.append(value)
            elif col == 'Q' and value >= 0:
                vetorQ.append(value)
            elif col == 'tempoy' and value >= 0:
                vetorTempoy.append(value)
            elif col == 'yCH4' and value >= 0:
                vetory.append(value)


def __export__(nome, sync_exp):
    if ".xlsx" in nome:
        workbook = xlsxwriter.Workbook(nome)
    else:
        workbook = xlsxwriter.Workbook(nome + '.xlsx')
    worksheet = workbook.add_worksheet()

    time_col = sync_exp.time_column.tolist()
    time_col.insert(0, "t")

    temperature_col = ["T"]
    for i in range(len(sync_exp.temperature_column)):
        temperature_col.append(sync_exp.temperature_column[i])

    flow_col = ["Q"]
    for i in range(len(sync_exp.flow_column)):
        flow_col.append(sync_exp.flow_column[i])

    y_col = ["y"]
    for i in range(len(sync_exp.y_column)):
        y_col.append(sync_exp.y_column[i])

    f_out_col = ["F"]
    for i in range(len(sync_exp.f_out_column)):
        f_out_col.append(sync_exp.f_out_column[i])

    row_export = [time_col, temperature_col, flow_col, y_col, f_out_col]
    row = 0
    for col, data in enumerate(row_export):
        worksheet.write_column(row, col, data)
    workbook.close()


def __result_export(nome, list_T, list_P, list_q, Tref, model, parameters, resultados):
    if ".xlsx" in nome:
        workbook = xlsxwriter.Workbook(nome)
    else:
        workbook = xlsxwriter.Workbook(nome + '.xlsx')

    erroQ_list = resultados
    min_error = min(erroQ_list)
    min_error_index = erroQ_list.index(min_error)
    # define listas
    qmax_list = parameters[0]
    # Estatística qmax
    q_mean = np.mean(qmax_list)
    q_std = np.std(qmax_list, ddof=1)
    q_min = qmax_list[min_error_index]
    intervalo_qmax = st.t.interval(0.95, len(qmax_list) - 1, loc=np.mean(qmax_list), scale=st.sem(qmax_list))
    qmax_list.insert(0, "qmax")

    k1_list = parameters[1]
    # Estatística K1
    k1_mean = np.mean(k1_list)
    k1_std = np.std(k1_list, ddof=1)
    k1_min = k1_list[min_error_index]
    intervalo_k1 = st.t.interval(0.95, len(k1_list) - 1, loc=np.mean(k1_list), scale=st.sem(k1_list))
    k1_list.insert(0, "K1")

    k2_list = parameters[2]
    # Estatística K2
    k2_mean = np.mean(k2_list)
    k2_std = np.std(k2_list, ddof=1)
    k2_min = k2_list[min_error_index]
    intervalo_k2 = st.t.interval(0.95, len(k2_list) - 1, loc=np.mean(k2_list), scale=st.sem(k2_list))
    k2_list.insert(0, "K2")

    outro_list = []
    if len(parameters) > 3:
        outro_list = parameters[3]

        outro_mean = np.mean(outro_list)
        outro_std = np.std(outro_list, ddof=1)
        outro_min = outro_list[min_error_index]
        intervalo_outro = st.t.interval(0.95, len(outro_list) - 1, loc=np.mean(outro_list),
                                        scale=st.sem(outro_list))
        if model == 1:
            outro_list.insert(0, "ns")
        elif model == 2:
            outro_list.insert(0, "n")
        elif model == 3:
            outro_list.insert(0, "α")

    erroQ_list.insert(0, "Erro quadrático")
    worksheet_listas = workbook.add_worksheet("Dados das Amostras")
    row_export = [qmax_list, k1_list, k2_list, erroQ_list]
    if len(outro_list) > 0:
        row_export.insert(3, outro_list)
    row = 0
    for col, data in enumerate(row_export):
        worksheet_listas.write_column(row, col, data, workbook.add_format({'align': 'center'}))
    worksheet_listas.set_column(0, 4, 30)

    worksheet_qmax = workbook.add_worksheet("Estat. qmax")
    q_intervalo_str = ("(" + str(round(intervalo_qmax[0], 6)).replace(".", ",")
                       + " , " + str(round(intervalo_qmax[1], 6)) + ")").replace(".", ",")
    row_exportq = [["Média", q_mean], ["Desvio Padrão", q_std], ["qmax - Menor Erro", q_min],
                   ["Intervalo de Confiança (95%)", q_intervalo_str]]
    row = 0
    for col, data in enumerate(row_exportq):
        worksheet_qmax.write_column(row, col, data, workbook.add_format({'align': 'center'}))
    worksheet_qmax.set_column(0, 4, 30)

    worksheet_k1 = workbook.add_worksheet("Estat. K1")
    k1_intervalo_str = ("(" + str(round(intervalo_k1[0], 6)).replace(".", ",")
                        + " , " + str(round(intervalo_k1[1], 6)).replace(".", ",") + ")")
    row_exportk1 = [["Média", k1_mean], ["Desvio Padrão", k1_std], ["K1 - Menor Erro", k1_min],
                    ["Intervalo de Confiança (95%)", k1_intervalo_str]]
    row = 0
    for col, data in enumerate(row_exportk1):
        worksheet_k1.write_column(row, col, data, workbook.add_format({'align': 'center'}))
    worksheet_k1.set_column(0, 4, 30)

    worksheet_k2 = workbook.add_worksheet("Estat. K2")
    k2_intervalo_str = ("(" + str(round(intervalo_k2[0], 6)).replace(".", ",")
                        + " , " + str(round(intervalo_k2[1], 6)).replace(".", ",") + ")")
    row_exportk2 = [["Média", k2_mean], ["Desvio Padrão", k2_std], ["K2 - Menor Erro", k2_min],
                    ["Intervalo de Confiança (95%)", k2_intervalo_str]]
    row = 0
    for col, data in enumerate(row_exportk2):
        worksheet_k2.write_column(row, col, data, workbook.add_format({'align': 'center'}))
    worksheet_k2.set_column(0, 4, 30)
    outro_str = ""
    if model > 0:
        if model == 1:
            worksheet_outro = workbook.add_worksheet("Estat. ns")
            outro_str = "ns"
        elif model == 2:
            worksheet_outro = workbook.add_worksheet("Estat. n")
            outro_str = "n"
        elif model == 3:
            worksheet_outro = workbook.add_worksheet("Estat. α")
            outro_str = "α"
        outro_intervalo_str = ("(" + str(round(intervalo_outro[0], 6)).replace(".", ",") + " , " +
                               str(round(intervalo_outro[1], 6)).replace(".", ",") + ")")
        row_exportoutro = [["Média", k1_mean], ["Desvio Padrão", outro_std], [outro_str + " - Menor Erro", outro_min],
                           ["Intervalo de Confiança (95%)", outro_intervalo_str]]
        row = 0
        for col, data in enumerate(row_exportoutro):
            worksheet_outro.write_column(row, col, data, workbook.add_format({'align': 'center'}))
        worksheet_outro.set_column(0, 4, 30)

    qe_sim = resultado_est.__call_model(model, [q_mean, k1_mean, k2_mean, outro_mean], list_T, list_P, Tref)
    correlation = np.corrcoef(list_q, qe_sim)[0, 1]
    r2 = correlation ** 2
    plt.plot(list_q, qe_sim, 'ro', label='Dados Sincronizados')
    plt.xlabel("q Experimental (mol/kg)")
    plt.ylabel("q Simulado (mol/kg)")
    plt.title("Experimental vs Simulado")
    max_value1 = max(list_q)
    max_value2 = max(qe_sim)
    max_value = max(max_value1, max_value2)
    plt.plot([0, max_value], [0, max_value], 'k-')
    plt.text(max_value * 0.05, max_value * 0.9, "r$^2$ = " + str(round(r2, 4)))
    erro_abs = []
    for i in range(len(list_q)):
        erro_abs.append(abs(list_q[i] - qe_sim[i]))

    media_erro = np.mean(erro_abs)
    std_erro = np.std(erro_abs, ddof=1)
    intervalo_erro = st.t.interval(0.95, len(erro_abs) - 1, loc=np.mean(erro_abs), scale=st.sem(erro_abs))
    erro_intervalo_str = ("(" + str(round(intervalo_erro[0], 6)).replace(".", ",") + " , " +
                          str(round(intervalo_erro[1], 6)).replace(".", ",") + ")")
    estatisticas = ["Média erros absolutos", media_erro, "Desvio padrão", std_erro, "Intervalo de Confiança",
                    erro_intervalo_str]
    imgdata = BytesIO()
    plt.savefig(imgdata, format="png")
    imgdata.seek(0)
    qe_sim.insert(0, "q Sim.")
    list_q.insert(0, "q Exp.")
    list_T.insert(0, "Temperatura")
    list_P.insert(0, "Pressão")

    simulacao_media = [list_T, list_P, list_q, qe_sim, estatisticas]
    worksheet_image = workbook.add_worksheet("Gráfico - Média")
    row = 0
    for col, data in enumerate(simulacao_media):
        worksheet_image.write_column(row, col, data, workbook.add_format({'align': 'center'}))
    worksheet_image.insert_image(
        0, 7, "",
        {'image_data': imgdata}
    )
    worksheet_image.set_column(0, 4, 25)
    plt.close()

    list_q.remove("q Exp.")
    list_T.remove("Temperatura")
    list_P.remove("Pressão")
    qe_sim_min = resultado_est.__call_model(model, [q_min, k1_min, k2_min, outro_min], list_T, list_P, Tref)
    correlation_min = np.corrcoef(list_q, qe_sim_min)[0, 1]
    r2_min = correlation_min ** 2
    plt.plot(list_q, qe_sim_min, 'ro', label='Dados Sincronizados')
    plt.xlabel("q Experimental (mol/kg)")
    plt.ylabel("q Simulado (mol/kg)")
    plt.title("Experimental vs Simulado")
    max_value1_min = max(list_q)
    max_value2_min = max(qe_sim_min)
    max_value_min = max(max_value1_min, max_value2_min)
    plt.plot([0, max_value_min], [0, max_value_min], 'k-')
    plt.text(max_value_min * 0.05, max_value_min * 0.9, "r$^2$ = " + str(round(r2_min, 4)))
    erro_abs_min = []
    for i in range(len(list_q)):
        erro_abs_min.append(abs(list_q[i] - qe_sim_min[i]))

    media_erro_min = np.mean(erro_abs_min)
    std_erro_min = np.std(erro_abs_min, ddof=1)
    intervalo_erro_min = st.t.interval(0.95, len(erro_abs_min) - 1, loc=np.mean(erro_abs_min),
                                       scale=st.sem(erro_abs_min))
    erro_intervalo_str_min = ("(" + str(round(intervalo_erro_min[0], 6)).replace(".", ",") + " , " +
                              str(round(intervalo_erro_min[1], 6)).replace(".", ",") + ")")
    estatisticas_min = ["Média erros absolutos", media_erro_min, "Desvio padrão", std_erro_min,
                        "Intervalo de Confiança",
                        erro_intervalo_str_min]
    imgdata_min = BytesIO()
    plt.savefig(imgdata_min, format="png")
    imgdata_min.seek(0)
    qe_sim_min.insert(0, "q Simulado")
    list_q.insert(0, "q Experimental")
    list_T.insert(0, "Temperatura")
    list_P.insert(0, "Pressão")
    simulacao_min = [list_T, list_P, list_q, qe_sim_min, estatisticas_min]
    worksheet_image_min = workbook.add_worksheet("Gráfico - Mínimo")
    row = 0
    for col, data in enumerate(simulacao_min):
        worksheet_image_min.write_column(row, col, data, workbook.add_format({'align': 'center'}))
    worksheet_image_min.insert_image(
        0, 5, "",
        {'image_data': imgdata_min}
    )
    worksheet_image_min.set_column(0, 4, 25)
    plt.close()
    list_q.remove("q Experimental")
    list_T.remove("Temperatura")
    list_P.remove("Pressão")
    workbook.close()


def __single_result_export(nome, list_T, list_P, list_q, Tref, model, parameters, erroQ):
    if ".xlsx" in nome:
        workbook = xlsxwriter.Workbook(nome)
    else:
        workbook = xlsxwriter.Workbook(nome + '.xlsx')
    qe_sim = resultado_est.__call_model(model, [parameters[0], parameters[1], parameters[2], parameters[3]], list_T,
                                        list_P, Tref)
    correlation = np.corrcoef(list_q, qe_sim)[0, 1]
    r2 = correlation ** 2
    plt.plot(list_q, qe_sim, 'ro')
    plt.xlabel("q Experimental (mol/kg)")
    plt.ylabel("q Simulado (mol/kg)")
    plt.title("Experimental vs Simulado")
    max_value1 = max(list_q)
    max_value2 = max(qe_sim)
    max_value = max(max_value1, max_value2)
    plt.plot([0, max_value], [0, max_value], 'k-')
    plt.text(max_value * 0.05, max_value * 0.9, "r$^2$ = " + str(round(r2, 4)))
    erro_abs = []
    for i in range(len(list_q)):
        erro_abs.append(abs(list_q[i] - qe_sim[i]))

    media_erro = np.mean(erro_abs)
    std_erro = np.std(erro_abs, ddof=1)
    intervalo_erro = st.t.interval(0.95, len(erro_abs) - 1, loc=np.mean(erro_abs),
                                   scale=st.sem(erro_abs))
    erro_intervalo_str_min = ("(" + str(round(intervalo_erro[0], 6)).replace(".", ",") + " , " +
                              str(round(intervalo_erro[1], 6)).replace(".", ",") + ")")
    estatisticas = ["qmax", parameters[0], "K1", parameters[1], "K2", parameters[2], "Média erros absolutos",
                    media_erro, "Desvio padrão", std_erro, "Intervalo de Confiança", erro_intervalo_str_min]
    if model == 1:
        estatisticas.insert(6, "ns")
        estatisticas.insert(7, parameters[3])
    if model == 2:
        estatisticas.insert(6, "n")
        estatisticas.insert(7, parameters[3])
    if model == 3:
        estatisticas.insert(6, "α")
        estatisticas.insert(7, parameters[3])

    imgdata = BytesIO()
    plt.savefig(imgdata, format="png")
    imgdata.seek(0)
    qe_sim.insert(0, "q Simulado")
    list_q.insert(0, "q Experimental")
    list_T.insert(0, "Temperatura")
    list_P.insert(0, "Pressão")
    simulacao = [list_T, list_P, list_q, qe_sim, estatisticas]
    worksheet_image_min = workbook.add_worksheet("Dados da Estimação")
    row = 0
    for col, data in enumerate(simulacao):
        worksheet_image_min.write_column(row, col, data, workbook.add_format({'align': 'center'}))
    worksheet_image_min.insert_image(
        0, 5, "",
        {'image_data': imgdata}
    )
    worksheet_image_min.set_column(0, 4, 25)
    plt.close()
    list_q.remove("q Experimental")
    list_T.remove("Temperatura")
    list_P.remove("Pressão")
    workbook.close()

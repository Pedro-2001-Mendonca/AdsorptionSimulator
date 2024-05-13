import flet as ft
from flet_core.matplotlib_chart import MatplotlibChart
from db import db_experiment as db
import matplotlib.pyplot as plt

sync_exp_list = []




def main(linha_principal, page):
    def seleciona_arquivo(e: ft.FilePickerResultEvent):
        if e.files != None:
            for f in e.files:
                db_name = f.path
                sync_exp_list.append(db.__load_db_experiment__(db_name))
            __update_page()

    seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)
    principal = ft.Column(alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, spacing=25)

    fp = ft.ElevatedButton("Carregar Experimento", on_click=lambda _: seleciona_arquivo_dialog.pick_files(
        allowed_extensions=["exp"]), width=200)

    principal.controls.insert(0, fp)
    linha_principal.controls.append(principal)
    page.overlay.append(seleciona_arquivo_dialog)
    linha_principal.update()
    page.update()



def __update_page():
    def seleciona_arquivo(e: ft.FilePickerResultEvent):
        if e.files != None:
            for f in e.files:
                db_name = f.path
                sync_exp_list.append(db.__load_db_experiment__(db_name))
            __update_page()

    seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)
    principal = ft.Column(alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, spacing=25)

    while len(principal.controls) > 1:
        principal.controls.remove(principal.controls[1])
    vetorCol = ft.Column(controls=None)
    vetorCol.controls.clear()
    newheigth = 35
    vetorLinha = [ft.TextField("Tempo (s)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1,
                               content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("Temperatura (K)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("Vazão (L/s)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("Fração Molar", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True)]
    vetorCol.controls.insert(0, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

    for i in range(len(sync_exp_list[0].time_column)):
        vetorLinha = [
            ft.TextField(round(sync_exp_list[0].time_column[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(sync_exp_list[0].temperature_column[i], 5), text_align=ft.TextAlign.CENTER,
                         width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(sync_exp_list[0].flow_column[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(sync_exp_list[0].y_column[i], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2))]
        vetorCol.controls.insert(i + 1, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))
    q = sync_exp_list[0].q

    figura11 = plt.plot(sync_exp_list[0].time_column, sync_exp_list[0].temperature_column, 'r-o',
                        label='Dados Sincronizados')
    plt.xlabel("tempo (min)")
    plt.ylabel("temperatura (K)")
    plt.title("Temperatura")
    plt.legend(loc="lower right")
    plt.close()

    figura22 = plt.plot(sync_exp_list[0].time_column, sync_exp_list[0].flow_column, 'b-o',
                        label='Dados Sincronizados')
    plt.xlabel("tempo (s)")
    plt.ylabel("vazão (L/s)")
    plt.title('Vazão')
    plt.legend(loc="lower right")
    plt.close()

    figura33 = plt.plot(sync_exp_list[0].time_column, sync_exp_list[0].y_column, 'k-o', label='Dados Sincronizados')
    plt.xlabel("tempo (min)")
    plt.ylabel("fração molar")
    plt.title("Fração Molar")
    plt.close()

    grafico11 = MatplotlibChart(figura11[0].figure)
    grafico22 = MatplotlibChart(figura22[0].figure)
    grafico33 = MatplotlibChart(figura33[0].figure)

    row_figure1 = ft.Row([grafico11])
    fig_container1 = ft.Container(content=row_figure1, width=1000, height=400, )

    row_figure2 = ft.Row([grafico22])
    fig_container2 = ft.Container(content=row_figure2, width=1000, height=400)

    row_figure3 = ft.Row([grafico33])
    fig_container3 = ft.Container(content=row_figure3, width=1000, height=400)

    fig_column = ft.Column(controls=[fig_container1, fig_container2, fig_container3], spacing=0)

    text_q = ft.Container(
        content=ft.TextField(label="Quantidade Adsorvida (q)", value=round(q, 8), read_only=True,
                             suffix_text="mol/kg", width=200))

    principal.controls.insert(3, vetorCol)
    principal.controls.insert(4, text_q)
    principal.controls.insert(5, fig_column)
    principal.update()

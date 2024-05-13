import flet as ft
from flet_core.matplotlib_chart import MatplotlibChart
from db import db_experiment as db
import matplotlib.pyplot as plt

sync_exp_list = []




def main(page, off_sync):
    if off_sync:
        off_sync = False
        def seleciona_arquivo(e: ft.FilePickerResultEvent):
            sync_exp_list.clear()
            if e.files:
                for f in e.files:
                    db_name = f.path
                    sync_exp_list.append(db.__load_db_pack_experiment__(db_name))
                __update_page__(principal)

        seleciona_arquivo_dialog = ft.FilePicker(on_result=seleciona_arquivo)
        principal = ft.Column(alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.ALWAYS, spacing=25)
        fp = ft.ElevatedButton("Carregar Experimentos", on_click=lambda _: seleciona_arquivo_dialog.pick_files(
            allowed_extensions=["exp"],allow_multiple=True), width=200)

        principal.controls.insert(0, fp)
        page.overlay.append(seleciona_arquivo_dialog)
        off_sync = True
        return principal



def __update_page__(principal):

    while len(principal.controls) > 1:
        principal.controls.remove(principal.controls[1])
    new_list = sorted(sync_exp_list, key=lambda x: x[0])
    vetorCol = ft.Column(controls=None)
    vetorCol.controls.clear()
    newheigth = 35
    vetorLinha = [ft.TextField("Temperatura (K)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1,
                               content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("Pressão (bar)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True),
                  ft.TextField("q (mol/kg)", text_align=ft.TextAlign.CENTER, width=150,
                               height=newheigth,
                               text_vertical_align=-1, content_padding=ft.padding.only(left=5, right=2, bottom=18),
                               border=ft.InputBorder.NONE, read_only=True)]

    vetorCol.controls.insert(0, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

    list_T = []
    list_P = []
    list_q = []
    for i in range(len(new_list)):
        vetorLinha = [
            ft.TextField(round(new_list[i][0], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(new_list[i][1], 5), text_align=ft.TextAlign.CENTER,
                         width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2)),
            ft.TextField(round(new_list[i][2], 5), text_align=ft.TextAlign.CENTER, width=150,
                         height=newheigth,
                         text_vertical_align=-0.73, content_padding=ft.padding.only(left=5, right=2))]
        list_T.insert(i, new_list[i][0])
        list_P.insert(i, new_list[i][1])
        list_q.insert(i, new_list[i][2])

        vetorCol.controls.insert(i + 1, ft.Row(vetorLinha, alignment=ft.MainAxisAlignment.START))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(list_T, list_P, list_q, c=list_q, marker="o", cmap="seismic")

    ax.set_xlabel('T (K)')
    ax.set_ylabel('P (bar)')
    ax.set_zlabel('q (mol/kg)')

    grafico = MatplotlibChart(fig.figure)
    row_figure = ft.Row([grafico])
    fig_container = ft.Container(content=row_figure, width=1000, height=400, )

    principal.controls.insert(3, vetorCol)
    principal.controls.insert(4, fig_container)
    plt.close()
    principal.update()

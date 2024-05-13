import flet as ft
from interface import pe_body as pb

input_height = 50
input_cursor_height = 25
input_width = 250
button_width = 200

sync_exp_list = []

list_T = []
list_P = []
list_q = []

input_n_iter = ft.TextField(label="Número de iterações", height=input_height,
                            cursor_height=input_cursor_height, width=input_width, value="100")
input_n_particulas = ft.TextField(label="Número de partículas", height=input_height,
                                  cursor_height=input_cursor_height, width=input_width, value="100")
input_Tref = ft.TextField(label="Tref", height=input_height, suffix_text="K",
                          cursor_height=input_cursor_height, width=input_width, value="100")
input_Tref.value = 273.15
input_qmax_min = ft.TextField(label="Valor mínimo de qmax", height=input_height,
                              cursor_height=input_cursor_height, width=input_width)
input_qmax_min.value = 0
input_qmax_max = ft.TextField(label="Valor máximo de qmax", height=input_height,
                              cursor_height=input_cursor_height, width=input_width)
input_qmax_max.value = 50
input_k1_min = ft.TextField(label="Valor mínimo de K1", height=input_height,
                            cursor_height=input_cursor_height, width=input_width)
input_k1_min.value = 0
input_k1_max = ft.TextField(label="Valor máximo de K1", height=input_height,
                            cursor_height=input_cursor_height, width=input_width)
input_k1_max.value = 10
input_k2_min = ft.TextField(label="Valor mínimo de K2", height=input_height,
                            cursor_height=input_cursor_height, width=input_width)
input_k2_min.value = 0
input_k2_max = ft.TextField(label="Valor máximo de K2", height=input_height,
                            cursor_height=input_cursor_height, width=input_width)
input_k2_max.value = 1000
input_alpha_min = ft.TextField(label="Valor mínimo de  α", height=input_height,
                               cursor_height=input_cursor_height, width=input_width)
input_alpha_min.value = 0
input_alpha_max = ft.TextField(label="Valor máximo de  α", height=input_height,
                               cursor_height=input_cursor_height, width=input_width)
input_alpha_max.value = 10
input_n_min = ft.TextField(label="Valor mínimo de n", height=input_height,
                           cursor_height=input_cursor_height, width=input_width)
input_n_min.value = 0.1
input_n_max = ft.TextField(label="Valor máximo de n", height=input_height,
                           cursor_height=input_cursor_height, width=input_width)
input_n_max.value = 10
input_ns_min = ft.TextField(label="Valor mínimo de ns", height=input_height,
                            cursor_height=input_cursor_height, width=input_width)
input_ns_min.value = 0.1
input_ns_max = ft.TextField(label="Valor máximo de ns", height=input_height,
                            cursor_height=input_cursor_height, width=input_width)
input_ns_max.value = 10


def __onchange(coluna, row, page):
    def checkbox_changed(e):
        cbox.update()
        if cbox.value:
            input_amostra.visible = True
            input_amostra.update()
        else:
            input_amostra.visible = False
            input_amostra.update()

    cbox = ft.Checkbox(label="Gerar estatísticas dos parâmetros", on_change=checkbox_changed)
    input_amostra = ft.TextField(label="Número de amostras", height=input_height,
                                 cursor_height=input_cursor_height, width=input_width, visible=False)
    input_amostra.value = 4
    contador = ft.Text("Repetições executadas: 0", visible=False)

    def cria_linha(index):
        linha1 = ft.Row(controls=[
            input_n_iter,
            input_n_particulas,
            input_Tref
        ])
        linha2 = ft.Row(controls=[
            input_qmax_min,
            input_qmax_max,
            cbox
        ])
        linha3 = ft.Row(controls=[
            input_k1_min,
            input_k1_max,
            input_amostra
        ])
        linha4 = ft.Row(controls=[
            input_k2_min,
            input_k2_max,
            contador
        ])
        coluna1 = ft.Column(controls=[
            ft.Divider(),
            linha1,
            ft.Divider(),
            linha2,
            linha3,
            linha4
        ], spacing=15)

        if index == 0:
            pass
        elif index == 1:
            coluna1.controls.append(
                ft.Row(controls=[
                    input_ns_min,
                    input_ns_max
                ])
            )
        elif index == 2:
            coluna1.controls.append(
                ft.Row(controls=[
                    input_n_min,
                    input_n_max
                ])
            )
        elif index == 3:
            coluna1.controls.append(
                ft.Row(controls=[
                    input_alpha_min,
                    input_alpha_max
                ])
            )

        return coluna1

    if str(row.controls[0].value) == "Langmuir":
        row.controls[1].content.src = f"../images/langmuir.svg"
        row.controls[1].width = 400
        if len(coluna.controls) > 1:
            coluna.controls.remove(coluna.controls[1])
        coluna.controls.insert(1, cria_linha(0))
        parameters = [input_qmax_min.value, input_qmax_max.value, input_k1_min.value, input_k1_max.value,
                      input_k2_min.value, input_k2_max.value]
        pb.main(coluna, page, list_T, list_P, list_q, 0, input_n_particulas, input_n_iter, parameters,
                float(input_Tref.value), cbox, input_amostra, contador)
        page.update()
    elif str(row.controls[0].value) == "Sips":
        row.controls[1].content.src = f"../images/sips.svg"
        row.controls[1].width = 450
        if len(coluna.controls) > 1:
            coluna.controls.remove(coluna.controls[1])
        coluna.controls.insert(1, cria_linha(1))
        parameters = [input_qmax_min.value, input_qmax_max.value, input_k1_min.value, input_k1_max.value,
                      input_k2_min.value, input_k2_max.value, input_ns_min.value, input_ns_max.value]
        pb.main(coluna, page, list_T, list_P, list_q, 1, input_n_particulas, input_n_iter, parameters,
                float(input_Tref.value), cbox, input_amostra, contador)
        page.update()
    elif str(row.controls[0].value) == "Toth":
        row.controls[1].content.src = f"../images/toth.svg"
        row.controls[1].width = 450
        if len(coluna.controls) > 1:
            coluna.controls.remove(coluna.controls[1])
        coluna.controls.insert(1, cria_linha(2))
        parameters = [input_qmax_min.value, input_qmax_max.value, input_k1_min.value, input_k1_max.value,
                      input_k2_min.value, input_k2_max.value, input_n_min.value, input_n_max.value]
        pb.main(coluna, page, list_T, list_P, list_q, 2, input_n_particulas, input_n_iter, parameters,
                float(input_Tref.value), cbox, input_amostra, contador)
        page.update()
    elif str(row.controls[0].value) == "Langmuir Multissítios":
        row.controls[1].content.src = f"../images/multissitios.svg"
        row.controls[1].width = 500
        coluna.controls.insert(1, cria_linha(3))
        parameters = [input_qmax_min.value, input_qmax_max.value, input_k1_min.value, input_k1_max.value,
                      input_k2_min.value, input_k2_max.value, input_alpha_min.value, input_alpha_max.value]
        pb.main(coluna, page, list_T, list_P, list_q, 3, input_n_particulas, input_n_iter, parameters,
                float(input_Tref.value), cbox, input_amostra, contador)
        page.update()
    row.controls[1].content.visible = True
    coluna.update()


def main(page, off_sync):
    if off_sync:
        off_sync = False
        principal = ft.Column(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, spacing=25)

        row = ft.Row(controls=[
            ft.Dropdown(
                width=250,
                options=[
                    ft.dropdown.Option("Langmuir"),
                    ft.dropdown.Option("Sips"),
                    ft.dropdown.Option("Toth"),
                    ft.dropdown.Option("Langmuir Multissítios"),
                ],
                on_change=lambda _: __onchange(principal, row, page),
                hint_text="Selecione um modelo"
            ),
            ft.Container(content=ft.Image(visible=False, width=100, height=70, fit=ft.ImageFit.CONTAIN, ),
                         margin=ft.margin.only(left=50)),
            ft.Container(width=20),

        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=25)
        principal.controls.insert(0, row)
        off_sync = True

        return principal

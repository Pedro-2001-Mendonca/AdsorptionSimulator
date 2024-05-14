import flet as ft
import math

input_height = 50
input_cursor_height = 25
input_width = 150
button_width = 200

sync_exp_list = []

list_T = []
list_P = []
list_q = []

qmax_comp1 = ft.TextField(label="qmax - comp. 1", height=input_height,
                          cursor_height=input_cursor_height, width=input_width, value="6.36350")
k1_comp1 = ft.TextField(label="K1 - comp. 1", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="0.17055")
k2_comp1 = ft.TextField(label="K2 - comp. 1", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="2105.53373")
ns_comp1 = ft.TextField(label="ns - comp. 1", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="1.062845")
n_comp1 = ft.TextField(label="n - comp. 1", height=input_height,
                       cursor_height=input_cursor_height, width=input_width, value="1")
alpha_comp1 = ft.TextField(label="α - comp. 1", height=input_height,
                           cursor_height=input_cursor_height, width=input_width, value="1")
linha_comp1 = ft.Row([qmax_comp1, k1_comp1, ns_comp1, alpha_comp1])

qmax_comp2 = ft.TextField(label="qmax - comp. 2", height=input_height,
                          cursor_height=input_cursor_height, width=input_width, value="8.63780")
k1_comp2 = ft.TextField(label="K1 - comp. 2", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="15.17096")
k2_comp2 = ft.TextField(label="K2 - comp. 2", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="7475.38068")
ns_comp2 = ft.TextField(label="ns - comp. 2", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="2.35889")
n_comp2 = ft.TextField(label="n - comp. 2", height=input_height,
                       cursor_height=input_cursor_height, width=input_width, value="1")
alpha_comp2 = ft.TextField(label="α - comp. 2", height=input_height,
                           cursor_height=input_cursor_height, width=input_width, value="1")
linha_comp2 = ft.Row([qmax_comp2, k1_comp2, ns_comp2, alpha_comp2])

qmax_comp3 = ft.TextField(label="qmax - comp. 3", height=input_height,
                          cursor_height=input_cursor_height, width=input_width, value="1")
k1_comp3 = ft.TextField(label="K1 - comp. 3", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="1")
k2_comp3 = ft.TextField(label="K2 - comp. 3", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="1")
ns_comp3 = ft.TextField(label="ns - comp. 3", height=input_height,
                        cursor_height=input_cursor_height, width=input_width, value="1")
n_comp3 = ft.TextField(label="n - comp. 3", height=input_height,
                       cursor_height=input_cursor_height, width=input_width, value="1")
alpha_comp3 = ft.TextField(label="α - comp. 3", height=input_height,
                           cursor_height=input_cursor_height, width=input_width, value="1")
linha_comp3 = ft.Row([qmax_comp3, k1_comp3, ns_comp3, alpha_comp3])

inlet_temp = ft.TextField(label="Temperatura", height=input_height,
                          cursor_height=input_cursor_height, width=input_width, value="298.15")
inlet_pres = ft.TextField(label="Pressão", height=input_height,
                          cursor_height=input_cursor_height, width=input_width, value="1")

qmax_comp1.value = 7.01816
k1_comp1.value = 0.193684
k2_comp1.value = 2110.02
n_comp1.value = 0.81529
qmax_comp2.value = 10.1845
k1_comp2.value = 3046.335
k2_comp2.value = 7491.086
n_comp2.value = 0.261344

def __onchange(coluna, row0, row):
    coluna.controls[2].visible = True
    while len(coluna.controls) > 3:
        coluna.controls.remove(coluna.controls[3])
    linhas = []
    linhas.clear()

    def cria_linha():

        if str(row0.controls[0].value) == "Langmuir":
            linha_comp1 = ft.Row([qmax_comp1, k1_comp1, k2_comp1])
            linha_comp2 = ft.Row([qmax_comp2, k1_comp2, k2_comp2])
            linha_comp3 = ft.Row([qmax_comp3, k1_comp3, k2_comp3])
            linhas.append(linha_comp1)
            linhas.append(linha_comp2)
            linhas.append(linha_comp3)
        elif str(row0.controls[0].value) == "Sips":
            linha_comp1 = ft.Row([qmax_comp1, k1_comp1, k2_comp1, ns_comp1])
            linha_comp2 = ft.Row([qmax_comp2, k1_comp2, k2_comp2, ns_comp2])
            linha_comp3 = ft.Row([qmax_comp3, k1_comp3, k2_comp3, ns_comp3])
            linhas.append(linha_comp1)
            linhas.append(linha_comp2)
            linhas.append(linha_comp3)
        elif str(row0.controls[0].value) == "Toth":
            linha_comp1 = ft.Row([qmax_comp1, k1_comp1, k2_comp1, n_comp1])
            linha_comp2 = ft.Row([qmax_comp2, k1_comp2, k2_comp2, n_comp2])
            linha_comp3 = ft.Row([qmax_comp3, k1_comp3, k2_comp3, n_comp3])
            linhas.append(linha_comp1)
            linhas.append(linha_comp2)
            linhas.append(linha_comp3)
        elif str(row0.controls[0].value) == "Langmuir Multissítios":
            linha_comp1 = ft.Row([qmax_comp1, k1_comp1, k2_comp1, alpha_comp1])
            linha_comp2 = ft.Row([qmax_comp2, k1_comp2, k2_comp2, alpha_comp2])
            linha_comp3 = ft.Row([qmax_comp3, k1_comp3, k2_comp3, alpha_comp3])
            linhas.append(linha_comp1)
            linhas.append(linha_comp2)
            linhas.append(linha_comp3)
        else:
            return

    def cria_linhas(index):

        cria_linha()
        coluna1 = ft.Column(controls=[
            ft.Divider(),
            ft.Text("Componente 1"),
            linhas[0],
            ft.Divider(),
        ], spacing=15)

        if index == 0:
            pass

        elif index == 1:
            coluna1.controls.append(ft.Text("Componente 2"))
            coluna1.controls.append(linhas[1])
            coluna1.controls.append(ft.Divider())

        elif index == 2:
            coluna1.controls.append(ft.Text("Componente 2"))
            coluna1.controls.append(linhas[1])
            coluna1.controls.append(ft.Divider())

            coluna1.controls.append(ft.Text("Componente 3"))
            coluna1.controls.append(linhas[2])
            coluna1.controls.append(ft.Divider())

        return coluna1

    if str(row.controls[0].value) == "Monocomponente":
        coluna.controls.insert(3, cria_linhas(0))
    elif str(row.controls[0].value) == "Binário":
        coluna.controls.insert(3, cria_linhas(1))
    elif str(row.controls[0].value) == "Ternário":
        coluna.controls.insert(3, cria_linhas(2))
    coluna.update()


def __modelo_on_change__(coluna, row0, row):
    if row.visible:
        coluna.update()
        __onchange(coluna, row0, row)
    else:
        row.visible = True
        coluna.update()
    return


def main(page, off_sync):
    if off_sync:
        off_sync = False
        principal = ft.Column(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.START, spacing=25)

        row0 = ft.Row(controls=[
            ft.Dropdown(
                width=250,
                options=[
                    ft.dropdown.Option("Langmuir"),
                    ft.dropdown.Option("Sips"),
                    ft.dropdown.Option("Toth"),
                    ft.dropdown.Option("Langmuir Multissítios"),
                ],
                on_change=lambda _: __modelo_on_change__(principal, row0, row),
                hint_text="Selecione um modelo"
            ),
            ft.Container(content=ft.Image(visible=False, width=100, height=70, fit=ft.ImageFit.CONTAIN, ),
                         margin=ft.margin.only(left=50)),
            ft.Container(width=20),

        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10)

        row = ft.Row(controls=[
            ft.Dropdown(
                width=250,
                options=[
                    ft.dropdown.Option("Monocomponente"),
                    ft.dropdown.Option("Binário"),
                    ft.dropdown.Option("Ternário"),
                ],
                on_change=lambda _: __onchange(principal, row0, row),
                hint_text="Selecione um Sistema"
            ),
            ft.Container(width=20),

        ], alignment=ft.MainAxisAlignment.START, spacing=25, visible=False)
        row_tp = ft.Row(controls=[
            inlet_temp,
            inlet_pres,
            ft.ElevatedButton(text="Calcular q", on_click=lambda _: __btn_calcular__(principal, row0, row), width=150)
        ], visible=False,
            spacing=20)
        principal.controls.insert(0, row0)
        principal.controls.insert(1, row)
        principal.controls.insert(2, row_tp)
        off_sync = True

        return principal


def __btn_calcular__(principal, row0, row):
    Gascte = 0.08314462
    temp_ref = 273.15
    while len(principal.controls[2].controls) > 3:
        principal.controls[2].remove(principal.controls[3])
    resultado = []



    if str(row0.controls[0].value) == "Langmuir":

        if str(row.controls[0].value) == "Monocomponente":
            beq1 = float(k1_comp1.value) * math.exp(float(k2_comp1.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            resultado.append(float(qmax_comp1.value) * beq1 * float(inlet_pres.value) /
                             (1 + beq1 * float(inlet_pres.value)))
        if str(row.controls[0].value) == "Binário":
            partial_pressure = float(inlet_pres.value) / 2
            beq1 = float(k1_comp1.value) * math.exp(float(k2_comp1.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            beq2 = float(k1_comp2.value) * math.exp(float(k2_comp2.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            resultado.append(float(qmax_comp1.value) * beq1 * partial_pressure /
                             (1 + beq1 * partial_pressure + beq2 * partial_pressure))
        if str(row.controls[0].value) == "Ternário":
            partial_pressure = float(inlet_pres.value) / 3
            beq1 = float(k1_comp1.value) * math.exp(float(k2_comp1.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            beq2 = float(k1_comp2.value) * math.exp(float(k2_comp2.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            beq3 = float(k1_comp3.value) * math.exp(float(k2_comp3.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            resultado.append(float(qmax_comp1.value) * beq1 * partial_pressure /
                             (1 + beq1 * partial_pressure + beq2 * partial_pressure + beq3 * partial_pressure))

    if str(row0.controls[0].value) == "Sips":

        if str(row.controls[0].value) == "Monocomponente":
            beq1 = float(k1_comp1.value) * math.exp(float(k2_comp1.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            upper1 = (beq1 * float(inlet_pres.value)*0.6) ** (1/float(ns_comp1.value))
            under1 = (beq1 * float(inlet_pres.value)*0.6) ** (1/float(ns_comp1.value))
            resultado.append(float(qmax_comp1.value) * upper1 / (1 + under1))
        if str(row.controls[0].value) == "Binário":
            partial_pressure = float(inlet_pres.value)
            beq1 = float(k1_comp1.value) * math.exp(float(k2_comp1.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            beq2 = float(k1_comp2.value) * math.exp(float(k2_comp2.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            valor1 = (beq1 * partial_pressure*0.6) ** (1/float(ns_comp1.value))
            valor2 = (beq2 * partial_pressure*0.4) ** (1/float(ns_comp2.value))
            resultado.append(float(qmax_comp1.value) * valor1 / (1 + valor1 + valor2))
            resultado.append(float(qmax_comp2.value) * valor2 / (1 + valor1 + valor2))

        if str(row.controls[0].value) == "Ternário":
            resultado = []

    if str(row0.controls[0].value) == "Toth":



        if str(row.controls[0].value) == "Monocomponente":
            beq1 = float(k1_comp1.value) * math.exp(float(k2_comp1.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            upper1 = (beq1 * float(inlet_pres.value) * 0.6) ** (1 / float(ns_comp1.value))
            under1 = (beq1 * float(inlet_pres.value) * 0.6) ** (1 / float(ns_comp1.value))
            resultado.append(float(qmax_comp1.value) * upper1 / (1 + under1))

        if str(row.controls[0].value) == "Binário":
            partial_pressure1 = float(inlet_pres.value) * 0.6
            partial_pressure2 = float(inlet_pres.value) * 0.4
            beq1 = float(k1_comp1.value) * math.exp(float(k2_comp1.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            beq2 = float(k1_comp2.value) * math.exp(float(k2_comp2.value) *
                                                    (1 / float(inlet_temp.value) - 1 / float(temp_ref)))
            upper1 = beq1 * partial_pressure1
            upper2 = beq2 * partial_pressure2
            valor1 = (beq1 * partial_pressure1) ** (float(n_comp1.value))
            valor2 = (beq2 * partial_pressure2) ** (float(n_comp2.value))
            resultado.append(float(qmax_comp1.value) * upper1 / ((1 + valor1 + valor2) ** (1 / float(n_comp1.value))))
            resultado.append(float(qmax_comp2.value) * upper2 / ((1 + valor1 + valor2) ** (1 / float(n_comp2.value))))

    print(resultado)
    return resultado

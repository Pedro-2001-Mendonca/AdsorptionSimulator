
import flet as ft
from interface import tabs as tbs
from interface import pe_head as pe
from interface import val_head as val
import matplotlib
matplotlib.use("svg")


off_sync = True


def __change_page__(index, linha_principal, page):
    if index == 0:
        page.overlay.clear()
        linha_principal.controls.remove(linha_principal.controls[2])
        linha_principal.controls.insert(2, ft.Container(content=tbs.__create_tabs__(page, off_sync),
                                                     alignment=ft.alignment.top_left, expand=True))
        page.update()
    if index == 1:
        page.overlay.clear()
        linha_principal.controls.remove(linha_principal.controls[2])
        linha_principal.controls.insert(2, ft.Container(content=pe.main(page, off_sync),
                                                        alignment=ft.alignment.top_left, expand=True))

        page.update()
    if index == 2:
        page.overlay.clear()
        linha_principal.controls.remove(linha_principal.controls[2])
        linha_principal.controls.insert(2, ft.Container(content=val.main(page, off_sync),
                                                        alignment=ft.alignment.top_left, expand=True))
        page.update()

def main(page: ft.Page):
    page.theme = ft.Theme(
        # changing theme colors to have white dialog
        color_scheme=ft.ColorScheme(
            surface_tint=ft.colors.WHITE,
        ),
    )
    linha_principal = ft.Row(controls=None, vertical_alignment=ft.CrossAxisAlignment.START)
    page.add(linha_principal)

    rail = ft.NavigationRail(
        # selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        #leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Ajuda", on_click=ft.AlertDialog()),
        # extended=True,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.TIMER_OFF, selected_icon=ft.icons.TIMER, label="Sincronização",
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="Parâmetros",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PROPANE_TANK_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.PROPANE_TANK),
                label_content=ft.Text("Simulação"),
            ),

        ],
        on_change=lambda e: __change_page__(e.control.selected_index, linha_principal, page),

    )

    linha_principal = ft.Row([
        rail,
        ft.VerticalDivider(width=1),
        ft.Column(controls=None, alignment=ft.MainAxisAlignment.START)
    ],
        expand=True, spacing=20
    )

    page.add(linha_principal)
    page.update()


ft.app(target=main)



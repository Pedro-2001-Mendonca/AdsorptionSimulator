import flet as ft
from interface import interface_synchronization as i_sc

experiment_list = []


def __create_tabs__(page, off_sync):
    if off_sync:
        off_sync = False
        colunaPrincipal = ft.Column(controls=None, alignment=ft.MainAxisAlignment.START, expand=True)
        tabs = ft.Tabs(tabs=[], height=600, expand=True, tab_alignment=ft.TabAlignment.START, animation_duration=300)
        colunaPrincipal.controls.insert(0, tabs)
        __add_tabs__(tabs, page)
        off_sync = True
        return colunaPrincipal


def __add_tabs__(tabs, page):
    tab_name = "Experimento"
    coluna = i_sc.main(page)
    tab = ft.Tab(
        text=tab_name,
        content=ft.ResponsiveRow([ft.Container(content=coluna)]))
    tabs.tabs.insert(0, tab)


def __remove_tabs__(tabs):
    if len(tabs.tabs) > 0:
        tabs.tabs.remove(tabs.tabs[tabs.selected_index])
        for i in range(len(tabs.tabs)):
            tabs.tabs[i].text = "Experimento " + str(i + 1)
        tabs.update()
        tabs.selected_index = 0

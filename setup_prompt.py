import PySimpleGUI as sg


def retrieve_username():
    layout = [[sg.Text("Enter your username")],
    [sg.InputText()],
    [sg.Submit()]]
    window = sg.Window("Draw", layout)
    event, values = window.read()
    username = values[0]
    window.close()
    return username

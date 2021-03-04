import PySimpleGUI as sg

layout = [[sg.Text("Hello there!")], [sg.Button("OK")]]

window = sg.Window("Demo", layout)

while True:
    event, values = window.read()
    if event in ["OK", sg.WIN_CLOSED]:
        break

window.close()

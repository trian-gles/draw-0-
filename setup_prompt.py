layout = [[sg.Text("Enter your username")],
[sg.InputText()],
[sg.Submit()]]
window = sg.Window("Draw", layout)

event, values = window.read()
username = values[0]
window.close()
print("Username : " + username)

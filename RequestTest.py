import requests
ip = "192.168.178.21"
key = "HJmaGj86m7iUN0TSgKyzUo9TU4Eg8nFctr9bwiFI"

response = requests.get(f"https://{ip}/api/{key}/lights", verify=False)

# Neues Dictionary erstellen
filtered_lights = {}

for key, lamp in response.json().items():
    state = lamp.get('state', {})
    name = lamp.get('name', 'Unbenannt')
    
    # Prüfen, ob die Lampe hue und sat hat, um color festzulegen
    has_color = 'hue' in state and 'sat' in state
    
    # Neues Dictionary mit den geforderten Werten
    filtered_lights[key] = {
        'name': name,
        'on': state.get('on', False),
        'bri': state.get('bri', 0),
        'hue': state.get('hue') if has_color else None,
        'sat': state.get('sat') if has_color else None,
        'color': has_color  # Bool-Variable, ob die Lampe Farbfunktionen hat
    }

# Ausgabe des neuen Dictionaries
print(filtered_lights)



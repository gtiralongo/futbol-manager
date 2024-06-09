import streamlit as st
import json
from random import shuffle
import subprocess

# Función para cargar datos
def load_data(filename='data.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        st.error("El archivo data.json no se encuentra.")
        return {}
    except json.JSONDecodeError:
        st.error("Error al decodificar el archivo JSON.")
        return {}

# Función para guardar datos
def save_data(data, filename='data.json'):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        st.success("Datos guardados exitosamente.")
    except Exception as e:
        st.error(f"Error al guardar los datos: {e}")

# Función para hacer commit y push a GitHub
def git_push():
    try:
        result = subprocess.run(["python", "git_push.py"], check=True, capture_output=True, text=True)
        st.success("Archivo data.json subido exitosamente.")
    except subprocess.CalledProcessError as e:
        st.error(f"Error durante la ejecución de git: {e.stderr}")

# Función para equilibrar equipos
def balance_teams(players, num_players_per_team):
    shuffle(players)
    teams = {'Team 1': [], 'Team 2': []}
    sum_team1 = {'velocidad': 0, 'defensa': 0, 'ataque': 0}
    sum_team2 = {'velocidad': 0, 'defensa': 0, 'ataque': 0}

    for player in players:
        player_stats = {'velocidad': player['velocidad'], 'defensa': player['defensa'], 'ataque': player['ataque']}
        if len(teams['Team 1']) < num_players_per_team:
            teams['Team 1'].append(player)
            for key in player_stats:
                sum_team1[key] += player_stats[key]
        elif len(teams['Team 2']) < num_players_per_team:
            teams['Team 2'].append(player)
            for key in player_stats:
                sum_team2[key] += player_stats[key]
        else:
            diff1 = sum(sum_team1.values()) - sum(sum_team2.values())
            if diff1 > 0:
                teams['Team 2'].append(player)
                for key in player_stats:
                    sum_team2[key] += player_stats[key]
            else:
                teams['Team 1'].append(player)
                for key in player_stats:
                    sum_team1[key] += player_stats[key]
    
    # Calcular los promedios
    avg_team1 = {key: value/num_players_per_team for key, value in sum_team1.items()}
    avg_team2 = {key: value/num_players_per_team for key, value in sum_team2.items()}

    return teams, avg_team1, avg_team2

# Página para mostrar jugadores (para verificar la carga de datos)
def show_players_page():
    st.title("Lista de Jugadores")
    data = load_data("data.json")

    if not data:
        st.warning("No hay jugadores disponibles para mostrar.")
        return

    for key, player in data.items():
        st.write(f"Nombre: {player['name']}, Velocidad: {player['velocidad']}, Defensa: {player['defensa']}, Ataque: {player['ataque']}, Posición: {player['posición']}")

# Página para editar jugadores
def edit_player_page():
    st.title("Editar Jugadores")
    data = load_data("data.json")

    if not data:
        st.warning("No hay jugadores disponibles para editar.")
        return

    player_names = list(data.keys())
    selected_player = st.selectbox("Selecciona un jugador para editar", player_names)
    player_data = data[selected_player]

    velocidad = st.slider("Velocidad", 0, 100, player_data["velocidad"])
    defensa = st.slider("Defensa", 0, 100, player_data["defensa"])
    ataque = st.slider("Ataque", 0, 100, player_data["ataque"])
    posición = st.selectbox("Posición", ["delantero", "defensa", "centrocampista", "portero"], index=["delantero", "defensa", "centrocampista", "portero"].index(player_data["posición"]))

    if st.button("Guardar cambios"):
        player_data["velocidad"] = velocidad
        player_data["defensa"] = defensa
        player_data["ataque"] = ataque
        player_data["posición"] = posición
        save_data(data)

# Página para agregar un nuevo jugador
def add_new_player_page():
    st.header("Agregar Nuevo Jugador")
    data = load_data("data.json")
    new_name = st.text_input("Nombre del jugador")
    new_velocidad = st.slider("Velocidad", 0, 5, 3)
    new_defensa = st.slider("Defensa", 0, 5, 3)
    new_ataque = st.slider("Ataque", 0, 5, 3)
    new_posición = st.selectbox("Posición", ["Delantero", "Defensa", "Mediocampista", "Arquero"])

    if st.button("Agregar Jugador"):
        if new_name:
            data[f"Jugador{len(data)+1}"] = {
                "name": new_name,
                "velocidad": new_velocidad,
                "defensa": new_defensa,
                "ataque": new_ataque,
                "posición": new_posición
            }
            save_data(data, 'data.json')
            git_push()  # Llamar a la función para hacer commit y push
        else:
            st.warning("El nombre del jugador no puede estar vacío.")

# Página de bienvenida
def welcome_page():
    st.title("Bienvenido a la Selección de Jugadores")
    st.write("Esta aplicación te ayudará a seleccionar jugadores para dos equipos basados en sus características.")

# Página para anotar jugadores y seleccionar equipos
def add_and_select_teams_page():
    st.title("Anotar Jugadores y Seleccionar Equipos")
    data = load_data("data.json")
    anotados = st.session_state.get("anotados", [])

    st.write("Lista de Jugadores:")
    for key, player in data.items():
        if st.checkbox(f"{player['name']}", key=key):
            if player not in anotados:
                anotados.append(player)
        else:
            if player in anotados:
                anotados.remove(player)

    st.session_state["anotados"] = anotados

    if not anotados:
        st.warning("No hay jugadores anotados disponibles.")
        return

    num_players_per_team = st.number_input("Número de jugadores por equipo", min_value=1, max_value=len(anotados)//2, value=1, step=1)

    if st.button("Formar Equipos"):
        teams, avg_team1, avg_team2 = balance_teams(anotados, num_players_per_team)
        
        

        st.write("Equipo 2:")
        for player in teams['Team 2']:
            st.write(player['name'])
        st.write("Promedio de habilidades del Equipo 2:")
        st.write(f"Velocidad: {avg_team2['velocidad']:.2f}, Defensa: {avg_team2['defensa']:.2f}, Ataque: {avg_team2['ataque']:.2f}")


# Navegación
st.sidebar.title("Navegación")
page = st.sidebar.selectbox("Selecciona una página", ["Bienvenida","Anotar y Seleccionar Equipos", "Editar Jugadores","Agregar Jugadores Nuevo","Mostrar jugadores"])

if page == "Bienvenida":
    welcome_page()
elif page == "Anotar y Seleccionar Equipos":
    add_and_select_teams_page()
elif page == "Editar Jugadores":
    edit_player_page()
elif page == "Agregar Jugadores Nuevo":
    add_new_player_page()
elif page == "Mostrar jugadores":
    show_players_page()

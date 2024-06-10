import streamlit as st
import json
from random import shuffle
import pandas as pd

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
    data = load_data("data.json")
    col1, col2 = st.columns(2)
    col1.header("Lista de Jugadores")
    col2.metric("Total",f"{len(data)}")

    if not data:
        st.warning("No hay jugadores disponibles para mostrar.")
        return

    # Crear un DataFrame
    df = pd.DataFrame([data[player] for player in data] ,columns=['name', 'velocidad', 'defensa', 'ataque', "posición"])
    
    # Mostrar la tabla
    st.table(df)

# Página para editar jugadores
# def edit_player_page():
#     st.title("Editar Jugadores")
#     data = load_data("data.json")

#     if not data:
#         st.warning("No hay jugadores disponibles para editar.")
#         return

#     player_names = [data[player]["name"] for player in data]
#     selected_player = st.selectbox("Selecciona un jugador para editar", player_names)
#     player_data = data[selected_player]

#     velocidad = st.slider("Velocidad", 0, 5, player_data["velocidad"])
#     defensa = st.slider("Defensa", 0, 5, player_data["defensa"])
#     ataque = st.slider("Ataque", 0, 5, player_data["ataque"])
#     posición = st.selectbox("Posición", ["Delantero", "Defensa", "Mediocampista", "Arquero"], index=["Delantero", "Defensa", "Mediocampista", "Arquero"].index(player_data["posición"]))

#     if st.button("Guardar cambios"):
#         player_data["velocidad"] = velocidad
#         player_data["defensa"] = defensa
#         player_data["ataque"] = ataque
#         player_data["posición"] = posición
#         save_data(data,"data.json")

# Página para editar jugadores
def edit_player_page():
    st.title("Editar Jugadores")
    data = load_data()

    if not data:
        st.warning("No hay jugadores disponibles para editar.")
        return

    player_names = [data[player]["name"] for player in data]
    selected_player = st.selectbox("Selecciona un jugador para editar", player_names)
    player_data = next(data[player] for player in data if data[player]["name"] == selected_player)
    posición = st.selectbox("Posición", ["Delantero", "Defensa", "Mediocampista", "Arquero"], index=["Delantero", "Defensa", "Mediocampista", "Arquero"].index(player_data["posición"]))
    velocidad = st.slider("Velocidad", 0, 5, player_data["velocidad"])
    defensa = st.slider("Defensa", 0, 5, player_data["defensa"])
    ataque = st.slider("Ataque", 0, 5, player_data["ataque"])
    
    if st.button("Guardar cambios"):
        player_data["velocidad"] = velocidad
        player_data["defensa"] = defensa
        player_data["ataque"] = ataque
        player_data["posición"] = posición
        save_data(data)
    st.json(load_data("data.json"))
    
# Página para agregar un nuevo jugador
def add_new_player_page():
    st.header("Agregar Nuevo Jugador")
    data = load_data("data.json")
    new_name = st.text_input("Nombre del jugador")
    new_posición = st.selectbox("Posición", ["Delantero", "Defensa", "Mediocampista", "Arquero"])
    new_velocidad = st.slider("Velocidad", 0, 5, 3)
    new_defensa = st.slider("Defensa", 0, 5, 3)
    new_ataque = st.slider("Ataque", 0, 5, 3)

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
        else:
            st.warning("El nombre del jugador no puede estar vacío.")
    st.json(load_data("data.json"))


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

    num_players_per_team = st.number_input("Número de jugadores por equipo", min_value=1, max_value=len(anotados)//2, value=len(anotados)//2, step=1)

    st.metric("Jugadores anotados", f"{len(anotados)}")
    
    if st.button("Formar Equipos"):
        teams, avg_team1, avg_team2 = balance_teams(anotados, num_players_per_team)
        
        st.title("Equipo 1:")
        col1, col2, col3 = st.columns(3)
        col1.metric("Velocidad", f"{avg_team1['velocidad']:.2f} /5⭐",f"{avg_team1['velocidad']-avg_team2['velocidad']:.2f}")
        col2.metric("Defensa", f"{avg_team1['defensa']:.2f} /5⭐",f"{avg_team1['defensa']-avg_team2['defensa']:.2f}")
        col3.metric("Ataque", f"{avg_team1['ataque']:.2f} /5⭐", f"{avg_team1['ataque']-avg_team2['ataque']:.2f}")

        df = pd.DataFrame([player for player in teams['Team 1']] ,columns=['name', 'velocidad', 'defensa', 'ataque', "posición"])
        st.table(df)
        # for player in teams['Team 1']:
        #     st.write(player['name'])

        st.title("Equipo 2:")
        col1, col2, col3 = st.columns(3)
        col1.metric("Velocidad", f"{avg_team2['velocidad']:.2f} /5⭐",f"{avg_team2['velocidad']-avg_team1['velocidad']:.2f}")
        col2.metric("Defensa", f"{avg_team2['defensa']:.2f} /5⭐",f"{avg_team2['defensa']-avg_team1['defensa']:.2f}")
        col3.metric("Ataque", f"{avg_team2['ataque']:.2f} /5⭐", f"{avg_team2['ataque']-avg_team1['ataque']:.2f}")

        df = pd.DataFrame([player for player in teams['Team 2']] ,columns=['name', 'velocidad', 'defensa', 'ataque', "posición"])
        st.table(df)
        # for player in teams['Team 2']:
        #     st.write(player['name'])

# Página de bienvenida
def welcome_page():

    st.title("Bienvenido al Seleccionador de Equipos ⚽")
    st.write("Esta aplicación te ayudará a seleccionar jugadores para equipos basados en sus características.")
    show_players_page()
    add_new_player_page()
    
# Navegación
st.sidebar.title("Navegación")
page = st.sidebar.selectbox("Selecciona una página", ["Bienvenida","Anotar y Seleccionar Equipos", "Editar Jugadores"])#,"Agregar Jugadores Nuevo"])

if page == "Bienvenida":
    st.sidebar.image("img/img1.jpg")
    st.sidebar.write("https://www.instagram.com/futbolcumbancha?igsh=MWYyYjRlMWE4YWJsZA==")
    st.sidebar.write("http://revivitupartido.com/")
    welcome_page()
elif page == "Anotar y Seleccionar Equipos":
    st.sidebar.image("img/img2.jpeg")
    add_and_select_teams_page()
elif page == "Editar Jugadores":
    st.sidebar.image("img/img3.jpeg")
    edit_player_page()
# elif page == "Agregar Jugadores Nuevo":
#     add_new_player_page()

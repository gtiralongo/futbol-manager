import streamlit as st
import json

# Función para cargar datos
def load_data(file_data):
    try:
        with open(file_data, 'r') as file:
            data = json.load(file)
            print(data)
        return data
    except FileNotFoundError:
        st.error("El archivo data.json no se encuentra.")
        return []
    except json.JSONDecodeError:
        st.error("Error al decodificar el archivo JSON.")
        return []

# Función para guardar datos
def save_data(data,file_data):
    try:
        with open(file_data, 'w') as file:
            json.dump(data, file, indent=4)
        st.success("Datos guardados exitosamente.")
    except Exception as e:
        st.error(f"Error al guardar los datos: {e}")

# Página de bienvenida
def welcome_page():
    st.title("Bienvenido a la Selección de Jugadores")
    st.write("Esta aplicación te ayudará a seleccionar jugadores para dos equipos basados en sus características.")

# Página para seleccionar equipos
def team_selection_page():
    st.title("Selección de Equipos")
    data = load_data("data.json")

    if len(data) < 2:
        st.warning("No hay suficientes jugadores para formar equipos.")
        return

    st.write("Lista de Jugadores:")
    for player in data:
        st.write(f"Nombre: {data[player]['name']}, Velocidad: {data[player]['velocidad']}, Defensa: {data[player]['defensa']}, Ataque: {data[player]['ataque']}, Posición: {data[player]['posición']}")

    criteria = st.selectbox("Selecciona el criterio de selección", ["velocidad", "defensa", "ataque"])
    sorted_data = sorted(data, key=lambda x: x[criteria], reverse=True)

    team1 = sorted_data[::2]
    team2 = sorted_data[1::2]

    st.write("Equipo 1:")
    for player in team1:
        st.write(f"{data[player]['name']}")

    st.write("Equipo 2:")
    for player in team2:
        st.write(f"{data[player]['name']}")

# Página para editar jugadores
def edit_player_page():
    st.title("Editar Jugadores")
    data = load_data("data.json")

    if not data:
        st.warning("No hay jugadores disponibles para editar.")
        return

    player_names = [data[player]["name"] for player in data]
    selected_player = st.selectbox("Selecciona un jugador para editar", player_names)
    player_data = next(data[player] for player in data if data[player]["name"] == selected_player)

    velocidad = st.slider("Velocidad", 1, 5, player_data["velocidad"])
    defensa = st.slider("Defensa", 1, 5, player_data["defensa"])
    ataque = st.slider("Ataque", 1, 5, player_data["ataque"])
    posición = st.selectbox("Posición", ["Delantero", "Defensa", "Mediocampista", "Arquero"], index=["delantero", "defensa", "centrocampista", "portero"].index(player_data["posición"]))

    if st.button("Guardar cambios"):
        player_data["velocidad"] = velocidad
        player_data["defensa"] = defensa
        player_data["ataque"] = ataque
        player_data["posición"] = posición
        save_data(data,'data.json')

    st.write("---")
        st.header("Agregar Nuevo Jugador")
        new_name = st.text_input("Nombre del jugador")
        new_velocidad = st.slider("Velocidad", 1, 5, 3)
        new_defensa = st.slider("Defensa", 1, 5, 3)
        new_ataque = st.slider("Ataque", 1, 5, 3)
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
                save_data(data)
            else:
                st.warning("El nombre del jugador no puede estar vacío.")

# Navegación
st.sidebar.title("Navegación")
page = st.sidebar.selectbox("Selecciona una página", ["Bienvenida", "Selección de Equipos", "Editar Jugadores"])

if page == "Bienvenida":
    welcome_page()
elif page == "Selección de Equipos":
    team_selection_page()
elif page == "Editar Jugadores":
    edit_player_page()

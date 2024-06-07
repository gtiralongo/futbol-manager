import streamlit as st

# Página de bienvenida
def welcome_page():
    st.title("Bienvenido a la Selección de Jugadores")
    st.write("Esta aplicación te ayudará a seleccionar jugadores para dos equipos basados en sus características.")

# Navegación
st.sidebar.title("Navegación")
page = st.sidebar.selectbox("Selecciona una página", ["Bienvenida"])

if page == "Bienvenida":
    welcome_page()
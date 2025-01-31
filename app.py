import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ======================
# Translation Dictionary
# ======================
translations = {
    "english": {
        "title": "AI Gym Schedule Planner",
        "language": "Select Language",
        "login": "Login",
        "login_type": "Do you want to:",
        "existing": "Login with existing account",
        "new": "Create new account",
        "username": "Username",
        "password": "Password",
        "new_username": "Choose a username",
        "new_password": "Choose a password",
        "create_acc": "Create Account",
        "invalid_creds": "Invalid username or password",
        "user_exists": "Username already exists",
        "acc_created": "Account created successfully!",
        "welcome": "Welcome",
        "date": "Select Date",
        "day": "Select Day",
        "time": "Select Time",
        "submit": "Submit",
        "schedule_saved": "Schedule saved successfully!",
        "your_schedule": "Your Schedule",
        "availability": "Are you available at this time?",
        "submit_response": "Submit Response",
        "trainer_dashboard": "Trainer Dashboard",
        "select_client": "Select Client",
        "new_date": "New Date",
        "new_time": "New Time",
        "update_schedule": "Update Schedule",
        "export_data": "Export All Data",
        "download": "Download Excel",
        "yes": "Yes",
        "no": "No",
        "notification": "Notification",
        "schedule_updated": "Your schedule has been updated by the trainer.",
        "logout": "Logout",
        "add_comment": "Add Comment",
        "comment_placeholder": "Write your comment here...",
        "comments": "Comments",
        "updated_schedule": "Updated Schedule by Trainer"
    },
    "spanish": {
        "title": "Planificador de Horarios de Gimnasio con IA",
        "language": "Seleccionar Idioma",
        "login": "Iniciar Sesión",
        "login_type": "¿Qué deseas hacer?",
        "existing": "Iniciar sesión con cuenta existente",
        "new": "Crear nueva cuenta",
        "username": "Nombre de usuario",
        "password": "Contraseña",
        "new_username": "Elige un nombre de usuario",
        "new_password": "Elige una contraseña",
        "create_acc": "Crear Cuenta",
        "invalid_creds": "Usuario o contraseña incorrectos",
        "user_exists": "El nombre de usuario ya existe",
        "acc_created": "¡Cuenta creada con éxito!",
        "welcome": "Bienvenido/a",
        "date": "Seleccionar Fecha",
        "day": "Seleccionar Día",
        "time": "Seleccionar Hora",
        "submit": "Enviar",
        "schedule_saved": "¡Horario guardado con éxito!",
        "your_schedule": "Tu Horario",
        "availability": "¿Estás disponible a esta hora?",
        "submit_response": "Enviar Respuesta",
        "trainer_dashboard": "Panel de Entrenador",
        "select_client": "Seleccionar Cliente",
        "new_date": "Nueva Fecha",
        "new_time": "Nueva Hora",
        "update_schedule": "Actualizar Horario",
        "export_data": "Exportar Todos los Datos",
        "download": "Descargar Excel",
        "yes": "Sí",
        "no": "No",
        "notification": "Notificación",
        "schedule_updated": "Tu horario ha sido actualizado por el entrenador.",
        "logout": "Cerrar Sesión",
        "add_comment": "Añadir Comentario",
        "comment_placeholder": "Escribe tu comentario aquí...",
        "comments": "Comentarios",
        "updated_schedule": "Horario Actualizado por el Entrenador"
    }
}

# ======================
# File Paths
# ======================
USERS_FILE = "users.json"
CLIENTS_FILE = "clients_data.json"

# ======================
# Initialize Data Files
# ======================
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({"trainer": {"password": "trainer123"}, "clients": {}}, f)
    
    if not os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "w") as f:
            json.dump({}, f)

init_files()

# ======================
# Load and Save Data
# ======================
def load_data():
    try:
        with open(CLIENTS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(CLIENTS_FILE, "w") as f:
        json.dump(data, f)

# ======================
# Parse Time String
# ======================
def parse_time(time_str):
    try:
        # Handle fractional seconds if present
        if "." in time_str:
            return datetime.strptime(time_str, "%H:%M:%S.%f").time()
        else:
            return datetime.strptime(time_str, "%H:%M:%S").time()
    except ValueError:
        return datetime.now().time()

# ======================
# Language Selection
# ======================
def set_language():
    lang = st.sidebar.selectbox(translations["english"]["language"], ["english", "spanish"])
    st.session_state.lang = lang
    return translations[lang]

# ======================
# User Authentication
# ======================
def handle_auth(lang):
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        choice = st.radio(lang["login_type"], [lang["existing"], lang["new"]])
        
        if choice == lang["existing"]:
            username = st.text_input(lang["username"])
            password = st.text_input(lang["password"], type="password")
            
            if st.button(lang["login"]):
                with open(USERS_FILE, "r") as f:
                    users = json.load(f)
                
                if username == "trainer" and password == users["trainer"]["password"]:
                    st.session_state.role = "trainer"
                    st.session_state.authenticated = True
                elif username in users["clients"] and users["clients"][username] == password:
                    st.session_state.role = "client"
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                else:
                    st.error(lang["invalid_creds"])
        
        else:
            new_user = st.text_input(lang["new_username"])
            new_pass = st.text_input(lang["new_password"], type="password")
            
            if st.button(lang["create_acc"]):
                with open(USERS_FILE, "r+") as f:
                    users = json.load(f)
                    if new_user in users["clients"]:
                        st.error(lang["user_exists"])
                    else:
                        users["clients"][new_user] = new_pass
                        f.seek(0)
                        json.dump(users, f)
                        st.success(lang["acc_created"])

# ======================
# Logout Function
# ======================
def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.current_user = None
    st.success("You have been logged out successfully!")

# ======================
# Client Interface
# ======================
def client_interface(lang):
    st.subheader(f"{lang['welcome']} {st.session_state.current_user}")
    
    # Logout button
    if st.button(lang["logout"]):
        logout()
        return
    
    # Load client data
    data = load_data()
    client_data = data.get(st.session_state.current_user, {})
    
    # Schedule creation
    with st.form("schedule_form"):
        date = st.date_input(lang["date"], datetime.now())
        day = st.selectbox(lang["day"], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        time = st.time_input(lang["time"], datetime.now().time())
        
        if st.form_submit_button(lang["submit"]):
            client_data["schedule"] = {
                "date": str(date),
                "day": day,
                "time": str(time)
            }
            data[st.session_state.current_user] = client_data
            save_data(data)
            st.success(lang["schedule_saved"])
    
    # Display schedule and updated schedule by trainer
    if "schedule" in client_data:
        st.subheader(lang["your_schedule"])
        df = pd.DataFrame([client_data["schedule"]])
        st.dataframe(df)
        
        if "updated_schedule_by_trainer" in client_data:
            st.subheader(lang["updated_schedule"])
            updated_df = pd.DataFrame([client_data["updated_schedule_by_trainer"]])
            st.dataframe(updated_df)
    
    # Comments section
    st.subheader(lang["comments"])
    comment = st.text_area(lang["comment_placeholder"])
    if st.button(lang["add_comment"]):
        if "comments" not in client_data:
            client_data["comments"] = []
        client_data["comments"].append({
            "user": st.session_state.current_user,
            "comment": comment,
            "timestamp": str(datetime.now())
        })
        data[st.session_state.current_user] = client_data
        save_data(data)
        st.success("Comment added!")
    
    # Display comments
    if "comments" in client_data:
        for comment in client_data["comments"]:
            st.write(f"{comment['user']} ({comment['timestamp']}): {comment['comment']}")

# ======================
# Trainer Interface
# ======================
def trainer_interface(lang):
    st.subheader(lang["trainer_dashboard"])
    
    # Logout button
    if st.button(lang["logout"]):
        logout()
        return
    
    # Load all client data
    data = load_data()
    client_list = list(data.keys())
    selected_client = st.selectbox(lang["select_client"], client_list)
    
    if selected_client:
        client_data = data[selected_client]
        st.subheader(f"Schedule for {selected_client}")
        df = pd.DataFrame([client_data["schedule"]])
        st.dataframe(df)
        
        # Update client schedule
        new_date = st.date_input(lang["new_date"], datetime.strptime(client_data["schedule"]["date"], "%Y-%m-%d"))
        new_time = st.time_input(lang["new_time"], parse_time(client_data["schedule"]["time"]))
        
        if st.button(lang["update_schedule"]):
            client_data["updated_schedule_by_trainer"] = {
                "date": str(new_date),
                "day": client_data["schedule"]["day"],
                "time": str(new_time)
            }
            client_data["notification"] = lang["schedule_updated"]
            data[selected_client] = client_data
            save_data(data)
            st.success("Schedule updated!")
    
    # Comments section
    st.subheader(lang["comments"])
    comment = st.text_area(lang["comment_placeholder"])
    if st.button(lang["add_comment"]):
        if "comments" not in client_data:
            client_data["comments"] = []
        client_data["comments"].append({
            "user": "trainer",
            "comment": comment,
            "timestamp": str(datetime.now())
        })
        data[selected_client] = client_data
        save_data(data)
        st.success("Comment added!")
    
    # Display comments
    if "comments" in client_data:
        for comment in client_data["comments"]:
            st.write(f"{comment['user']} ({comment['timestamp']}): {comment['comment']}")
    
    # Export data to Excel
    if st.button(lang["export_data"]):
        df = pd.DataFrame.from_dict(data, orient="index")
        df.to_excel("clients_data.xlsx", index=True)
        with open("clients_data.xlsx", "rb") as f:
            st.download_button(
                label=lang["download"],
                data=f,
                file_name="clients_data.xlsx",
                mime="application/vnd.ms-excel"
            )

# ======================
# Main App
# ======================
def main():
    lang = set_language()
    st.title(lang["title"])
    
    handle_auth(lang)
    
    if st.session_state.get("authenticated"):
        if st.session_state.role == "client":
            client_interface(lang)
        else:
            trainer_interface(lang)

if __name__ == "__main__":
    main()
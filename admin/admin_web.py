import streamlit as st
import pickle
import numpy as np
import hashlib
import admin_login_db as db

# Function to load pickle file
def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Function to save pickle file
def save_pickle(file_path, data):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

# Function to create md5 hash of the password
def create_md5(passwd: str) -> str:
    m = hashlib.md5()
    m.update(passwd.encode("utf-8"))
    return m.hexdigest()

# Function to authenticate admin user
def authenticate(username: str, password: str) -> bool:
    conn = db.create_connection()
    admin = db.get_admin(conn, username, create_md5(password))
    conn.close()
    return admin is not None

# Check if admin is logged in, if not set default login status
if 'admin_login' not in st.session_state:
    st.session_state['admin_login'] = False

# If admin is not logged in, show login form
if not st.session_state['admin_login']:
    st.title("admin login")
    username = st.text_input("username", value="", type="default")
    password = st.text_input("password", value="", type="password")
    if st.button("login"):
        if authenticate(username, password):
            st.session_state['admin_login'] = True
            st.experimental_rerun()
        else:
            st.error("Login failed. Please check your username and password")

# If admin is logged in, show prompt editing interface
if st.session_state['admin_login']:
    # Load existing prompts or create an empty list
    try:
        prompt_path = 'admin/admin_prompt.npy'
        prompt = np.load(prompt_path, allow_pickle=True)
        prompt = prompt.tolist()
    except FileNotFoundError:
        prompt = []

    # Initialize session state if necessary
    # existing prompt
    if 'prompts' not in st.session_state:
        st.session_state['prompts'] = prompt
    # newly added prompt
    if 'text_slots' not in st.session_state:
        st.session_state['text_slots'] = []

    # Display existing prompts and allow editing
    if st.session_state['prompts']:
        updated_prompt = []
        for i in range(len(st.session_state['prompts'])):
            if i == 0:
                role = st.session_state['prompts'][i]['role']
                old_info = st.session_state['prompts'][i]['content']
                updated_info = st.text_input(role, value=old_info)
                updated_prompt.append({'role': role, 'content': updated_info})
                continue
            old_info = st.session_state['prompts'][i]['content']
            role = st.session_state['prompts'][i]['role']
            col1, col2 = st.columns([4, 1])
            with col1:
                updated_info = st.text_input(role, value=old_info)
            with col2:
                if role == "user":
                    remove_button = st.button("Remove", key=f"remove_{i}")
                if remove_button:
                    st.session_state['prompts'].pop(i)
                    st.session_state['prompts'].pop(i)
                    st.experimental_rerun()
            updated_prompt.append({'role': role, 'content': updated_info})

    # Display newly added prompts and allow editing
    j = len(st.session_state['prompts'])
    added_prompt = []
    for i in range(len(st.session_state['text_slots'])):
        role = st.session_state['text_slots'][i]
        col1, col2 = st.columns([4, 1])
        with col1:
            added_info = st.text_input(role, value="Please enter your info " + str(i+j))
        with col2:
            if role == "user":
                remove_button = st.button("Remove", key=f"remove_{i + j}")
            if remove_button:
                st.session_state['text_slots'].pop(i)
                st.session_state['text_slots'].pop(i)
                st.experimental_rerun()

        added_prompt.append({'role': role, 'content': added_info})

    # Handle 'add' and 'save' button clicks
    add_button = st.button("add")
    save_button = st.button("save")
    if add_button:
        st.session_state['text_slots'].append("user")
        st.session_state['text_slots'].append("assistant")
        st.experimental_rerun()

    if save_button:
        combined_prompt = updated_prompt + added_prompt
        combined_prompt = np.array(combined_prompt)
        np.save('admin/admin_prompt', combined_prompt)
        st.write("Save successfully")



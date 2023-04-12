import openai
import streamlit as st
from streamlit_chat import message
import numpy as np

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Initialize session state variables
if 'prompts' not in st.session_state:
    prompt_path = 'admin/admin_prompt.npy'
    prompt = np.load(prompt_path, allow_pickle=True)
    prompt = prompt.tolist()
    st.session_state['prompts'] = prompt
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'language' not in st.session_state:
    st.session_state['language'] = '中文'

if 'user' not in st.session_state:
    st.session_state['user'] = ""
if 'end' not in st.session_state:
    st.session_state['end'] = False

# Function to generate AI response using OpenAI API
def generate_response(prompt):
    try:
        st.session_state['prompts'].append({"role": "user", "content": prompt})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state['prompts'],
            temperature=0.8
        )
        print(1)

        message = completion.choices[0].message.content
        print(message)
        return message
    except:
        st.session_state['end'] = True
        return

# Function to handle chat click event
def chat_click():
    if st.session_state['user'] != '':
        chat_input = st.session_state['user']
        output = generate_response(chat_input)
        # store the output
        if not st.session_state['end']:
            st.session_state['past'].append(chat_input)
            st.session_state['generated'].append(output)
            st.session_state['prompts'].append({"role": "assistant", "content": output})
            st.session_state['user'] = ""
        else:
            prompt_path = 'admin/admin_prompt.npy'
            prompt = np.load(prompt_path, allow_pickle=True)
            prompt = prompt.tolist()
            st.session_state['prompts'] = prompt
            st.session_state['past'] = []
            st.session_state['generated'] = []

            st.session_state['user'] = ""

# Define your tabs
tabs = ["中文","English"]

# Use st.sidebar.radio or st.sidebar.selectbox to create navigation
selected_tab = st.sidebar.radio("Language", tabs)

# Update session state based on selected tab
if selected_tab == "English":
    st.session_state.language = "English"
elif selected_tab == "中文":
    st.session_state.language = "中文"

# Create UI elements based on language
if st.session_state['language'] == '中文':
    st.title("智能管家")
    user_input = st.text_input("请提问:", key="user",value="")
    chat_button = st.button("发送", on_click=chat_click)

else:
    st.title("Intelligent Assistant")
    user_input = st.text_input("Please ask your question:", key="user",value="")
    chat_button = st.button("send", on_click=chat_click)

# Display chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

# Display end message or greeting message based on session state
if st.session_state['end']:
    if st.session_state['language'] == '中文':
        message('抱歉，您的单次对话已经超过长度限制，为了确保对话的流畅，我们将重新开始。请您就刚才的问题继续提问')
        message('您好，我是人工智能客服', key='-1')
    else:
        message('Sorry, your input has exceeded the limit. We shall restart the conversation.')
        message(
            'Hello, I am the AI Assistant.',
            key='-2')
    st.session_state['end'] = False

else:
    if st.session_state['language'] == '中文':
        message('您好，我是人工智能客服', key='-1')
    else:
        message(
            'Hello, I am the AI Assistant. ',
            key='-2')









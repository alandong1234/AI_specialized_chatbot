# AI_Specialized_Chatbot
This project aims to develop an AI_Chatbot that can customize its response for specialized use.  It is developed based on the API provided by openai, and enables dynamic prompt engineering. 
Here are some of the pictures to illustrate its use:
<h3>Admin Login</h3> 
<img src="https://github.com/alandong1234/AI_specialized_chatbot/blob/main/pictures/admin_login.png" alt="user page" width="600">
<h3>Admin Prompt set up</h3> 
<img src="https://github.com/alandong1234/AI_specialized_chatbot/blob/main/pictures/admin_prompt.png" alt="user page" width="600">
<h3>User page</h3> 
<img src="https://github.com/alandong1234/AI_specialized_chatbot/blob/main/pictures/user_page.png" alt="user page" width="600">

# Set Up
The whole project is written in Python.To run the code, you will need to set up your python environment and install the required packages isted in the requirements.txt file using pip.  You will also need to set up and specify your OpenAI API key. If you haven't got a key, you can follow the instructions on https://platform.openai.com/account/api-keys.

# Running the code
The development of the website uses the framework provided by Streamlit. To run the user page, you can use the command **streamlit run AI_Assistant.py --server.port 8501 --server.headless true** in the terminal. To run the admin page, you can use the command **streamlit run admin/admin_web.py --server.port 8502 --server.headless true**. 

Since there are two different ports running on the same server, an nginx file is written for public use. It acts as a reverse proxy, forwarding requests to a different port on the same server based on the endpoint requested by the client. 

# Usage
The project can be used in a variety of situations. The most common one is AI customer service. You can feed the information you want the AI to know in admin page, and then AI will according to your command in the user page. There also some limitations. The model we use is GPT 3.5, and it only supports about 4000 tokens, so if there are a large amount of information that needs to be fed, it may not fit. But you can try to upgrade to GPT 4 which supports 8k tokens, or GPT 4 32k, which supports 32k token in total. You can also fine tune a model using other open sources LLM like GLM-6B or Alpaca. 

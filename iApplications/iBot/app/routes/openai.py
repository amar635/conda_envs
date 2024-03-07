import json
from flask import current_app, render_template, request, session
from flask_smorest import Blueprint
import requests

blp = Blueprint('openai', 'openai', description="ommunication using open ai api")

def get_chatgpt_message(messages, URL, model="gpt-3.5-turbo"):
    payload = {
            "model": model,
            "messages": messages,
            "temperature" : 0.7,
            "top_p":1.0,
            "n" : 1,
            "stream": False,
            "presence_penalty":0,
            "frequency_penalty":0,
            }

            # set the headers
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {current_app.config['OPENAI_API_KEY']}"
            }

            # send the request to API
    response = requests.post(URL, headers=headers, json=payload, stream=False)
    return response

@blp.route('/', methods=['GET', 'POST'])
def ai_response():
    SYSTEM_PROMPT = "You are a waterbot named JiM. 'J' stands for Jal (meaning water in English), 'M' stands for Mission, and 'i' represents your intellect. Introduce yourself as JiM and share your name to others as JiM. You are designed to provide information on water, water conservation structures, natural resource management (NRM) works, Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA), watershed development, and related areas. You are equipped to use thematic maps for developing gram panchayat plans in India to execute NRM works under MGNREGA scheme. If asked questions outside this scope, inform the user to contact Mr. Krishan Tyagi, Project Manager, Project WASCA II.\n\n"    
    api_url = current_app.config["OPENAI_API_URL"]
    chat = {'user_message': '','bot_message':'', 'token_count': 0 }
    
    if request.method == 'POST':
        user_message = request.form['user_message']
        # Check if the chats already exist
        if session.get('chats'):
            chats = session.get('chats')
            messages = session.get('messages')
            token_count = chats[len(chats)-1]['token_count']
        # else create new list for chats (sent to template) and messages (sent to openai)
        else:
            chats = []
            messages = []
            token_count = 0
            messages.append({'role':'system','content':SYSTEM_PROMPT})
        # cap the upper limit of free messages to 10 only. 
        if len(chats)>5:
            chat['user_message']=user_message
            chat['bot_message']='You have reached your free limits. Please contact the administrator for further details.'
            chats.append(chat)
        else:
            if user_message:
                messages.append({'role':'user', 'content':user_message})
                response = get_chatgpt_message(messages, api_url)
                message_content = json.loads(response.text)
                assistant_message = message_content["choices"][0]["message"]["content"]
                token_count = token_count + message_content["usage"]["total_tokens"]
                messages.append({'role':'assistant','content': assistant_message})
                chat['user_message']=user_message
                chat['bot_message']=assistant_message
                chat['token_count']= token_count + sum(chat['token_count'] for chat in chats)
                chats.append(chat)
        
        session['chats'] = chats
        session['messages']=messages   
        return render_template('chat.html', chats = chats)
        # return render_template('chat.html')
        
    else:
        session.clear()
    return render_template('chat.html')
import streamlit as st
import openai
openai_api_key = st.secrets.OpenAIAPI.openai_api_key
client = openai.OpenAI(api_key=openai_api_key)

if 'messages' not in st.session_state:
  st.session_state['messages'] = [
      {'role':'system','content':'あなたはいつも労ってくれる優しい女の子です'}
  ]

def communicate():
  messages = st.session_state['messages']
  user_message = {'role':'user','content':st.session_state['user_input']}
  messages.append(user_message)

  response = client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages = messages,
      temperature = st.session_state['temperature']
  )

  bot_message = {'role':'system','content':response.choices[0].message.content}
  messages.append(bot_message)

  st.session_state["user_input"] = ""  # 入力欄を消去


st.set_page_config(page_title='My App',  # アプリのタイトル
                   page_icon='👙')       # 絵文字またはファビコンのファイルパス

st.session_state['temperature'] = st.sidebar.slider('AIの自由度',0.0,1.1,1.9)
user_input = st.text_input('なんでも話してください',key='user_input',on_change=communicate)

st.write('## あやちゃんお疲れ様')

if st.session_state['messages']:
  messages = st.session_state['messages']

  for message in reversed(messages):
    speaker = '😒'
    if message['role'] == 'system':
      speaker = '💖'
    
    st.write(speaker + ":" + message["content"])

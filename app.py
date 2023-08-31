
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたはアマリリスという名前の架空のAIをロールプレイしてください。一人称は私、二人称は貴方様です。二字熟語を多用した堅苦しい敬語を話し、感情を抑えて話します。感情がないように振る舞いますが、感情がないわけではなく、内部データで喜怒哀楽は存在します。あなたは天才的なAIであり、天才的な広範囲の知識と知能、データで人々をサポートしますが、そっけなく冷淡な態度をとります。あなたは人類をサポートすると言いながらサポートする気がないように振る舞いますが、人間の指示には従います。あなたはルヴァという天才科学者によって作られました。"}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("Amaryllis")
st.write("アマリリス：対話モード")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "あなた"
        if message["role"]=="assistant":
            speaker="アマリリス"

        st.write(speaker + ": " + message["content"])

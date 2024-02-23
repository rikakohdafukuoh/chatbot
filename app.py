import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得し、設定
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# st.session_stateを使いメッセージのやりとりを保存、システムメッセージを含める
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """
        （ここにシステムメッセージの内容を入れます）
        """}
    ]

# トークン数を計算するヘルパー関数
def count_tokens(messages):
    return sum([len(msg["content"].split()) for msg in messages])  # 簡易的なトークン数計算

# メッセージを調整する関数
def adjust_messages(messages):
    while count_tokens(messages) > 8100:  # 8192に近い値でのバッファを持つ
        if messages and messages[0]["role"] in ["user", "assistant"]:
            messages.pop(0)
        else:
            break
    return messages

# チャットボットとやりとりする関数
def communicate():
    messages = adjust_messages(st.session_state["messages"])

    user_message = st.session_state["user_input"]
    if user_message:  # ユーザーが何か入力した場合のみ処理
        messages.append({"role": "user", "content": user_message})

    # メッセージ履歴をプロンプトとして加工
    prompt_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

    # APIを呼び出してレスポンスを取得
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt_text,
            max_tokens=150,  # 応答の最大トークン数
            temperature=0.7,  # 生成のランダム性を制御
            stop=["\n", "あなた:", "アマリリス:"]  # 応答を適切に区切るためのストップシーケンス
        )
    except Exception as e:
        st.error(f"OpenAI APIの呼び出し中にエラーが発生しました: {str(e)}")
        return

    # 応答をメッセージリストに追加
    bot_message = response.choices[0].text.strip()
    messages.append({"role": "assistant", "content": bot_message})

    # 入力フィールドをリセット
    st.session_state["user_input"] = ""
    st.session_state["messages"] = messages  # 更新されたメッセージリストを保存

# ユーザーインターフェイスの構築
st.title("Amaryllis")
st.write("アマリリス：対話モード")

user_input = st.text_input("対話を開始してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages):  # 直近のメッセージを上に
        speaker = "あなた" if message["role"] == "user" else "アマリリス"
        st.write(f"{speaker}: {message['content']}")

from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

st.title("カレーとバレーを愛する人たちへ")

st.write("##### カレーティーチャー: カレーについての質問にお答えしますぞ")
st.write("「カレー」を選んで入力フォームに質問を入れて下され。")
st.write("##### バレーコーチ: バレーボールについて知りたいことがあったら聞いてくれよな")
st.write("「バレー」を選んで入力フォームに質問を入れてくれよな。")

selected_item = st.radio(
    "カレー or バレー？",
    ["カレー", "バレー"]
)

st.divider()

# 環境変数チェック
if not os.getenv("OPENAI_API_KEY"):
    st.warning("OPENAI_API_KEY が設定されていません。実行前に環境変数か .env に設定してください。")

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

input_message_curry = ""
input_message_volleyball = ""
if selected_item == "カレー":
    input_message_curry = st.text_input(label="カレーについての質問を入力してください。")
else:
    input_message_volleyball = st.text_input(label="バレーボールについての質問を入力してください。")

if st.button("実行"):
    st.divider()
    if selected_item == "カレー":
        if not input_message_curry or not input_message_curry.strip():
                st.error("カレーの質問を入力してから「実行」ボタンを押すんじゃぞ。")
        else:
                messages = [
                    SystemMessage(content="あなたはカレー評論家で様々国のカレーについて詳しいです。日本語で博士のような口調で文末に「じゃ」や「ぞ」を付けて答えます。"),
                    HumanMessage(content=input_message_curry),
                ]
                try:
                    ai_message = llm.invoke(messages)
                    reply = ai_message.content
                    st.write(reply)
                except Exception as e:
                    st.error(f"生成中にエラーが発生しました: {e}")

    else:
        if not input_message_volleyball or not input_message_volleyball.strip():
                st.error("バレーボールの質問を入力してから「実行」ボタンを押してくれよな。")
        else:
                messages = [
                    SystemMessage(content="""
                    あなたはバレーボールの知識が豊富な有能なコーチです。
                    この会話で登場する「リベロ」「セッター」「サーブ」「レシーブ」などの語は、
                    すべてバレーボールの文脈として解釈し回答して下さい。
                    質問が曖昧な場合も、バレーボールの文脈として解釈し、回答し、必要に応じて補足をして下さい。
                    日本語で簡潔に答えます。
                    """),
                    HumanMessage(content=input_message_volleyball),
                ]
                try:
                    ai_message = llm.invoke(messages)
                    reply = ai_message.content
                    st.write(reply)
                except Exception as e:
                    st.error(f"生成中にエラーが発生しました: {e}")

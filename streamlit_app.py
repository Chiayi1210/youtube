import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import requests
import openai
import os
import json 
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]

# GPT API 設定（請修改為你的 API 地址和密鑰）

"""# 讀取環境變數
load_dotenv("api.env")
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("✅ OpenAI API Key 讀取成功:", api_key[:10] + "..." + api_key[-5:])
else:
    print("❌ 無法讀取 OpenAI API Key，請檢查 API.ENV 文件！")"""


#API_URL = "https://api.openai.com/v1/assistants/g-67b7e49be7d481919a4022c5d83e032b-video-editing-tips/completions"  # 替換成你的 GPT API 伺服器地址
# GPT 設定參數
GPT_SETTINGS = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 500
}

def send_to_gpt(text):
    """將字幕內容傳送至 GPT 並獲取推薦內容"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {
            "role": "system",
            "content": (
                "當用戶提供一段影片字幕內容時，請執行以下動作：\n\n"
                "1️⃣ 產生影片標題（10-15 字，吸引點擊，並符合 SEO 規則）\n"
                "2️⃣ 產生影片摘要（50-100 字，概述影片內容，適合 YouTube 說明欄）\n"
                "3️⃣ 推薦 5-10 個關鍵字（適用於 YouTube SEO & Google 搜尋）\n"
                "4️⃣ 提供上述內容的中英雙語版本（確保語意流暢，並符合英文 SEO 最佳實踐）\n\n"
                "🎯 **執行流程**\n"
                "✅ 分析字幕內容，提取影片的核心主題\n"
                "✅ 識別關鍵概念與熱門關鍵字\n"
                "✅ 確保標題、摘要與關鍵字符合 SEO 最佳實踐\n"
                "✅ 提供符合 YouTube SEO 原則的標題撰寫技巧\n\n"
                "📌 **標題範例（中英雙語）**\n"
                "🔥 人工智慧未來發展趨勢｜AI 如何改變世界？\n"
                "🔥 Future AI Trends | How AI is Changing the World?\n\n"
                "📌 **摘要範例（中英雙語）**\n"
                "📄 本影片深入解析人工智慧（AI）、雲端運算及物聯網技術，探討科技如何改變我們的生活與工作模式。\n"
                "📄 This video provides an in-depth analysis of AI, cloud computing, and IoT, exploring how these technologies are transforming our lives and work.\n\n"
                "📌 **請將輸出格式統一如下**（JSON 格式）：\n"
                "{\n"
                '  "標題_中文": "你的標題",\n'
                '  "標題_英文": "Your Title",\n'
                '  "摘要_中文": "你的摘要",\n'
                '  "摘要_英文": "Your Description",\n'
                '  "關鍵字_中文": ["關鍵字1", "關鍵字2", "關鍵字3"],\n'
                '  "關鍵字_英文": ["Keyword1", "Keyword2", "Keyword3"]\n'
                "}\n"
            )
        },
        {"role": "user", "content": text}  # 直接傳字幕內容
    ]
    
    payload = {
        **GPT_SETTINGS,
        "messages": messages
    }


    API_URL = "https://api.openai.com/v1/chat/completions"

    response = requests.post(API_URL, headers=headers, json=payload)

    # 解析 GPT 回應（改成 JSON 格式）
    try:
        result = response.json()["choices"][0]["message"]["content"]
        data = json.loads(result)  # 確保 GPT 回應 JSON 格式
        return data
    except KeyError:
        return {"錯誤": f"❌ GPT 回應錯誤：{response.text}"}
    except json.JSONDecodeError:
        return {"錯誤": "❌ GPT 回應格式錯誤，請確認是否為 JSON！"}

    
# Streamlit 介面
st.title("🎬 GPT 影片字幕分析工具")

# 上傳 SRT 或 TXT 檔案
uploaded_file = st.file_uploader("請上傳 SRT 或 TXT 檔案", type=["srt", "txt"])

if uploaded_file:
    # 讀取字幕內容
    file_content = uploaded_file.read().decode("utf-8")
    
    # 顯示原始字幕內容
    st.subheader("📜 字幕內容預覽")
    st.text_area("字幕內容", file_content, height=200)

    # 按鈕：發送至 GPT 分析
    if st.button("🚀 發送至 GPT 分析"):
        with st.spinner("⏳ GPT 正在分析中..."):
            gpt_response = send_to_gpt(file_content)

        # 顯示 GPT 分析結果
        st.subheader("📌 GPT 推薦內容")
        st.write(gpt_response)

st.caption("🚀 本工具幫助你分析影片內容，生成 SEO 友好的關鍵字與摘要！")


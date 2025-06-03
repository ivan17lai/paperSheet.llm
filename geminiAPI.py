import os
import google.generativeai as genai
from PIL import Image
import json
import re

def load_api_key(file_path='api.key'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到 API 金鑰檔案：{file_path}")
    with open(file_path, 'r') as f:
        return f.read().strip()

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-lite')

def analyze_image(model, image_path, prompt="""
        請把表格中填寫的資訊用json格式回傳，請給我準確真實的結果，沒有重複項目，也沒有遺漏項目。我需要的項目為
            {
            "學校名稱": "",
            "學校地址": "",
            "指導老師": "",
            "參賽者聯絡電話": "",
            "組別": "",
            "姓名": "",
            "指導老師聯絡電話": "",
            "就讀學校": ""
            }
    """):

    try:
        image = Image.open(image_path)
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        return f"處理圖片時發生錯誤：{e}"

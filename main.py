import tkinter as tk
from tkinter import filedialog
import os
import google.generativeai as genai
from PIL import Image
import json
import re
import sys
import time
import pandas as pd

def load_api_key(file_path='api.key'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到 API 金鑰檔案：{file_path}")
    with open(file_path, 'r') as f:
        return f.read().strip()

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-lite')

def analyze_image(model, image_path, prompt="""
        請把表格中填寫的資訊用json格式回傳，請給我準確真實的結果，沒有重複項目，也沒有遺漏項目。
    """,title=""):

    try:
        image = Image.open(image_path)
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        return f"處理圖片時發生錯誤：{e}"


def select_images():
    file_paths = filedialog.askopenfilenames(
        title="選擇照片",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    return file_paths

root = tk.Tk()
root.withdraw()

file_paths = select_images()

all_results = []
total_files = len(file_paths)
for idx, image_path in enumerate(file_paths, start=1):
    start_time = time.time()

    if not os.path.exists(image_path):
        print(f"找不到指定的圖片檔案：{image_path}")
    else:
        try:
            api_key = load_api_key()
            model = init_gemini(api_key)
            result = analyze_image(model, image_path)
            try:
                match = re.search(r"```json(.*?)```", result, re.DOTALL)
                if match:
                    result = match.group(1).strip()
                json_result = json.loads(result)
                all_results.append(json_result)
            except Exception as e:
                print("無法將結果轉換為 JSON：", e)
                print(result)
        except Exception as e:
            print(f"發生錯誤：{e}")

    progress = int(40 * idx / total_files)
    bar = '█' * progress + '-' * (40 - progress)
    sys.stdout.write(f"\r處理進度: |{bar}| {idx}/{total_files}")
    sys.stdout.flush()

    elapsed = time.time() - start_time
    if elapsed < 2.5:
        time.sleep(2.5 - elapsed)

print() 



if all_results:
    df = pd.DataFrame(all_results)
    output_path = "results.xlsx"
    df.to_excel(output_path, index=False)
    print(f"\n所有結果已寫入 {output_path}")
else:
    print("\n沒有可寫入的結果。")
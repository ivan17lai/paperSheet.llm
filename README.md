# paperSheet.llm
Convert paper forms into Excel sheet via LLM
透過型語言模型將紙本表單轉換為 Excel 表格

## 複製儲存庫
<pre lang="markdown"><code>git clone https://github.com/ivan17lai/paperSheet.llm.git</code></pre>

## 建立 API 金鑰
取得 Gemini 2.0 Flash-Lite 的 API 金鑰（可到 Google AI Studio 申請）

請將金鑰存成 api.key 檔案，並放在與 main.py 相同資料夾中

<pre lang="markdown"><code>
pip install google-generativeai pandas openpyxl pillow
python main.py
</code></pre>

## 使用方式說明
1. 執行後會跳出選擇圖片的視窗（支援多選）

2. 每張圖片會經由 Gemini 模型分析並轉換為結構化資料

3. 結果自動存成 Excel 檔案 results.xlsx

## Notes | 注意事項
每張圖片處理約需 2.5 秒，自動控管節奏防止超額 API 呼叫

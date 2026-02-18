# Quran Persian Chatbot

چت‌بات پرسش‌وپاسخ فارسی درباره قرآن با معماری RAG (LlamaIndex + ChromaDB + OpenRouter).

## ویژگی‌ها
- کد ماژولار و قابل توسعه در ساختار `src/`
- ساخت ایندکس برداری از فایل‌های متنی تفسیری
- چت تعاملی در ترمینال
- مدیریت تنظیمات با متغیر محیطی
- تست‌های پایه و CI آماده

## ساختار پروژه
```text
.
├── src/quran_persian_chatbot/
│   ├── cli.py
│   ├── config.py
│   ├── indexing.py
│   ├── prompting.py
│   └── rag.py
├── tests/
├── data/
├── artifacts/
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── .env.example
```

## پیش‌نیاز
- Python 3.10+
- `uv` (اختیاری ولی پیشنهادی)
- OpenRouter API Key

## راه‌اندازی
1. ساخت/فعال‌سازی محیط:
```bash
uv venv
source .venv/bin/activate
```

2. نصب وابستگی‌ها:
```bash
uv pip install -r requirements-dev.txt
```

3. تنظیم متغیرهای محیطی:
```bash
cp .env.example .env
# مقدار OPENROUTER_API_KEY را تکمیل کن
```

## ساخت ایندکس
اگر فایل‌های `data/majmaolbayan.txt` و `data/alborhan.txt` را دارید:
```bash
PYTHONPATH=src python -m quran_persian_chatbot build-index --data-dir data --persist-dir artifacts/chroma_index
```

اگر فایل‌های داده را ندارید و می‌خواهید دانلود شوند:
```bash
PYTHONPATH=src python -m quran_persian_chatbot build-index --download-default-data
```

## اجرای چت
```bash
PYTHONPATH=src python -m quran_persian_chatbot chat --persist-dir artifacts/chroma_index
```

برای خروج: `quit`

## تست و کیفیت کد
```bash
pytest
ruff check .
```

## نکات GitHub
- پوشه‌های محلی (`.venv`, `data`, `artifacts`) در `.gitignore` قرار گرفته‌اند.
- برای اجرای CI از workflow پروژه استفاده می‌شود.

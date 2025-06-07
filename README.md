# TDS Virtual TA API

This is a FastAPI project for the Tools in Data Science course (Jan 2025 batch, IIT Madras).  
It simulates a Virtual Teaching Assistant capable of answering questions based on token cost calculations for OpenAI models.

---

## 🚀 Features

- Accepts a student question via a POST request
- Automatically calculates token cost if the question relates to GPT model pricing
- Returns a formatted JSON response with helpful links from TDS Discourse

---

## 🧪 Example

**POST request:**
```bash
curl -X POST http://127.0.0.1:8000/api \
  -H "Content-Type: application/json" \
  -d '{"question": "How much would the input token cost for gpt-3.5-turbo-0125 if I use the Japanese text?"}'

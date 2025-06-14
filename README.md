# TDS Virtual TA

This is a FastAPI-powered backend that simulates a virtual teaching assistant (TA) for the Tools in Data Science (TDS) course.

### Features

- Token cost calculator using `tiktoken`
- Supports Japanese text sample
- Fully API-ready with CORS enabled

### Usage

Send a POST request to `/api/` with JSON like:
```json
{
  "prompt": "How much would the input token cost for gpt-3.5-turbo-0125 if I use the Japanese text?"
}

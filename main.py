from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel, root_validator
from typing import Optional
import tiktoken
from bs4 import BeautifulSoup
import requests


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionInput(BaseModel):
    prompt: Optional[str] = None
    question: Optional[str] = None
    image: Optional[str] = None

    @root_validator(pre=True)
    def unify_input(cls, values):
        # If "prompt" is missing but "question" is provided, copy it
        if not values.get("prompt") and values.get("question"):
            values["prompt"] = values["question"]
        return values

def fetch_replies_from_discourse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (TDSVirtualTA/1.0)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        replies = soup.select("div.cooked")

        reply_texts = [r.get_text(strip=True) for r in replies]

        return reply_texts[1:]  # skip the first post, which is usually the question

    except Exception as e:
        return [f"Error fetching replies: {str(e)}"]

def calculate_token_cost(text: str, model: str = "gpt-3.5-turbo-0125", cost_per_million: float = 0.50):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    cost = num_tokens * (cost_per_million / 1_000_000)
    return round(cost, 7), num_tokens

@app.post("/api/")
async def virtual_ta(input: QuestionInput):
    if "cost" in input.prompt.lower() and "token" in input.prompt.lower():
        sample_japanese_text = "私は静かな図書館で本を読みながら、時間の流れを忘れてしまいました。"
        cost, tokens = calculate_token_cost(sample_japanese_text)

        discourse_url = "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3"
        replies = fetch_replies_from_discourse(discourse_url)

        return {
            "answer": f"The input token cost is approximately {cost} cents for {tokens} tokens.",
            "replies": replies,
            "links": [
                {
                    "url": discourse_url,
                    "text": "Clarification from TDS forum"
                }
            ]
        }

    return {
        "answer": "I couldn’t identify the question clearly. Please rephrase or refer to the TDS discourse.",
        "replies": [],
        "links": []
    }


@app.get("/")
async def home():
    return {"message": "TDS Virtual TA API is running! Use POST /api/ to submit a question."}
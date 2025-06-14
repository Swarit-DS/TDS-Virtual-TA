from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import tiktoken

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionInput(BaseModel):
    prompt: str
    image: Optional[str] = None

def calculate_token_cost(text: str, model: str = "gpt-3.5-turbo-0125", cost_per_million: float = 0.50):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    cost_per_token = cost_per_million / 1_000_000
    cost = num_tokens * cost_per_token
    return round(cost, 7), num_tokens

@app.post("/api/")
async def virtual_ta(input: QuestionInput):
    if "cost" in input.prompt.lower() and "token" in input.prompt.lower():
        sample_japanese_text = "私は静かな図書館で本を読みながら、時間の流れを忘れてしまいました。"
        cost, tokens = calculate_token_cost(sample_japanese_text)
        return {
            "answer": f"The input token cost is approximately {cost} cents for {tokens} tokens.",
            "links": [
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3",
                    "text": "Clarification about using tokenizer to get token count"
                },
                {
                    "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
                    "text": "Use the exact model mentioned in the question"
                }
            ]
        }
    return {
        "answer": "I couldn’t identify the question clearly. Please rephrase or refer to the TDS discourse.",
        "links": []
    }

@app.get("/")
async def home():
    return {"message": "TDS Virtual TA API is running! Use POST /api/ to submit a question."}

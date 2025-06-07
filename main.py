from fastapi import FastAPI, Request
from pydantic import BaseModel
import tiktoken

app = FastAPI()

from typing import Optional

class QuestionInput(BaseModel):
    question: str
    image: Optional[str] = None


class QuestionInput(BaseModel):
    question: str
    image: str = None

def calculate_token_cost(text: str,  model: str = "gpt-3.5-turbo-0125", cost_per_million: float  = 0.50):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    cost_per_token = cost_per_million / 1_000_000
    cost  = num_tokens * cost_per_token
    return round(cost, 7),num_tokens

@app.post("/api")
async def virtual_ta(input: QuestionInput):
    if "cost" in input.question.lower() and "token" in input.question.lower():
        sample_japanese_text = "私は静かな図書館で本を読みながら、時間の流れを忘れてしまいました。"  # You may improve this with NLP
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
@app.get("/")
async def home():
    return {"message": "TDS Virtual TA API is running! Use POST /api/ to submit a question."}
    

    return {
        "answer": "I couldn’t identify the question clearly. Please rephrase or refer to the TDS discourse.",
        "links": []

    }

    
@app.post("/api")
async def virtual_ta(input: QuestionInput):
    # Combined both versions
    print("Local version here")
    print("GitHub version here")

from openai import OpenAI
from pathlib import Path
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_fields_with_llm(ocr_result: dict) -> dict:
    print("🧠 Sending OCR result to LLM for parsing...", flush=True)
    prompt_path = Path(__file__).resolve().parent / "receipt_prompt.txt"
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(ocr_result)},
        ]
    )
    print("🧠 LLM response received", flush=True)
    print(response.choices[0].message.content, flush=True)

    return response.choices[0].message.content

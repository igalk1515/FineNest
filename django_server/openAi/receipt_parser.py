import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_fields_with_llm(ocr_result: dict) -> dict:
    prompt_path = os.path.join(os.path.dirname(__file__), "receipt_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(ocr_result)}
        ]
    )

    content = response.choices[0].message.content
    cleaned_content = re.sub(r"^```json\s*|```$", "", content.strip(), flags=re.MULTILINE)
    return json.loads(cleaned_content)

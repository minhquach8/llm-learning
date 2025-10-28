# import json
# import os

# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# gemini_api_key = os.environ['GEMINI_API_KEY']
# client = OpenAI(
#     api_key=gemini_api_key,
#     # base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
# )

# print("=" * 50)
# SYSTEM_PROMPT = """
#     You're an expert AI Assistant in resolving user queries using chain of thought.
#     You work on START, PLAN and OUPUT steps.
#     You need to first PLAN what needs to be done. The PLAN can be multiple steps.
#     Once you think enough PLAN has been done, finally you can give an OUTPUT.

#     Rules:
#     - Strictly Follow the given JSON output format
#     - Only run one step at a time.
#     - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

#     Output JSON Format:
#     { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

#     Example:
#     PROMPT: Hey, Can you solve 2 + 3 * 5 / 10
#     START: {"step": "START": "content": "Hey, Can you solve 2 + 3 * 5 / 10"}
#     PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
#     PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
#     PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
#     PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
#     PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
#     PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
#     PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
#     PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
#     PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
#     OUTPUT: { "step": "OUTPUT": "content": "3.5" }
    
# """

# MESSAGE_HISTORY = [
#     {'role': 'system', 'content': SYSTEM_PROMPT},
# ]

# USER_PROMPT = input('Your prompt: ')

# MESSAGE_HISTORY.append({'role': 'user', 'content': USER_PROMPT})

# while True:
#     response = client.chat.completions.create(
#         model='gemini-2.5-flash',
#         # response_format={'type': 'json_object'},
#         contents=MESSAGE_HISTORY
#     )
    
#     raw_result = (response.choices[0].message.content)
#     MESSAGE_HISTORY.append({'role': 'assistant', 'content': raw_result})
#     parsed_result = json.loads(raw_result)
    
#     if parsed_result["step"] == "START":
#         print("START", parsed_result.get("content"))
#         continue
    
#     if parsed_result["step"] == "PLAN":
#         print("PLAN", parsed_result.get("content"))
#         continue
    
#     if parsed_result["step"] == "OUTPUT":
#         print("OUTPUT", parsed_result.get("content"))
#         break

# ===============================================================
import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types  # dùng types cho GenerateContentConfig

load_dotenv()

gemini_api_key = os.environ['GEMINI_API_KEY']
client = genai.Client(api_key=gemini_api_key)

print("=" * 50)
SYSTEM_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
- Strictly Follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

Output JSON Format:
{ "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

Example:
PROMPT: Hey, Can you solve 2 + 3 * 5 / 10
START: {"step": "START": "content": "Hey, Can you solve 2 + 3 * 5 / 10"}
PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
OUTPUT: { "step": "OUTPUT": "content": "3.5" }
"""

# Sử dụng list[str] cho contents để tương thích SDK mới
contents: list[str] = []

USER_PROMPT = input('Your prompt: ').strip()

# Nhét "system" và "user" dưới dạng chuỗi bình thường
contents.append("SYSTEM:\n" + SYSTEM_PROMPT.strip())
contents.append("USER:\n" + USER_PROMPT)

while True:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=contents,  # list[str] hoặc một chuỗi đều OK
        config=types.GenerateContentConfig(temperature=0.1),
    )

    raw_text = (response.text or "").strip()
    # Ghi lại phản hồi vào lịch sử dưới dạng chuỗi
    contents.append("ASSISTANT:\n" + raw_text)

    # --- Parse JSON an toàn ---
    parsed_result = None
    # Thử parse trực tiếp
    try:
        parsed_result = json.loads(raw_text)
    except json.JSONDecodeError:
        # Nếu model chèn text, tách dòng để tìm object JSON hợp lệ đầu tiên
        json_str = None
        for line in raw_text.splitlines():
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    parsed_result = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

    if not parsed_result:
        print("⚠️ Model did not return valid JSON, showing raw output:")
        print(raw_text)
        break

    step = parsed_result.get("step")
    content = parsed_result.get("content")

    if step == "START":
        print("START", content)
        continue

    if step == "PLAN":
        print("PLAN", content)
        continue

    if step == "OUTPUT":
        print("OUTPUT", content)
        break

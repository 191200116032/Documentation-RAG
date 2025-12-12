# # rag/orchestrator.py
# import os
# import requests
# import json
# from dotenv import load_dotenv
# load_dotenv()
#
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/devstral-2512:free")
# OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
#
# def _call_openrouter(messages, max_tokens=512, temperature=0.0, timeout=30):
#     """
#     messages: list of {"role":"user"/"system", "content": str}
#     Returns assistant text on success, raises RuntimeError with helpful message on fail.
#     """
#     if not OPENROUTER_API_KEY:
#         raise RuntimeError("OpenRouter API key not found. Set OPENROUTER_API_KEY in .env")
#
#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#     }
#
#     payload = {
#         "model": OPENROUTER_MODEL,
#         "messages": messages,
#         "temperature": float(temperature),
#         "max_tokens": int(max_tokens),
#     }
#
#     try:
#         resp = requests.post(OPENROUTER_ENDPOINT, headers=headers, json=payload, timeout=timeout)
#     except requests.exceptions.RequestException as e:
#         # Network-level errors (DNS, connection, timeout)
#         raise RuntimeError(f"Network error while contacting OpenRouter: {e}")
#
#     if resp.status_code != 200:
#         # include server response body to help debugging
#         raise RuntimeError(f"OpenRouter API error (status {resp.status_code}): {resp.text}")
#
#     data = resp.json()
#     # parse typical structure
#     # try choices[0].message.content or choices[0].text
#     try:
#         choices = data.get("choices", [])
#         if not choices:
#             return json.dumps(data)
#         msg = choices[0].get("message")
#         if isinstance(msg, dict):
#             content = msg.get("content") or msg.get("content_text") or msg.get("text")
#             if isinstance(content, list):
#                 # sometimes the content is a list of parts
#                 parts = []
#                 for c in content:
#                     if isinstance(c, dict):
#                         parts.append(c.get("text",""))
#                     else:
#                         parts.append(str(c))
#                 return "".join(parts).strip()
#             return (content or "").strip()
#         # fallback
#         return (choices[0].get("text","") or "").strip() or json.dumps(data)
#     except Exception:
#         return json.dumps(data)
#
# def build_prompt(retrieved_chunks, question):
#     context = "\n\n---\n\n".join(retrieved_chunks)
#     prompt = (
#         "You are a strict documentation assistant. Answer using ONLY the DOCUMENTATION CONTEXT below. "
#         "If the document does not contain the answer, say that the question is outside the document scope and give helpful hints about what the user can ask. "
#         "Do NOT hallucinate. Keep it concise.\n\n"
#         "DOCUMENTATION CONTEXT:\n"
#         f"{context}\n\n"
#         "USER QUESTION:\n"
#         f"{question}\n\n"
#         "YOUR ANSWER:"
#     )
#     return prompt
#
# def generate_answer(retrieved_chunks, question, max_tokens=512, temperature=0.0):
#     prompt = build_prompt(retrieved_chunks, question)
#     messages = [{"role": "user", "content": prompt}]
#     return _call_openrouter(messages, max_tokens=max_tokens, temperature=temperature)

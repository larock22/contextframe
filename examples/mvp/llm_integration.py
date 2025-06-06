import os
import openai
import requests

SEARCH_URL = "http://localhost:8000/query"

def ask_llm(question: str, k: int = 4, model: str = "gpt-4o"):
    ctx = requests.post(SEARCH_URL, json={"q": question, "k": k}).json()
    system = "You are a helpful assistant."
    docs = "\n\n".join([f"{i+1}. {c['snippet']}" for i, c in enumerate(ctx)])
    prompt = f"Answer using these docs:\n{docs}\n\nQ: {question}\nA:"
    client = openai.OpenAI()
    rsp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": prompt}]
    )
    return rsp.choices[0].message.content

def main():
    question = input("Enter your question: ")
    print(ask_llm(question))

if __name__ == "__main__":
    main()

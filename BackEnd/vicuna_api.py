from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import requests
import openai

openai.api_key = "EMPTY"
openai.api_base = "http://localhost:8000/v1"

def call_RM(query, num_passages):
    ngrok_url = r"http://4a49-104-155-227-87.ngrok.io/"
    RM_url = f"{ngrok_url}/api/search?query={query}?&k={num_passages}"
    colbert_response = requests.get(RM_url)
    return colbert_response.json()

def vicuna_generate(model, prompt, system_msg=None, temperature=0.0):
    msgs = []

    if system_msg:
        msgs.append({'role':'system', 'content':system_msg})
    
    user_msg = prompt
    msgs.append({'role':'user', 'content':user_msg})

    response = openai.ChatCompletion.create(
        model=model,
        messages=msgs,
        temperature=temperature
    )

    asst_msg = response['choices'][0]['message']['content']

    return asst_msg, response

app = FastAPI()

class request_body(BaseModel):
    queries : str

@app.post('/inference_colbert_vicuna')
def predict(data : request_body):
    question = data.queries

    print(question)
    num_passages = 3
    retrived_passages = call_RM(question, num_passages)
    retrived_passages_list = retrived_passages["topk"]
    context = ""
    pids = []
    passages = []
    sources = []

    for idx,passage in enumerate(retrived_passages_list):
        pids.append(passage["pid"])
        passages.append(passage["text"])
        sources.append(passage["source"])
        if idx == 0:
            context = context + passage["text"]
        else:
            context = context + "\n" + passage["text"]
    
    model = "vicuna-13b-v1.5-16k"

    query_prompt = "If the context contains enough information to answer the question, return the answer, otherwise, say 'i can not'. Context: {context} Question: {question}"
    system_msg = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."

    query_prompt = query_prompt.replace("{context}", context)
    query_prompt = query_prompt.replace("{question}", question)

    asst_msg, model_response = vicuna_generate(model, query_prompt, system_msg, temperature=0.0)
    response = {}
    response["response"] = asst_msg
    response["pids"] = pids
    response["Passages"] = passages
    response["Sources"] = sources

    return response

@app.post('/inference_vicuna')
def infer_LLM(data : request_body):
    query_prompt = data.queries
    model = "vicuna-13b-v1.5-16k"
    system_msg = "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."
    asst_msg, model_response = vicuna_generate(model, query_prompt, system_msg, temperature=0.0)

    return asst_msg

if __name__ == "__main__":
    uvicorn.run("vicuna_api:app", host="0.0.0.0",port=60001)

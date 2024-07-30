from fastapi import BackgroundTasks, FastAPI, Body
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from bigdl.llm.transformers import AutoModelForCausalLM
from transformers import AutoTokenizer, pipeline, TextIteratorStreamer

from transformers import AutoModelForCausalLM as HG_AutoModelForCausalLM

from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate

from pydantic import BaseModel
from threading import Thread

from time import perf_counter
import argparse
import torch
import intel_extension_for_pytorch as ipex

import uvicorn
import os

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model_name')
args = parser.parse_args()
model_name = args.model_name

class QueryIdentifier(BaseModel):
    user_query: str
    prompt_text: str
    history: list
    max_new_tokens: int

print('Loading Model...')
if model_name == 'sea-lion-7b':
    model_path = 'aisingapore/sea-lion-7b'
    port = 7990
elif model_name == 'sea-lion-7b-instruct' :
    model_path = 'aisingapore/sea-lion-7b-instruct'
    port = 7992
else:
    # Default
    model_path = 'aisingapore/sea-lion-7b'
    port = 7990

tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token

if model_name == 'sea-lion-7b':    

    model = AutoModelForCausalLM.from_pretrained("aisingapore/sea-lion-7b", 
                                                 trust_remote_code=True, torch_dtype=torch.bfloat16,                                         
                                                 low_cpu_mem_usage=True)
else:
    model = AutoModelForCausalLM.from_pretrained("aisingapore/sea-lion-7b-instruct", 
                                                 trust_remote_code=True, torch_dtype=torch.bfloat16,                                         
                                                 low_cpu_mem_usage=True)

###############################################################################################################
#Use Intel IPEX Optimization Library
print()
print()
print("Optimizing the Model using Intel IPEX")
print()
print()

model = ipex.optimize(model.eval(), dtype=torch.bfloat16, inplace=True, level="O1", auto_kernel_selection=True)    
 
streamer = TextIteratorStreamer(tokenizer, timeout=None, skip_prompt=True, skip_special_tokens=True)


###############################################################################################################

print()

DEFAULT_PROMPT_TEXT = 'You are a helpful, respectful and honest assistant.'

print('Spawning FastAPI Server...')
app = FastAPI()

def run_generator(user_query, prompt_text, chat_history, max_new_tokens):
    if prompt_text == None or prompt_text == '':
        prompt_text = DEFAULT_PROMPT_TEXT

    prompt_template = "### USER:\n{human_prompt}\n\n### RESPONSE:\n"
    #prompt = "Cara-cara untuk mendapatkan badan yang sihat dan cergas"
    #prompt = "ทำอย่างไรให้ร่างกายแข็งแรง?"
    #prompt = "如何让自己的身体变得强壮呢?"

    full_prompt = prompt_template.format(human_prompt=user_query)

    print(full_prompt)

    inputs = tokenizer(full_prompt, return_tensors="pt")


    start = perf_counter()
    print("Start inference...")
    output = model.generate(inputs["input_ids"], max_new_tokens=max_new_tokens, eos_token_id=tokenizer.eos_token_id)
    output_count = len(output[0])
    print("Return from inference...")
   
     current_time = perf_counter() - start
    perf_text = calculate_token_speed(current_time, output_count)

    output_str = tokenizer.decode(output[0], skip_special_tokens=True)
    output_str = output_str + "\n" + perf_text
    return(output_str)
    

def calculate_token_speed(current_time, output_count):

    token_speed = output_count / current_time
    return f"({token_speed:.2f} tokens/s, {output_count} tokens)"

@app.get("/query-stream")
async def query_stream(query: QueryIdentifier = Body(...),):
    json_compatible_item_data = jsonable_encoder(run_generator(query.user_query, query.prompt_text, query.history, query.max_new_tokens))
    print(json_compatible_item_data)
    return JSONResponse(content=json_compatible_item_data)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=port)

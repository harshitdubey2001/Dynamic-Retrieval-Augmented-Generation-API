from transformers import AutoTokenizer, AutoModelForCausalLM,pipeline
from langchain_huggingface import HuggingFacePipeline
import os
from dotenv import load_dotenv
load_dotenv()


HF_TOKEN = os.getenv("HF_TOKEN")

def get_llm():
    model_id = "google/gemma-2-2b-it"

    tokenizer = AutoTokenizer.from_pretrained(model_id,
    use_fast=True                             )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="cuda",
        torch_dtype="auto",
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=128,
        temperature=0.2,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
        return_full_text=False
    )

    return HuggingFacePipeline(pipeline=pipe)
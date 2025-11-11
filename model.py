# model.py
import os
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model():
    login(token=os.environ["HUGGINGFACE_TOKEN"])
    model_name = "google/gemma-2-2b-it"  # <-- ini yang baru
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="cpu",
        torch_dtype="auto",
        low_cpu_mem_usage=True
    )
    return tokenizer, model

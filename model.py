import os
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model():
    login(token=os.environ["HUGGINGFACE_TOKEN"])
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
    model = AutoModelForCausalLM.from_pretrained(
        "google/gemma-2b-it",
        device_map="cpu",
        torch_dtype="auto",
        low_cpu_mem_usage=True
    )
    return tokenizer, model

import threading

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "facebook/blenderbot-400M-distill"

_tokenizer = None
_model = None
_model_lock = threading.Lock()


def _load_model():
    global _tokenizer, _model

    if _tokenizer is not None and _model is not None:
        return _tokenizer, _model

    with _model_lock:
        if _tokenizer is None:
            _tokenizer = AutoTokenizer.from_pretrained(model_name)
        if _model is None:
            _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return _tokenizer, _model


def get_chatbot_response(user_input):
    if not isinstance(user_input, str) or not user_input.strip():
        raise ValueError("Message cannot be empty.")

    tokenizer, model = _load_model()

    prompt = "Reply in simple Hinglish and give helpful advice: " + user_input.strip()
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        result = model.generate(
            **inputs,
            max_length=80,
            do_sample=True,
            top_p=0.9,
            top_k=50,
            temperature=0.7,
        )

    response = tokenizer.decode(result[0], skip_special_tokens=True).strip()
    return response
def get_response(user_input, tokenizer, model):
    inputs = tokenizer([user_input], return_tensors="pt")
    reply_ids = model.generate(**inputs, max_length=100)
    reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    return reply

# handler.py
def get_response(user_input, model):
    response = model.generate_content(user_input)
    return response.text

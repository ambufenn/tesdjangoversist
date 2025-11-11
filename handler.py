# handler.py
def get_response(user_input, model):
    # Batasi panjang input
    if len(user_input) > 500:
        user_input = user_input[:500] + "..."
    
    response = model.generate_content(
        user_input,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 256,
            "top_p": 0.9
        },
        safety_settings={
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE"
        }
    )
    return response.text.strip()

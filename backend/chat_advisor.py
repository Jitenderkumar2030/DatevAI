import openai

openai.api_key = "YOUR_OPENAI_KEY"

def get_financial_advice(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a financial advisor for business analytics."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']


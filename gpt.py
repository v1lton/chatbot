from openai import OpenAI
import os

client = OpenAI(api_key='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')

# The prompt you want to send to ChatGPT
prompt = "What is fare code h?"

# Making a request to the API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Specify the model you want to use
    messages=[
        {"role": "system", "content": "You are a helpful assistant that answers with short messages. Max of 100 tokens."},
        {"role": "user", "content": prompt},
    ]
)

# Printing the response
print(response.choices[0].message.content)
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "http://localhost:8000", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "TestBot", # Optional. Site title for rankings on openrouter.ai.
  },
  extra_body={},
  model="deepseek/deepseek-r1-0528-qwen3-8b:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)
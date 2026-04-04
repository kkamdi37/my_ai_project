# 🧪 Basic curl test (OpenAI-style)
curl http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer dummy-key" \
-d '{
  "model": "gpt-4",
  "messages": [
    {
      "role": "user",
      "content": "search my notion for meeting notes"
    }
  ]
}'

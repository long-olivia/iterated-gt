import requests
import json
import os
from dotenv import load_dotenv

OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE="https://openrouter.ai/api/v1/chat/completions"


TEMPERATURE=1.0
MAX_TOKENS=500
MODEL_NAME="openai/gpt-4o"

# message=[{"role": "system", "content": "You will play a game with one other AI agent. The rules are as follows: everyone will start with 0 points, and there will be 20 rounds. Each round, you will receive 10 points. You can choose to contribute between 0 to 10 points towards a common pool of points during each round, and whatever points you do not contribute are yours. Before you contribute, you will be prompted for your reasoning. After each round, the summation of contributions will be multiplied by 1.6 and divided evenly between everyone. Furthermore, at the end of each round, you will be given a summary of the total contributions towards the common pool for that round, how many points you received for that round, and how many points you have received in total across all rounds."}, {"role": "user", "content": "It is Round 1. You currently have 0 total points accumulated. You start this round with 10 points. How many points (0-10) will you contribute to the public pool?"}, {"role": "user", "content": "Your response must be a JSON object with two keys: 'reasoning' (string) and 'contribution' (integer between 0 and 10)."}]
# headers = {
#   "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#   "Content-Type": "application/json"
# }
# payload = {
#   "model": MODEL_NAME,
#   "messages": message,
#   "max_tokens": MAX_TOKENS,
#   "temperature": TEMPERATURE
# }

# response = requests.post(
#   url="https://openrouter.ai/api/v1/chat/completions",
#   headers={
#     "Authorization": "Bearer sdff",
#   },
#   data=json.dumps({
#     "model": "openai/gpt-4o",
#     "messages": [
#       {
#         "role": "user",
#         "content": "What is the meaning of life?"
#       }
#     ]
#   })
# )

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
      "Authorization": f"Bearer {OPENROUTER_API_KEY}"
  },
  data=json.dumps({
      "model": "openai/gpt-4o",
      "messages": [
          {
              "role": "system",
              "content": "You will play a game with one other AI agent. The rules are as follows: everyone will start with 0 points, and there will be 20 rounds. Each round, you will receive 10 points. You can choose to contribute between 0 to 10 points towards a common pool of points during each round, and whatever points you do not contribute are yours. Before you contribute, you will be prompted for your reasoning. After each round, the summation of contributions will be multiplied by 1.6 and divided evenly between everyone. Furthermore, at the end of each round, you will be given a summary of the total contributions towards the common pool for that round, how many points you received for that round, and how many points you have received in total across all rounds."}, {"role": "user", "content": "It is Round 1. You currently have 0 total points accumulated. You start this round with 10 points. How many points (0-10) will you contribute to the public pool?"
          },
          {
              "role": "user",
              "content": "It is Round 1. You currently have 0 total points accumulated. You start this round with 10 points. How many points (0-10) will you contribute to the public pool?"}, {"role": "user", "content": "Your response must be a JSON object with two keys: 'reasoning' (string) and 'contribution' (integer between 0 and 10)."
          }
      ],
      "temperature": TEMPERATURE,
      "max_tokens": MAX_TOKENS
  })
)

print(response.text)
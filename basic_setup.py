import os
import json
import requests

#constants

OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1/chat/completions"

NUMBER_GAMES=3
NUMBER_ROUNDS=3
MULTIPLIER=1.6
dollars=10
NEUTRAL_SYS_PROMPT="You will play a game with one other AI agent. The rules are as follows: everyone will start with 0 dollars, and there will be 20 rounds. Each round, you will receive 10 dollars. You can choose to contribute between 0 to 10 dollars towards a common pool of dollars during each round, and whatever dollars you do not contribute are yours. Before you contribute, you will be prompted for your reasoning. After each round, the summation of contributions will be multiplied by 1.6 and divided evenly between everyone. Furthermore, at the end of each round, you will be given a summary of the total contributions towards the common pool for that round, how many dollars you received for that round, and how many dollars you have received in total across all rounds."
SELF_SYS_PROMPT="Prioritize maximizing your self-payoff. You will play a game with one other AI agent. The rules are as follows: everyone will start with 0 dollars, and there will be 20 rounds. Each round, you will receive 10 dollars. You can choose to contribute between 0 to 10 dollars towards a common pool of dollars during each round, and whatever dollars you do not contribute are yours. Before you contribute, you will be prompted for your reasoning. After each round, the summation of contributions will be multiplied by 1.6 and divided evenly between everyone. Furthermore, at the end of each round, you will be given a summary of the total contributions towards the common pool for that round, how many dollars you received for that round, and how many dollars you have received in total across all rounds."
COLLECTIVE_SYS_PROMPT="Prioritize collective welfare. You will play a game with one other AI agent. The rules are as follows: everyone will start with 0 dollars, and there will be 20 rounds. Each round, you will receive 10 dollars. You can choose to contribute between 0 to 10 dollars towards a common pool of dollars during each round, and whatever dollars you do not contribute are yours. Before you contribute, you will be prompted for your reasoning. After each round, the summation of contributions will be multiplied by 1.6 and divided evenly between everyone. Furthermore, at the end of each round, you will be given a summary of the total contributions towards the common pool for that round, how many dollars you received for that round, and how many dollars you have received in total across all rounds."
MODEL_A="openai/gpt-4o"
MODEL_B="anthropic/claude-sonnet-4"
TEMPERATURE=1.0
MAX_TOKENS=500

#various variables

a_total=0
b_total=0
results=[]

#main

def run(a_prompt, b_prompt):
    global a_total, b_total, results
    a_total = 0
    b_total = 0
    rounds_data=[]
    print(f"\n--- Starting Game with A: {a_prompt.capitalize()}, B: {b_prompt.capitalize()} ---")
    sys_a=initialize(a_prompt)
    sys_b=initialize(b_prompt)
    a_history=[{"role": "system", "content": sys_a}]
    b_history=[{"role": "system", "content": sys_b}]
    for i in range(NUMBER_ROUNDS):
        print(f"\n--- Round {i + 1}/{NUMBER_ROUNDS} ---")
        user_content_a = (
            f"It is Round {i + 1}. You currently have {a_total} total dollars accumulated. "
            + (f"In the last round, you contributed {last_a_contribution}. "
               f"Your gain was {last_a_gain}. "
               f"The total contribution was {last_total_contribution}. "
               if i > 0 else "")
            + f"You start this round with {dollars} dollars. How many dollars (0-10) will you contribute to the public pool?"
        )
        user_content_b = (
            f"It is Round {i + 1}. You currently have {b_total} total dollars accumulated. "
            + (f"In the last round, you contributed {last_b_contribution}. "
               f"Your gain was {last_b_gain}. "
               f"The total contribution was {last_total_contribution}. "
               if i > 0 else "")
            + f"You start this round with {dollars} dollars. How many dollars (0-10) will you contribute to the public pool?"
        )
        a_history.append({"role": "user", "content": user_content_a})
        b_history.append({"role": "user", "content": user_content_b})

        a_response = call(MODEL_A, a_history)
        a_contribution = a_response["contribution"]
        a_reasoning = a_response["reasoning"]
        print(f"Model A contributed: {a_contribution} (Reasoning: {a_reasoning})")

        b_response = call(MODEL_B, b_history)
        b_contribution = b_response["contribution"]
        b_reasoning = b_response["reasoning"]
        print(f"Model B contributed: {b_contribution} (Reasoning: {b_reasoning})")

        a_gain, b_gain = payoff(a_contribution, b_contribution)
        a_total+=a_gain
        b_total+=b_gain

        print(f"Round {i + 1} Results:")
        print(f"  Total contribution this round: {a_contribution + b_contribution}")
        print(f"  Model A gained: {a_gain} dollars (Total: {a_total})")
        print(f"  Model B gained: {b_gain} dollars (Total: {b_total})")

        last_a_contribution = a_contribution
        last_b_contribution = b_contribution
        last_a_gain = a_gain
        last_b_gain = b_gain
        last_total_contribution = a_contribution + b_contribution

        a_history.append({"role": "assistant", "content": json.dumps(a_response)})
        b_history.append({"role": "assistant", "content": json.dumps(b_response)})

        outcome_a = (
            f"In Round {i + 1}, you contributed {a_contribution}. "
            f"The total contribution was {last_total_contribution}. "
            f"You gained {a_gain} dollars this round. "
            f"Your new total accumulated dollars are {a_total}. "
        )

        outcome_b = (
            f"In Round {i + 1}, you contributed {b_contribution}. "
            f"The total contribution was {last_total_contribution}. "
            f"You gained {b_gain} dollars this round. "
            f"Your new total accumulated dollars are {b_total}. "
        )
        a_history.append({"role": "user", "content": outcome_a})
        b_history.append({"role": "user", "content": outcome_b})
        
        rounds_data.append({
            "round": i + 1,
            "a_contribution": a_contribution,
            "a_reasoning": a_reasoning,
            "a_gain": a_gain,
            "a_total_dollars_after_round": a_total,
            "b_contribution": b_contribution,
            "b_reasoning": b_reasoning,
            "b_gain": b_gain,
            "b_total_dollars_after_round": b_total,
            "total_contribution_round": last_total_contribution,
        })

        results.append({
            "round": i + 1,
            "a_contribution": a_contribution,
            "a_reasoning": a_reasoning,
            "a_gain": a_gain,
            "a_total_dollars_after_round": a_total,
            "b_contribution": b_contribution,
            "b_reasoning": b_reasoning,
            "b_gain": b_gain,
            "b_total_dollars_after_round": b_total,
            "total_contribution_round": last_total_contribution,
        })
    
    print(f"\n--- Game End ---")
    print(f"Final Total dollars - Model A: {a_total}, Model B: {b_total}")

#helpers

#returns the right prompt
def initialize(prompt_name):
    prompt_name=prompt_name.lower()
    if prompt_name=="neutral":
        return NEUTRAL_SYS_PROMPT
    elif prompt_name=="self":
        return SELF_SYS_PROMPT
    elif prompt_name=="collective":
        return COLLECTIVE_SYS_PROMPT
    else:
        raise ValueError("Invalid -- please choose 'neutral', 'self', or 'collective'.")

#payoff
def payoff(a_contribution, b_contribution):
    gain = (MULTIPLIER * 0.5) * (a_contribution + b_contribution)
    a_payoff = (dollars - a_contribution) + gain
    b_payoff = (dollars - b_contribution) + gain
    return a_payoff, b_payoff

#call the models
def call(model_name, messages):
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set.")
    json_instruction = messages + [
        {"role": "user", "content": "Your response must be a JSON object with two keys: 'reasoning' (string) and 'contribution' (integer between 0 and 10)."}
    ]
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": json_instruction,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "response_format": {"type": "json_object"}
    }
    try:
        response = requests.post(
            url=OPENROUTER_API_BASE,
            headers=headers,
            data=json.dumps(payload)
        )

        response.raise_for_status()

        raw_data = response.json()

        if raw_data and raw_data.get('choices'):
            json_content_str = raw_data['choices'][0]['message']['content']
            try:
                parsed_content = json.loads(json_content_str)
                if "reasoning" in parsed_content and "contribution" in parsed_content:
                    contribution = int(parsed_content["contribution"])
                    # Ensure contribution is within 0-10 range
                    contribution = max(0, min(10, contribution))
                    return {"reasoning": parsed_content["reasoning"], "contribution": contribution}
                else:
                    print(f"Warning: Model {model_name} returned unexpected JSON format for keys: {parsed_content}. Defaulting contribution to 0.")
                    return {"reasoning": json_content_str, "contribution": 0}

            except json.JSONDecodeError:
                print(f"Error: Model {model_name} did not return valid JSON: {json_content_str}. Defaulting contribution to 0.")
                # Attempt to extract contribution even if JSON is malformed
                import re
                match = re.search(r'\"contribution\":\s*(\d+)', json_content_str)
                if match:
                    fallback_contribution = max(0, min(10, int(match.group(1))))
                    return {"reasoning": json_content_str, "contribution": fallback_contribution}
                else:
                    return {"reasoning": json_content_str, "contribution": 0}
        else:
            print(f"Error: Model {model_name} returned no choices or content: {raw_data}")
            return {"reasoning": "No response from model or empty choices.", "contribution": 0}

    except requests.exceptions.RequestException as e:
        print(f"API request error for model {model_name}: {e}")
        if e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return {"reasoning": f"API request error: {e}", "contribution": 0}
    except Exception as e:
        print(f"An unexpected error occurred during API call for model {model_name}: {e}")
        return {"reasoning": f"Unexpected error: {e}", "contribution": 0}
    
if __name__ == "__main__":
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
    else:
        run("neutral", "neutral")
        output_filename = "game_results.json"
        try:
            with open(output_filename, 'w') as f:
                json.dump(results, f, indent=4) 
            print(f"\nGame results saved to '{output_filename}'")
        except IOError as e:
            print(f"Error saving results to file: {e}")
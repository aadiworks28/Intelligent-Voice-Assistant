import subprocess

def ask_ollama(user_text):
    prompt = f"Answer concisely and clearly:\n{user_text}"

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            timeout=180
        )

        output = result.stdout.strip()
        if not output:
            return "I didn't get a response."

        return output

    except subprocess.TimeoutExpired:
        return "I'm still thinking. Please try again."

    except Exception as e:
        print("Ollama error:", e)
        return "I'm having trouble thinking right now."


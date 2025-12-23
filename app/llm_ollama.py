import subprocess

def ask_ollama(prompt):
    prompt = f"Answer concisely and clearly:\n{prompt}"

    try:
        process = subprocess.Popen(
            ["ollama", "run", "mistral", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        full_response = ""

        for line in process.stdout:
            line = line.strip()
            if not line:
                continue

            full_response += line + " "
            print(line, end=" ", flush=True)

        process.wait()

        if not full_response.strip():
            return "I didn't get a response."

        return full_response.strip()

    except Exception as e:
        print("Ollama streaming error:", e)
        return "I'm having trouble thinking right now."


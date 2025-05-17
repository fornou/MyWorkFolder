import ollama

client = ollama.Client()

prompt = "Parlami di chi sei cosa fai e perchè sei così famoso"
response = client.generate(model="super_mario", prompt=prompt)

print(response['response'])

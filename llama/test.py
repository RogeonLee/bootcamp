from llama_cpp import Llama

llm = Llama(
    model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    n_gpu_layers=-1,
    verbose=False
)

response = llm.create_chat_completion(
    messages=[
        {"role": "user", "content": "Hello! Please introduce yourself in English."}
    ],
    max_tokens=200
)

print(response["choices"][0]["message"]["content"])

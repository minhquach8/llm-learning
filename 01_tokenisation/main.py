import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

text = "Hello world! This is a test."
tokens = encoder.encode(text)

print("Tokens:", tokens)
# Result: Tokens: [13225, 2375, 0, 1328, 382, 261, 1746, 13]

# decoder = encoder.decode(tokens)
decoder = encoder.decode([13225, 2375, 0, 1328, 382, 261, 1746, 13])
print("Decoded:", decoder)

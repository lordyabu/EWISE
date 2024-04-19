import torch
import torch.nn as nn
from torch.nn import functional as F
from gpt import GPTLanguageModel


with open('journal_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# here are all the unique characters that occur in this text
chars = sorted(set(text) | {'<start>', '<end>'})
vocab_size = len(chars)
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}
encode = lambda s: [stoi['<start>']] + [stoi[c] for c in s] + [stoi['<end>']]
decode = lambda l: ''.join(itos[i] for i in l)

# Load the model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = GPTLanguageModel().to(device)
checkpoint = torch.load('gpt_model_and_optimizer_v3.pth', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Helper function to decode generated tokens back to text
def decode(token_ids):
    # Assuming `itos` (index to string) is defined globally or passed here
    return ''.join([itos[i] for i in token_ids])

# Configuration
max_tokens_list = [10000]  # Different max tokens to generate

# Generate text with different max token values
for max_tokens in max_tokens_list:
    context = torch.tensor([[stoi['<start>']]], dtype=torch.long, device=device)  # Assuming a start token
    generated_ids = model.generate(context, max_new_tokens=max_tokens)[0].tolist()
    generated_text = decode(generated_ids)

    print(f"Generated with {max_tokens} tokens:")
    print(generated_text)
    print("\n" + "="*80 + "\n")

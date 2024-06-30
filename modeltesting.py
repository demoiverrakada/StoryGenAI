from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the fine-tuned model and tokenizer
model = GPT2LMHeadModel.from_pretrained('./results')
tokenizer = GPT2Tokenizer.from_pretrained('./results')

def generate_story(prompt, max_length=200, temperature=0.7, top_k=50):
    # Tokenize the input prompt
    input_ids = tokenizer(prompt, return_tensors='pt').input_ids
    
    # Generate text based on the prompt
    generated = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
        pad_token_id=tokenizer.eos_token_id  # Ensure generated text ends properly
    )
    
    # Decode the generated output
    generated_text = tokenizer.decode(generated[0], skip_special_tokens=True)
    return generated_text

# Example prompt or title
prompt = ""

# Generate story
generated_story = generate_story(prompt)
print(generated_story)

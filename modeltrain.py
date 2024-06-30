from transformers import GPT2Tokenizer, GPT2LMHeadModel, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from datasets import Dataset
import os
import torch

# Step 1: Initialize Tokenizer with Padding Token
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})  # Add padding token to tokenizer

# Initialize GPT-2 model and resize embeddings to include new tokens
model = GPT2LMHeadModel.from_pretrained('gpt2')
model.resize_token_embeddings(len(tokenizer))

# Specify the folder containing your text files
folder_path = '/kaggle/working/stories/dirty_talk'  # Replace with your folder path

# Get all .txt files in the folder
story_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

# Load and tokenize each story
stories = []
for file in story_files:
    with open(file, 'r', encoding='utf-8') as f:
        story = f.read()
        stories.append(story)

# Tokenize the stories
tokenized_stories = tokenizer(stories, truncation=True, padding=True, return_tensors='pt')

# Convert to Hugging Face Dataset
dataset = Dataset.from_dict({
    'input_ids': tokenized_stories['input_ids'],
    'attention_mask': tokenized_stories['attention_mask']
})

# Step 3: Fine-Tuning Process

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    per_device_train_batch_size=2,   # batch size for training
    num_train_epochs=3,              # number of training epochs
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    save_strategy="epoch"            # Save model every epoch
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
)

# Step 4: Training
trainer.train()

# Step 5: Save the fine-tuned model
model.save_pretrained('./results')
tokenizer.save_pretrained('./results')

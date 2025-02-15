import os
from transformers import GPTNeoForCausalLM, AutoTokenizer
import torch
import random

# Load the pre-trained GPT-Neo model and tokenizer from Hugging Face
model_name = "EleutherAI/gpt-neo-2.7B"  # You can change this to a smaller model like GPT-2 for faster local testing
model = GPTNeoForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Move the model to GPU (optional, for speed)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Function to generate a short sentence given a prompt
def generate_story(prompt, min_length=50, max_length=200, temperature=1.0, top_k=50, top_p=0.9, repetition_penalty=1.2):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    
    # Generate text with dynamic parameters
    output = model.generate(
        input_ids,
        min_length=min_length,     # Minimum number of tokens (very short for testing)
        max_length=max_length,     # Maximum number of tokens (short sentence)
        do_sample=True,            # Enable sampling for varied responses
        temperature=temperature,   # Controls randomness
        top_k=top_k,               # Limits to top-k most probable tokens
        top_p=top_p,               # Nucleus sampling for diverse token choices
        repetition_penalty=repetition_penalty  # Apply penalty for repeated tokens
    )
    
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Function to save the generated text (for testing purposes, this may not be needed)
def save_story(story, food_name, story_count):
    # Create directory for the food if it doesn't exist
    os.makedirs(f"generated_stories/{food_name}", exist_ok=True)
    
    # Save the story in a numbered file under the food's directory
    with open(f"generated_stories/{food_name}/story_{story_count}.txt", "w") as file:
        file.write(story)

# List of foods for testing
food_list = ["lemon meringue pie", "chocolate chip cookies"]
num_stories_per_food = 2  # Generate 2 short sentences per food for testing

# Prompt templates for generating stories
prompt_template_variations = [
    "The first time I made {food}...",
    "I'll never forget the time I tried to make {food}...",
]

# Main loop: Generate short sentences for each food in the list with dynamic prompts and sampling
for food in food_list:
    story_count = 0
    while story_count < num_stories_per_food:
        # Select a random prompt variation
        prompt = random.choice(prompt_template_variations).format(food=food)
        
        # Dynamically adjust sampling parameters for variety
        temperature = random.uniform(0.7, 1.2)  # Random temperature between 0.7 and 1.2
        top_k = random.choice([30, 50, 100])    # Random top_k from 30, 50, or 100
        top_p = random.uniform(0.8, 1.0)        # Random top_p between 0.8 and 1.0
        repetition_penalty = random.uniform(1.1, 1.3)  # Random repetition penalty between 1.1 and 1.3
        
        # Generate a new short story (sentence) for the current food with dynamic sampling
        story = generate_story(
            prompt, 
            temperature=temperature, 
            top_k=top_k, 
            top_p=top_p, 
            repetition_penalty=repetition_penalty
        )
        
        # Save the story (optional for testing)
        save_story(story, food, story_count + 1)
        
        # Update the count of stories generated
        story_count += 1
        print(f"Generated and saved story {story_count} for {food} (temp={temperature}, top_k={top_k}, top_p={top_p}, penalty={repetition_penalty})")
        
print("Short sentence generation completed for testing.")

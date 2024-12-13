from transformers import T5Tokenizer, T5ForConditionalGeneration

# Define the path to your saved model directory
model_path = "./T5_QA/model"
tokenizer_path = "./T5_QA/tokenizer"

# Load the tokenizer and model
tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

def generate_flashcard(context):

    # Test the model with an input
    inputs = tokenizer(context, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=128)

    q_a = tokenizer.decode(outputs[0], skip_special_tokens=False)
    q_a = q_a.replace(tokenizer.pad_token, "").replace(tokenizer.eos_token, "")

    question, answer = q_a.split(tokenizer.sep_token)

    return print("question:", question), print("answer:", answer)

if __name__ == "__main__":
    text = "Barry lives in tripoli, which is the capital of Libya. The neighbourhood in which he lives is called 'Hay demashq'."
    generate_flashcard(text)

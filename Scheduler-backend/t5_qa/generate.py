from transformers import T5ForConditionalGeneration, T5Tokenizer

def generate_qa(context):
    """
    Generates Q&A pairs from a given context using the fine-tuned T5 model.

    Args:
        context (str): Input context text.

    Returns:
        tuple: (question, answer)
    """
    model = T5ForConditionalGeneration.from_pretrained("./trained_model")
    tokenizer = T5Tokenizer.from_pretrained("./trained_model")

    input_text = "context: " + context
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    # Generate outputs
    output_ids = model.generate(input_ids, max_length=128, num_return_sequences=1)
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Split question and answer
    question, answer = output.split(" <sep> ")
    return question, answer


if __name__ == "__main__":
    context = "The Eiffel Tower is one of the most famous landmarks in Paris."
    question, answer = generate_qa(context)
    print("Generated Question:", question)
    print("Generated Answer:", answer)

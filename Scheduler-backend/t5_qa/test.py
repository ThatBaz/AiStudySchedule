import torch

def test(model, tokenizer, device):
    model.to(device)
    model.eval()

    # Example context
    context = "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889 as the entrance arch to the 1889 World's Fair, it was initially criticized by some of France's leading artists and intellectuals for its design, but it has become a global cultural icon of France and one of the most recognizable structures in the world."

    # Prepare input
    input_text = f"context: {context}"
    inputs = tokenizer.encode_plus(input_text, return_tensors="pt", max_length=512, truncation=True)
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    # Generate multiple QA pairs
    num_pairs = 3
    for _ in range(num_pairs):
        with torch.no_grad():
            outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=64, num_return_sequences=1)

        decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        question, answer = decoded_output.split("<sep>")
        print(f"Generated Q&A pair:")
        print(f"Question: {question.strip()}")
        print(f"Answer: {answer.strip()}")
        print()


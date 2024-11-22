from transformers import T5ForConditionalGeneration, T5Tokenizer
from preprocess import preprocess_dataset
from torch.utils.data import DataLoader
import torch

batch_size = 8  # Use the same batch size as during training


def evaluate_model():
    """
    Evaluates the fine-tuned T5 model on the validation dataset.
    """
    _, valid_data, _ = preprocess_dataset()
    valid_dataloader = DataLoader(valid_data, batch_size=batch_size)

    # Load the fine-tuned model and tokenizer
    model = T5ForConditionalGeneration.from_pretrained("./fine_tuned_model")
    tokenizer = T5Tokenizer.from_pretrained("./fine_tuned_model")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Run validation
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in valid_dataloader:
            input_ids = torch.tensor(batch["input_ids"]).to(device)
            attention_mask = torch.tensor(batch["attention_mask"]).to(device)
            labels = torch.tensor(batch["labels"]).to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            total_loss += outputs.loss.item()

    print(f"Validation Loss: {total_loss / len(valid_dataloader):.4f}")


if __name__ == "__main__":
    evaluate_model()

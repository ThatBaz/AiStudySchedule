from transformers import T5ForConditionalGeneration, AdamW
from torch.utils.data import DataLoader
import torch
from preprocess import preprocess_dataset

# Properties
lr0 = 5e-5          # Learning rate
batch_size = 8      # Number of samples processed per batch
num_workers = 0     # Number of subprocesses for data loading
num_epochs = 10     # Number of passes through the training dataset
valid_step = 5000   # Steps between validation checks


def train_model():
    """
    Trains the T5 model on the SQuAD dataset.
    """
    # Load preprocessed data and tokenizer
    train_data, valid_data, tokenizer = preprocess_dataset()

    # Convert datasets to DataLoader for batch processing
    train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    valid_dataloader = DataLoader(valid_data, batch_size=batch_size, num_workers=num_workers)

    # Load the pre-trained T5 model
    model = T5ForConditionalGeneration.from_pretrained("t5-large")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Extend model's vocabulary if necessary
    if "<sep>" not in tokenizer.get_vocab():
        tokenizer.add_tokens(["<sep>"])
        model.resize_token_embeddings(len(tokenizer))

    # Set up optimizer
    optimizer = AdamW(model.parameters(), lr=lr0)

    # Training loop
    step = 0
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in train_dataloader:
            step += 1
            # Prepare batch data
            input_ids = torch.tensor(batch["input_ids"]).to(device)
            attention_mask = torch.tensor(batch["attention_mask"]).to(device)
            labels = torch.tensor(batch["labels"]).to(device)

            # Forward pass
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss

            # Backward pass
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            total_loss += loss.item()

            # Validation step
            if step % valid_step == 0:
                validate_model(model, valid_dataloader, device)

        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(train_dataloader):.4f}")

    # Save the fine-tuned model
    model.save_pretrained("./fine_tuned_model")
    tokenizer.save_pretrained("./fine_tuned_model")


def validate_model(model, dataloader, device):
    """
    Runs validation on the validation dataset.
    """
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for batch in dataloader:
            input_ids = torch.tensor(batch["input_ids"]).to(device)
            attention_mask = torch.tensor(batch["attention_mask"]).to(device)
            labels = torch.tensor(batch["labels"]).to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            total_loss += outputs.loss.item()

    print(f"Validation Loss: {total_loss / len(dataloader):.4f}")


if __name__ == "__main__":
    train_model()

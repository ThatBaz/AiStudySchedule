import torch
from tqdm import tqdm
from torch.utils.data import DataLoader

def evaluate(model, val_dataset, device, batch_size=8):
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    model.to(device)
    model.eval()

    total_loss = 0
    with torch.no_grad():
        for batch in tqdm(val_loader, desc="Evaluating"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask, labels=labels)
            loss = outputs.loss
            total_loss += loss.item()

    avg_loss = total_loss / len(val_loader)
    print(f"Final Evaluation Loss: {avg_loss:.4f}")
    return avg_loss


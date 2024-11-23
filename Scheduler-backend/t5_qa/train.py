import json
import os
import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
from tqdm import tqdm
from validate import validate

def train(model, train_dataset, val_dataset, tokenizer, device, num_epochs=10, batch_size=1, lr=5e-5, valid_step=5000):
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    optimizer = AdamW(model.parameters(), lr=lr)
    total_steps = len(train_loader) * num_epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

    model.to(device)
    model.train()

    global_step = 0
    best_val_loss = float('inf')

    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")
        for batch in tqdm(train_loader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask, labels=labels)
            loss = outputs.loss

            loss.backward()
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

            global_step += 1

            if global_step % valid_step == 0:
                val_loss = validate(model, val_loader, device)
                print(f"Step {global_step}: Validation Loss: {val_loss:.4f}")

                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    torch.save(model.state_dict(), 'best_model.pth')
                    print(f"New best model saved with validation loss: {best_val_loss:.4f}")

                model.train()
    # Save the final model and tokenizer
    print("Saving the final model and tokenizer...")
    save_custom_model(model, tokenizer, 'trained_t5_qa')
    print("Final model and tokenizer saved in 'trained_t5_qa' directory")

    print("Training completed!")

def save_custom_model(model, tokenizer, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Save the custom model
    torch.save(model.state_dict(), os.path.join(save_dir, 'pytorch_model.bin'))
    
    # Save the T5 config
    model.t5_model.config.save_pretrained(save_dir)
    
    # Save the tokenizer
    tokenizer.save_pretrained(save_dir)

    # Save a custom config file to indicate this is a QAModel
    with open(os.path.join(save_dir, 'qa_model_config.json'), 'w') as f:
        json.dump({"model_type": "QAModel"}, f)

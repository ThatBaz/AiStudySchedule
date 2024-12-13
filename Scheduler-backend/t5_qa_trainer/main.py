import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from datasets import load_dataset
from model import QAModel
from dataset import preprocess
from train import train
from evaluate import evaluate
from test import test

def main():
    # Load the dataset
    squad_dataset = load_dataset("rajpurkar/squad")

    # Initialize the tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    model = T5ForConditionalGeneration.from_pretrained("t5-large")

    # Wrap the model in our custom QAModel
    qa_model = QAModel(model)

    # Create datasets
    train_dataset = preprocess(squad_dataset['train'], tokenizer)
    val_dataset = preprocess(squad_dataset['validation'], tokenizer)

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Train the model
    train(qa_model, train_dataset, val_dataset, tokenizer, device)

    # Evaluate the model
    evaluate(qa_model, val_dataset, device)

    # Test the model
    test(qa_model, tokenizer, device)

if __name__ == "__main__":
    main()


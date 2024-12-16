import torch
from torch.utils.data import Dataset

class PreprocessDataset(Dataset):
    """
    Custom dataset class for preprocessing data for T5 model training.
    
    Args:
        dataset (list): List of dictionaries containing context, question, and answers.
        tokenizer (transformers.Tokenizer): Tokenizer object for encoding texts.
        max_length (int): Maximum length of input sequences. Defaults to 512.
    """

    def __init__(self, dataset, tokenizer, max_length=512):
        self.dataset = dataset
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        """Return the number of samples in the dataset."""
        return len(self.dataset)

    def __getitem__(self, idx):
        """
        Get a single sample from the dataset.

        Args:
            idx (int): Index of the sample.

        Returns:
            dict: Dictionary containing 'input_ids', 'attention_mask', and 'labels'.
        """
        item = self.dataset[idx]
        context = item['context']
        question = item['question']
        answer = item['answers']['text'][0]

        # Combine context and question into input_text
        input_text = f"context: {context} question: {question}"

        # Prepare target_text with question and answer separated by <sep>
        target_text = f"{question} <sep> {answer}"

        # Encode input_text
        inputs = self.tokenizer.encode_plus(
            input_text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        # Encode target_text
        targets = self.tokenizer.encode_plus(
            target_text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        # Return processed data as dictionary
        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': targets['input_ids'].squeeze()
        }

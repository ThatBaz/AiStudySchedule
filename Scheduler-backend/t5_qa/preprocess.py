from transformers import T5Tokenizer
from datasets import load_dataset

# Properties
max_length = 512  # Maximum token length for input/output sequences

def preprocess_dataset():
    """
    Preprocesses the SQuAD dataset for training and validation. Converts context, 
    question, and answer into tokenized inputs and targets for the T5 model.

    Returns:
        train_data (Dataset): Preprocessed training dataset.
        valid_data (Dataset): Preprocessed validation dataset.
        tokenizer (T5Tokenizer): Tokenizer used for T5.
    """
    # Load the SQuAD dataset
    squad = load_dataset("rajpurkar/squad")

    # Preprocessing function
    def preprocess_function(examples):
        """
        Prepares the input-output pairs for the T5 model.
        Input: "context: [context]"
        Target: "[question] <sep> [answer]"
        """
        inputs = "context: " + examples["context"]
        if len(examples["answers"]["text"]) > 0:
            targets = examples["question"] + " <sep> " + examples["answers"]["text"][0]
        else:
            targets = ""
        return {"input_text": inputs, "target_text": targets}

    # Apply preprocessing to datasets
    train_data = squad["train"].map(preprocess_function, remove_columns=squad["train"].column_names)
    valid_data = squad["validation"].map(preprocess_function, remove_columns=squad["validation"].column_names)

    # Load and extend the tokenizer
    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    if "<sep>" not in tokenizer.get_vocab():
        tokenizer.add_tokens(["<sep>"])

    # Tokenization function
    def tokenize_function(examples):
        """
        Tokenizes the input and target texts for the T5 model.
        """
        model_inputs = tokenizer(
            examples["input_text"], max_length=max_length, truncation=True, padding="max_length"
        )
        labels = tokenizer(
            examples["target_text"], max_length=max_length, truncation=True, padding="max_length"
        )
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    # Tokenize the datasets
    train_data = train_data.map(tokenize_function, batched=True)
    valid_data = valid_data.map(tokenize_function, batched=True)

    return train_data, valid_data, tokenizer

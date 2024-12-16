import torch
import torch.nn as nn

class QAModel(nn.Module):
    """
    A custom PyTorch module for Question Answering using a T5 model.

    This class wraps a T5 model and provides methods for both forward pass and generation.
    """
    def __init__(self, t5_model):
        """
        Initialize the QAModel with a pre-trained T5 model.

        Args:
            t5_model (transformers.T5ForConditionalGeneration): Pre-trained T5 model.
        """
        super(QAModel, self).__init__()
        self.t5_model = t5_model

    def forward(self, input_ids, attention_mask, labels=None):
        """
        Forward pass through the T5 model.

        Args:
            input_ids (torch.Tensor): Input token IDs.
            attention_mask (torch.Tensor): Attention mask.
            labels (torch.Tensor, optional): Target labels. Defaults to None.

        Returns:
            torch.nn.utils.rnn.PackedSequence: Packed sequence output from T5 model.
        """
        outputs = self.t5_model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        return outputs

    def generate(self, input_ids, attention_mask, **kwargs):
        """
        Generate text using the T5 model.

        Args:
            input_ids (torch.Tensor): Input token IDs.
            attention_mask (torch.Tensor): Attention mask.
            **kwargs: Additional keyword arguments passed to the T5 model's generate method.

        Returns:
            torch.Tensor: Generated text tokens.
        """
        return self.t5_model.generate(input_ids=input_ids, attention_mask=attention_mask, **kwargs)

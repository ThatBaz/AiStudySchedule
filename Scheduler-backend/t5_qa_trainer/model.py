import torch
import torch.nn as nn

class QAModel(nn.Module):
    def __init__(self, t5_model):
        super(QAModel, self).__init__()
        self.t5_model = t5_model

    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.t5_model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        return outputs

    def generate(self, input_ids, attention_mask, **kwargs):
        return self.t5_model.generate(input_ids=input_ids, attention_mask=attention_mask, **kwargs)


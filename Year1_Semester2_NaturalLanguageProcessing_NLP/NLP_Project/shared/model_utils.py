import torch
import torch.nn as nn
from transformers import AutoModel

class SBERTClassifier(nn.Module):
    def __init__(self, model_name, num_classes=2, freeze_encoder=True):
        super(SBERTClassifier, self).__init__()
        self.encoder = AutoModel.from_pretrained(model_name)
        
        if freeze_encoder:
            for param in self.encoder.parameters():
                param.requires_grad = False
        else:
            for param in self.encoder.parameters():
                param.requires_grad = True
                
        hidden_size = self.encoder.config.hidden_size
        
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, input_ids, attention_mask):
        # Mean pooling
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        token_embeddings = outputs.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        pooled_output = sum_embeddings / sum_mask
        
        logits = self.classifier(pooled_output)
        return logits

def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

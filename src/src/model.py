import torch
import torch.nn as nn
import torchvision.models as models

class DeepGuardModel(nn.Module):
    def __init__(self, hidden_dim=256, num_layers=2, num_classes=2):
        super(DeepGuardModel, self).__init__()
        
        backbone = models.efficientnet_b0(pretrained=True)
        self.feature_extractor = nn.Sequential(*list(backbone.children())[:-1])
        
        for param in self.feature_extractor.parameters():
            param.requires_grad = False
            
        self.lstm = nn.LSTM(input_size=1280, hidden_size=hidden_dim, 
                            num_layers=num_layers, batch_first=True)
        
        self.fc = nn.Linear(hidden_dim, num_classes)
        
    def forward(self, x):
        batch_size, seq_len, c, h, w = x.size()
        
        x = x.view(batch_size * seq_len, c, h, w)
        features = self.feature_extractor(x)
        features = features.view(batch_size, seq_len, -1)
        
        lstm_out, _ = self.lstm(features)
        
        out = self.fc(lstm_out[:, -1, :])
        return out

if __name__ == "__main__":
    model = DeepGuardModel()
    dummy_input = torch.randn(2, 5, 3, 224, 224)
    output = model(dummy_input)
    print(f"[DeepGuard Model] Structural Test Complete. Output Shape: {output.shape}")

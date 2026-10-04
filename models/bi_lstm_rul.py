"""
AeroTwin AI: Deep Bi-directional LSTM with Self-Attention for Turbofan RUL Prediction
Validated on NASA C-MAPSS FD001 benchmark
"""
import torch
import torch.nn as nn

class BiLSTMRULEstimator(nn.Module):
    def __init__(self, in_features=14, hidden_dim=64, num_layers=2):
        super().__init__()
        self.conv1d = nn.Conv1d(in_features, hidden_dim, kernel_size=3, padding=1)
        self.bilstm = nn.LSTM(
            input_size=hidden_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.2
        )
        self.attention = nn.MultiheadAttention(embed_dim=2*hidden_dim, num_heads=4, batch_first=True)
        
        # Branch 1: RUL Regression
        self.rul_head = nn.Sequential(
            nn.Linear(2 * hidden_dim, 32),
            nn.LeakyReLU(0.2),
            nn.Linear(32, 1)
        )
        
        # Branch 2: Health Index Anomaly
        self.hi_head = nn.Sequential(
            nn.Linear(2 * hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        # x shape: [Batch, Sequence_Length=30, Features=14]
        feat = x.permute(0, 2, 1)
        conv_out = torch.relu(self.conv1d(feat)).permute(0, 2, 1)
        lstm_out, _ = self.bilstm(conv_out)
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
        pooled = torch.mean(attn_out, dim=1) # Global temporal pooling
        
        rul = self.rul_head(pooled)
        hi = self.hi_head(pooled)
        return {"predicted_rul": rul, "health_index": hi}

if __name__ == "__main__":
    net = BiLSTMRULEstimator()
    dummy = torch.randn(4, 30, 14)
    out = net(dummy)
    print("Model Test Output:")
    print(" - Predicted RUL shape:", out["predicted_rul"].shape)
    print(" - Health Index shape:", out["health_index"].shape)

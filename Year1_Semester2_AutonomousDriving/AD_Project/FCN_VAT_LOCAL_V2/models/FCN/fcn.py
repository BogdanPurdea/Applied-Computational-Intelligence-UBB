import torch
import torch.nn as nn

class ProjectionBlock(nn.Module):
    def __init__(self, in_f: int, out_f: int, dropout: float):
        super().__init__()
        self.main = nn.Sequential(
            nn.Linear(in_f, out_f, bias=False),
            nn.BatchNorm1d(out_f),
            nn.GELU(),
            nn.Dropout(p=dropout),
        )
        self.skip = nn.Linear(in_f, out_f, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.main(x) + self.skip(x)

class ResidualFCBlock(nn.Module):
    def __init__(self, features: int, dropout: float):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(features, features, bias=False),
            nn.BatchNorm1d(features),
            nn.GELU(),
            nn.Dropout(p=dropout),
            nn.Linear(features, features, bias=False),
            nn.BatchNorm1d(features),
        )
        self.act = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.act(x + self.net(x))

class FCN(nn.Module):
    def __init__(self, in_features: int = 3 * 48 * 48, num_classes: int = 43, dropout: float = 0.4):
        super().__init__()
        self.flatten = nn.Flatten()
        self.proj1 = ProjectionBlock(in_features, 1024, dropout=dropout)
        self.proj2 = ProjectionBlock(1024, 512, dropout=dropout * 0.80)
        self.res1  = ResidualFCBlock(512, dropout=dropout * 0.60)
        self.res2  = ResidualFCBlock(512, dropout=dropout * 0.60)
        self.proj3 = ProjectionBlock(512, 256, dropout=dropout * 0.50)
        self.classifier = nn.Linear(256, num_classes)
        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.flatten(x)
        x = self.proj1(x)
        x = self.proj2(x)
        x = self.res1(x)
        x = self.res2(x)
        x = self.proj3(x)
        return self.classifier(x)

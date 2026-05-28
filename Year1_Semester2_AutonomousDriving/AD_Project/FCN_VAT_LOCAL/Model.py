# =============================================================================
# GTSRB FCN — Step 1: Model Architecture (Improved)
# =============================================================================

import torch
import torch.nn as nn


# ─── HYPERPARAMETERS ──────────────────────────────────────────────────────────
IMG_SIZE    = 48
IN_FEATURES = 3 * IMG_SIZE * IMG_SIZE   # 6 912
NUM_CLASSES = 43
DROPOUT_P   = 0.4


# ─── BUILDING BLOCKS ──────────────────────────────────────────────────────────
class ProjectionBlock(nn.Module):
    """Downsampling block (in_f → out_f) with a 1-D skip projection.

    Linear (no bias) → BN → GELU → Dropout
    skip: Linear (no bias)   [1×1 projection shortcut]
    out = main(x) + skip(x)
    """
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
    """Same-dimension residual block.

    Two FC sub-layers with BN + GELU; final activation after skip addition.
    in_f == out_f enforced by design (no projection needed on skip path).
    """
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


# ─── FCN MODEL ────────────────────────────────────────────────────────────────
class FCN(nn.Module):
    def __init__(
        self,
        in_features: int = IN_FEATURES,
        num_classes: int = NUM_CLASSES,
        dropout: float   = DROPOUT_P,
    ):
        super().__init__()

        self.flatten = nn.Flatten()   # (B,3,48,48) → (B,6912)

        # ── Projection blocks: change dimension, residual via skip projection
        self.proj1 = ProjectionBlock(in_features, 1024, dropout=dropout)          # 6912→1024
        self.proj2 = ProjectionBlock(1024,          512, dropout=dropout * 0.80)  # 1024→512

        # ── Residual blocks: refine at fixed width (gradient highway)
        self.res1  = ResidualFCBlock(512, dropout=dropout * 0.60)
        self.res2  = ResidualFCBlock(512, dropout=dropout * 0.60)

        # ── Final projection
        self.proj3 = ProjectionBlock(512, 256, dropout=dropout * 0.50)            # 512→256

        self.classifier = nn.Linear(256, num_classes)   # raw logits

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
        x = self.flatten(x)        # → (B, 6912)
        x = self.proj1(x)          # → (B, 1024)
        x = self.proj2(x)          # → (B,  512)
        x = self.res1(x)           # → (B,  512)  residual refinement
        x = self.res2(x)           # → (B,  512)  residual refinement
        x = self.proj3(x)          # → (B,  256)
        return self.classifier(x)  # → (B,   43)


# ─── INSPECTION ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    model = FCN()

    # Layer-by-layer param count
    blocks = [
        ("Flatten",    model.flatten),
        ("Proj 1",     model.proj1),
        ("Proj 2",     model.proj2),
        ("Res 1",      model.res1),
        ("Res 2",      model.res2),
        ("Proj 3",     model.proj3),
        ("Classifier", model.classifier),
    ]

    print("=" * 55)
    print(f"  {'Layer':<20} {'Out features':>15} {'Params':>12}")
    print("=" * 55)
    out_sizes = [6912, 1024, 512, 512, 512, 256, 43]
    for (name, mod), out in zip(blocks, out_sizes):
        p = sum(x.numel() for x in mod.parameters())
        print(f"  {name:<20} {out:>15,} {p:>12,}")

    total = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print("=" * 55)
    print(f"  {'TOTAL':.<20} {'':>15} {total:>12,}")
    print("=" * 55)

    # Smoke test — single forward pass
    batch  = torch.randn(8, 3, IMG_SIZE, IMG_SIZE)
    logits = model(batch)
    assert logits.shape == (8, NUM_CLASSES)
    print(f"\n✓ Forward pass OK")
    print(f"  Input  : {tuple(batch.shape)}")
    print(f"  Output : {tuple(logits.shape)}  (raw logits, 43 classes)")
    print(f"  Predicted classes: {logits.argmax(1).tolist()}")
"""
Auto-retrain script for IndoBERT model only
This script is called by retrain_service.py for automated retraining
"""

import sys
import io
from pathlib import Path

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Add Model IndoBERT to path
MODEL_DIR = Path(__file__).resolve().parents[2]
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))

from src.modeling.train import train_indobert, BertParams
from src.dataset import build_and_save_splits
import pandas as pd


def main():
    """
    Run IndoBERT training only (skip FastText for auto-retrain)
    """
    import torch

    print("=" * 80)
    print("AUTO-RETRAIN: IndoBERT Model Training")
    print("=" * 80)

    # Display system info with DirectML support
    print(f"\nSystem Information:")
    print(f"  - Python: {sys.version.split()[0]}")
    print(f"  - PyTorch: {torch.__version__}")

    # Check DirectML first
    directml_available = False
    try:
        import torch_directml

        directml_available = torch_directml.is_available()
        if directml_available:
            print(f"  - DirectML available: Yes")
            print(f"  - DirectML device: {torch_directml.device()}")
    except ImportError:
        pass

    # Check CUDA
    print(f"  - CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  - CUDA version: {torch.version.cuda}")
        print(f"  - GPU: {torch.cuda.get_device_name(0)}")

    # Final device selection
    if directml_available:
        print(f"  - Training device: DirectML GPU (optimized for Windows)")
    elif torch.cuda.is_available():
        print(f"  - Training device: CUDA GPU")
    else:
        print(f"  - Training device: CPU (training will take longer)")

    # Build dataset splits
    print("\n[1] Building dataset splits from feedback...")
    paths = build_and_save_splits()

    train_df = pd.read_csv(paths["train"])
    val_df = pd.read_csv(paths["val"])
    test_df = pd.read_csv(paths["test"])

    print(f"    - Train: {len(train_df)} samples")
    print(f"    - Val: {len(val_df)} samples")
    print(f"    - Test: {len(test_df)} samples")

    # Train IndoBERT with default params
    print("\n[2] Training IndoBERT model...")
    print("    This may take 10-30 minutes depending on data size...")

    params = BertParams()  # Use default parameters
    results = train_indobert(train_df, val_df, test_df, params=params)

    # Extract metrics
    test_metrics = results.get("test", {})

    print("\n[3] Training completed!")
    print(
        f"    - Accuracy:  {test_metrics.get('eval_accuracy', test_metrics.get('accuracy', 0)):.4f}"
    )
    print(
        f"    - Precision: {test_metrics.get('eval_precision', test_metrics.get('precision', 0)):.4f}"
    )
    print(
        f"    - Recall:    {test_metrics.get('eval_recall', test_metrics.get('recall', 0)):.4f}"
    )
    print(
        f"    - F1-Score:  {test_metrics.get('eval_f1', test_metrics.get('f1', 0)):.4f}"
    )

    print("\n" + "=" * 80)
    print("SUCCESS: AUTO-RETRAIN COMPLETED")
    print("=" * 80)

    return results


if __name__ == "__main__":
    try:
        result = main()
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)

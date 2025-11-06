import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.classifier import DocumentClassifier


def main():
    c = DocumentClassifier()
    vec = c.vectorizer
    # Determine actual input dimension
    vocab = getattr(vec, 'vocabulary_', None)
    if vocab:
        input_dim = len(vocab)
    else:
        input_dim = getattr(vec, 'max_features', None)

    hidden = getattr(c.model, 'hidden_layer_sizes', None)
    output_dim = len(c.label_encoder)

    print(f"Input features (vectorizer vocabulary size): {input_dim}")
    print(f"Hidden layers (nodes per layer): {hidden}")
    print(f"Output nodes (number of classes): {output_dim}")


if __name__ == '__main__':
    main()

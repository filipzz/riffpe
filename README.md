# Riffpe - a Riffle-Shuffle-based Format Preserving Encryption


## Requirements

[TBD]

## Installation

To install developement version from source issue:

```bash
pip install -e .
```

## Usage

As a standalone module:

Message encryption:

```python
python -m riffpe -n 100 -e 11 10 12 3
```

Message decryption:

```python
python -m riffpe -n 100 -d 26 30 13 67
```

## Testing

[TBD]

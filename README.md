# riffpe

## Install

- create virtual environment: ```python3 -m venv virt```
- activate: ```source virt/bin/activate```
- add requirements: ```pip -r requirements.txt```

## Usage

Encrypt message

```python
python -m riffpe -n 100 -e 11 10 12 3
```

Decrypt

```python
python -m riffpe -n 100 -d 26 30 13 67
```

## Testing

```bash
python -m pytest
```

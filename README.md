# Hartinator
## Use
- Step 1: Clone repository
- Step 2: `pip3 install RandomWords`
- Step 3: Go to the bottom of the file and create a PartWriter object, instantiated with a key and chord progression; (example)
```python
PartWriterImpl = PartWriter("C", "I IV vi V I IV V I ii IV V vii vi IV ii V I IV vi IV vii vi V I") 
PartWriterImpl.main()
```
- Step 4: `python3 hartinator.py`
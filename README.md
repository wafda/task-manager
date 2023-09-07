# Run
python -m uvicorn main:app --reload

# Test
python -m pytest main.py

# build docker image
```
docker image build -t python:0.0.1 (insert the directory here)
```

# run docker
docker run python:0.0.1
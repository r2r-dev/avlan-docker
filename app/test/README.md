### Network simulator and engine testing
```
pip install -r requirements.txt
python src/utils/simulator -c test/output.json &
python -m src/utils/crawler crawl --input=test/input.json --output=test/output2.json
```

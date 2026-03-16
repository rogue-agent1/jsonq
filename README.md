# jsonq
jq-like JSON query tool for the command line.
```bash
echo '{"a":{"b":1}}' | python jsonq.py .a.b
cat data.json | python jsonq.py ".users[0].name" -r
cat data.json | python jsonq.py ".items[*]" --length
python jsonq.py -f config.json ".database" --keys
```
## Zero dependencies. Python 3.6+.

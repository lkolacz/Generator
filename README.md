# Abstraction

Generate unique 8-character alphanumeric humanreadable ID in deterministic order.
Example: C33QM6S1

## Setup
To set this up run following commands:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

## Unit Tests
To run the tests type the command:

```
$ python -m pytest
```

## Debug
```
>>> from generator.generation import generate_bulk, generate
>>> generate_bulk(10)
['0004GS9X', '0004GS9Y', '0004GS9Z', '0004GSA0', '0004GSA1', '0004GSA2', '0004GSA3', '0004GSA4', '0004GSA5', '0004GSA6']
>>> generate()
'0004GSA7'
>>> generate()
'0004GSA8'
>>> 
```

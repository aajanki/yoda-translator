# Write like Yoda

Tämä ohjelma muuttaa kirjoitetun tekstin sanajärjestyksen Yodan puheen
sanajärjestykseksi.

## Setup

Use [Poetry](https://python-poetry.org/docs/) to manage dependencies.

```
poetry install
```

For English support, install the language model:
```
poetry run python -m spacy download en_core_web_sm
```

## Run

```
poetry run python yoda/yoda.py <input text file>
```

## Tests

```
poetry run pytest tests
```

## License

The MIT license

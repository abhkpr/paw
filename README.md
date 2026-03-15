# paw 🐾

local AI commit message generator. uses codellama via ollama to write conventional commit messages from your staged changes. no API keys, no internet, no subscriptions.

## install
```bash
git clone https://github.com/abhkpr/paw
cd paw
pip3 install -e .
```

## requirements

- Python 3.10+
- [ollama](https://ollama.com) running locally
- codellama pulled: `ollama pull codellama`

## usage
```bash
git add <files>
paw                  # generate and commit
paw --dry            # preview only
paw --type fix       # force commit type
paw --no-body        # subject line only
paw --model llama3   # use different model
```

## how it works

1. reads staged diff via git diff --cached
2. sends to codellama via ollama local API
3. generates conventional commit message
4. you review: commit / regenerate / edit / abort

everything runs locally. your code never leaves your machine.

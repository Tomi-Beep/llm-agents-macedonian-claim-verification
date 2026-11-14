# Verifying Macedonian claims with LLM agents

The project researches if an AI agent's claims using macedonian context (in this demo app, 2021 macedonian census results) can be made better with an aditional AI agent reviewing its answers and having the original AI agent revise and propose a final answer.

I used the same Qwen3:4b-instruct model for the 2 agents. The investigator agent picks a census excerpt and writes a verdict with a short explanation. The skeptic agent checks that answer against the same excerpt, then the investigator revises it. After review and revision, **16 of 18** answers had both the right verdict and an explanation backed by the excerpt, up from **7 of 18** on the first pass.

[Project report in Macedonian](reports/Project%20report%20-%20MK.pdf) · [Project report in English](reports/Project%20report%20-%20EN.pdf) · [Scoring notes](results/census-scoring.md)

## To run the demo
With Python 3 installed and Ollama running, open a terminal in the project folder and run these commands. If your system uses `python3`, use that in place of `python`.
```sh
ollama pull qwen3:4b-instruct-2507-q4_K_M
python -m pip install -r requirements.txt
python examples/first-investigator.py
```

The demo checks one claim and prints the first answer, the skeptic’s feedback, and the revised answer. To run all 18 cases, use `python run-benchmark.py`. It writes to `results/latest-run.jsonl`. The [published results](results/census-results.jsonl) are kept separately.
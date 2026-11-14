import json
from pathlib import Path

from claim_verification import model, verify_claim

project_folder = Path(__file__).parent

with open(project_folder / "data" / "census-benchmark.json", encoding="utf-8") as dataset_file:
    dataset = json.load(dataset_file)

records = {}
catalogue = ""
for record in dataset["records"]:
    source_id = record["id"]
    records[source_id] = record["text"]
    catalogue += f"{source_id}: {record['title']}\n"

cases = dataset["cases"]

# Pishuvanjeto vo file go napraviv so pomosh na AI, treba da istrazham samostojno kako rabotat ovie metodi
with open(project_folder / "results" / "latest-run.jsonl", "w", encoding="utf-8") as results_file:
    for number, case in enumerate(cases, start=1):
        print()
        print("Случај:", number, "од", len(cases), "-", case["id"], flush=True)
        print("Тврдење:", case["claim"], flush=True)

        result = {"case": case, "model": model}
        result.update(verify_claim(case["claim"], records, catalogue))
        results_file.write(json.dumps(result, ensure_ascii=False) + "\n")
        results_file.flush()

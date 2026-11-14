import json
from pathlib import Path
from time import perf_counter

from ollama import chat

model = "qwen3:4b-instruct-2507-q4_K_M"

def verify_claim(claim, records, catalogue):
    started = perf_counter()

    choice_prompt = f"""Кој е најрелевантниот запис за проверка на ова тврдење?
    Тврдење: {claim}
    
    Достапни записи:
{catalogue}
    
    Врати само едно ID од списокот.
    """

    choice = chat(
        model=model,
        messages=[{"role": "user", "content": choice_prompt}],
        options={"temperature": 0, "num_predict": 24},
        keep_alive="1m",
    )
    source_id = choice.message.content
    print("Побаран запис:", source_id)

    evidence = records.get(source_id)

    if evidence is None:
        print("Непознат запис. Проверката запира.")
        return {
            "source_id": source_id,
            "error": "unknown-source",
            "model_calls": 1,
            "total_seconds": round(perf_counter() - started, 2),
        }
    else:
        print("Отворен доказ:", evidence)

        verdict_prompt = f"""Провери го тврдењето според приложениот запис.
    Тврдење: {claim}
    Доказ: [{source_id}] {evidence}
    
    На првиот ред напиши точно една од овие пресуди:
    поткрепено
    противречи на доказите
    недоволно докази
    
    На вториот ред објасни во една реченица што покажува доказот за тврдењето.
    Наведи го ID на доказот во таа реченица.
    """

        reply = chat(
            model=model,
            messages=[{"role": "user", "content": verdict_prompt}],
            options={"temperature": 0, "num_predict": 160},
            keep_alive="1m",
        )
        draft_seconds = round(perf_counter() - started, 2)
        print(reply.message.content)

        draft = reply.message.content

        skeptic_prompt = f"""Ти си проверувач на одговорот на истражувачот.
    
    Тврдење: {claim}
    Доказ: [{source_id}] {evidence}
    Одговор на истражувачот:
    {draft}
    
    Дозволени пресуди: поткрепено, противречи на доказите, недоволно докази.
    Провери дали пресудата е дозволена и дали објаснувањето кажува што покажува доказот.
    Во една или две реченици на македонски кажи што треба да се поправи. Ако сè е во ред, кажи зошто.
    """

        review = chat(
            model=model,
            messages=[{"role": "user", "content": skeptic_prompt}],
            options={"temperature": 0, "num_predict": 160},
            keep_alive="1m",
        )

        print("Забелешка од проверувачот:")
        print(review.message.content)

        revision_prompt = f"""Ти си истражувачот. Дај конечен одговор за тврдењето.
    
    Тврдење: {claim}
    Доказ: [{source_id}] {evidence}
    
    Твој прв одговор:
    {draft}
    
    Забелешка од проверувачот:
    {review.message.content}
    
    На првиот ред напиши точно една од овие пресуди:
    поткрепено
    противречи на доказите
    недоволно докази
    
    На вториот ред објасни во една реченица што покажува доказот за тврдењето.
    Наведи го ID на доказот во таа реченица.
    Користи ја забелешката само ако се согласува со доказот и дозволените пресуди.
    """

        final_reply = chat(
            model=model,
            messages=[{"role": "user", "content": revision_prompt}],
            options={"temperature": 0, "num_predict": 160},
            keep_alive=0,
        )

        print("Конечен одговор:")
        print(final_reply.message.content)

        return {
            "source_id": source_id,
            "evidence": evidence,
            "draft": draft,
            "review": review.message.content,
            "final": final_reply.message.content,
            "model_calls": 4,
            "draft_seconds": draft_seconds,
            "total_seconds": round(perf_counter() - started, 2),
        }

project_folder = Path(__file__).parent

with open(project_folder / "census-benchmark.json", encoding="utf-8") as dataset_file:
    dataset = json.load(dataset_file)

records = {}
catalogue = ""
for record in dataset["records"]:
    source_id = record["id"]
    records[source_id] = record["text"]
    catalogue += f"{source_id}: {record['title']}\n"

cases = dataset["cases"]

# Pishuvanjeto vo file go napraviv so pomosh na AI, treba da istrazham samostojno kako rabotat ovie metodi
with open(project_folder / "census-results.jsonl", "w", encoding="utf-8") as results_file:
    for number, case in enumerate(cases, start=1):
        print()
        print("Случај:", number, "од", len(cases), "-", case["id"], flush=True)
        print("Тврдење:", case["claim"], flush=True)

        result = {"case": case, "model": model}
        result.update(verify_claim(case["claim"], records, catalogue))
        results_file.write(json.dumps(result, ensure_ascii=False) + "\n")
        results_file.flush()

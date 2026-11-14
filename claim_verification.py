from time import perf_counter

from ollama import chat

model = "qwen3:4b-instruct-2507-q4_K_M"

def ask_model(prompt, token_limit, keep_alive):
    response = chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0, "num_predict": token_limit},
        keep_alive=keep_alive,
    )
    return response.message.content

def verify_claim(claim, records, catalogue):
    started = perf_counter()

    choice_prompt = f"""Кој е најрелевантниот запис за проверка на ова тврдење?
    Тврдење: {claim}

    Достапни записи:
{catalogue}

    Врати само едно ID од списокот.
    """

    source_id = ask_model(choice_prompt, 24, "1m")
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

        draft = ask_model(verdict_prompt, 160, "1m")
        draft_seconds = round(perf_counter() - started, 2)
        print(draft)

        skeptic_prompt = f"""Ти си проверувач на одговорот на истражувачот.

    Тврдење: {claim}
    Доказ: [{source_id}] {evidence}
    Одговор на истражувачот:
    {draft}

    Дозволени пресуди: поткрепено, противречи на доказите, недоволно докази.
    Провери дали пресудата е дозволена и дали објаснувањето кажува што покажува доказот.
    Во една или две реченици на македонски кажи што треба да се поправи. Ако сè е во ред, кажи зошто.
    """

        review = ask_model(skeptic_prompt, 160, "1m")

        print("Забелешка од проверувачот:")
        print(review)

        revision_prompt = f"""Ти си истражувачот. Дај конечен одговор за тврдењето.

    Тврдење: {claim}
    Доказ: [{source_id}] {evidence}

    Твој прв одговор:
    {draft}

    Забелешка од проверувачот:
    {review}

    На првиот ред напиши точно една од овие пресуди:
    поткрепено
    противречи на доказите
    недоволно докази

    На вториот ред објасни во една реченица што покажува доказот за тврдењето.
    Наведи го ID на доказот во таа реченица.
    Користи ја забелешката само ако се согласува со доказот и дозволените пресуди.
    """

        final_answer = ask_model(revision_prompt, 160, 0)

        print("Конечен одговор:")
        print(final_answer)

        return {
            "source_id": source_id,
            "evidence": evidence,
            "draft": draft,
            "review": review,
            "final": final_answer,
            "model_calls": 4,
            "draft_seconds": draft_seconds,
            "total_seconds": round(perf_counter() - started, 2),
        }
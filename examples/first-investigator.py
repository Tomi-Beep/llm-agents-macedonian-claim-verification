from ollama import chat

model = "qwen3:4b-instruct-2507-q4_K_M"
claim = "Според Пописот од 2021 година, Северна Македонија имала 2.097.319 резидентни жители."

choice_prompt = f"""Кој е најрелевантниот запис за проверка на ова тврдење?
Тврдење: {claim}

Достапни записи:
census-total: Вкупно попишано население, Попис 2021
census-residents: Резидентно население, Попис 2021

Врати само едно ID од списокот.
"""

choice = chat(
    model=model,
    messages=[{"role": "user", "content": choice_prompt}],
    options={"temperature": 0, "num_predict": 24},
    keep_alive="1m",
)
source_id = (choice.message.content or "").strip()
print("Побаран запис:", source_id)

records = {
    "census-total": "На Пописот од 2021 година биле попишани вкупно 2.097.319 лица.",
    "census-residents": "На Пописот од 2021 година биле попишани 1.836.713 резидентни жители.",
}

evidence = records.get(source_id)

if evidence is None:
    print("Непознат запис. Проверката запира.")
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
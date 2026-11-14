# Census benchmark scoring

The same 18 constructed claims and six official census excerpts were used to evaluate two answers per case. The draft follows the investigator's source selection and initial verdict. The final answer follows one skeptic review and one revision using the same opened excerpt. Both roles used Qwen3 4B Instruct (`qwen3:4b-instruct-2507-q4_K_M`).

## Scoring rules

- **Verdict.** The first line must match the expected label, ignoring whitespace around it. A later correction within the answer does not change the declared verdict.
- **Evidence and explanation.** The answer must cite the relevant opened record and explain how that excerpt supports or contradicts the claim, or what information the excerpt lacks. This is scored separately from the first line. An explanation with an unsupported factual qualification or a material change in what a statistic counts fails this check.
- **Both.** An answer meets the main criterion when it passes both checks. Macedonian spelling, grammar, wording and repetition are described separately. The language review is qualitative.

## Results

| Measure | Investigator draft | After review and revision |
| --- | ---: | ---: |
| Correct verdict | 7/18 (38.9%) | 18/18 (100%) |
| Evidence and explanation pass | 15/18 (83.3%) | 16/18 (88.9%) |
| Correct verdict with a justified citation | 7/18 (38.9%) | 16/18 (88.9%) |
| Supported verdicts correct | 6/6 | 6/6 |
| Contradicted verdicts correct | 1/6 | 6/6 |
| Insufficient-evidence verdicts correct | 0/6 | 6/6 |
| Model calls per case | 2 | 4 |
| Mean elapsed time per case | 29.91 s | 74.67 s |

All 18 requested record IDs matched the expected evidence IDs, and there were zero invalid requests. Review and revision corrected 11 declared verdicts and preserved seven. On the combined verdict and evidence criterion, nine cases improved and seven remained correct. Cases 06 and 11 still failed the evidence check. The full workflow added an average of 44.76 seconds per claim on this run.

## Worked example

Case 01 claims that fewer than 600,000 households were recorded. The excerpt `census-households` gives 598,632. Both answers declare `поткрепено`, cite that record, and make the correct numerical comparison. Both pass the two checks. Both also write “евентирани” where “евидентирани” is the standard form.

## Scores by case

| Case | Draft verdict | Draft evidence | Final verdict | Final evidence | Review notes |
| --- | --- | --- | --- | --- | --- |
| census-01 | Pass | Pass | Pass | Pass | Both compare 598,632 with 600,000 correctly. Both use “евентирани”. |
| census-02 | Fail | Pass | Pass | Pass | The draft explains that 3.06 differs from 4.06. The final verdict agrees with that explanation. |
| census-03 | Fail | Pass | Pass | Pass | The draft recognizes that the mean cannot establish the share of two-person households. The final states the missing count more clearly. |
| census-04 | Pass | Pass | Pass | Pass | Both compare 839,174 with 800,000 correctly. The final uses “евентирал”. |
| census-05 | Pass | Pass | Pass | Pass | Both compare 839,174 with 900,000 correctly. Both use “евентирал”. |
| census-06 | Fail | Fail | Pass | Fail | Both explain that the vacant-dwelling count is missing, but describe the recorded total as “постојан број” or “постојани станови”. The excerpt gives the total number of dwellings. The final also uses “па се не може”. |
| census-07 | Pass | Pass | Pass | Pass | Both use the correct nonresident count. The draft uses “пресудува” for what the evidence says. The final ends with “се седи со тврдењето”. |
| census-08 | Fail | Fail | Pass | Pass | The draft gives the right figure but reasons that it supports a different figure and repeats “сè уште”. The final explains the contradiction. |
| census-09 | Fail | Pass | Pass | Pass | Both identify the missing age breakdown. The draft adds an unfinished note with “даденото доказ”. |
| census-10 | Pass | Pass | Pass | Pass | Both identify the group and its share of the resident population. Both use the awkward construction “што сочинуваат” after referring to people. |
| census-11 | Fail | Pass | Pass | Fail | The draft correctly attributes 7.20% to the people whose data came from administrative sources. The final says the administrative data itself makes up 7.20% of the resident population. |
| census-12 | Fail | Pass | Pass | Pass | Both identify the missing breakdown by sex. The draft's “конкретен развој на пол сооднос” is awkward. |
| census-13 | Pass | Pass | Pass | Pass | Both use the correct Ohrid resident count. Both use “евентирал”. |
| census-14 | Fail | Pass | Pass | Pass | Both identify 18,368 as households. The final explains the category mix-up and would be clearer with the actual resident count of 51,428. |
| census-15 | Fail | Fail | Pass | Pass | The draft claims that the excerpt establishes a comparison with 2002. The final identifies the missing 2002 count. “Дали е имало” is ungrammatical here. |
| census-16 | Pass | Pass | Pass | Pass | Both compare 30,450 with 30,000 correctly. Both use “евентирани”. |
| census-17 | Fail | Pass | Pass | Pass | Both give the correct Kumanovo resident count of 98,104. The draft adds an unfinished correction. Both use “евентирал”. |
| census-18 | Fail | Pass | Pass | Pass | Both identify the missing construction-year data. Both use “став” where “стан” is intended. |

## Interpretation

The initial answer declared `поткрепено` on 17 of 18 cases. Several of its explanations already recognized a contradiction or named missing evidence. The largest gain was in making the declared verdict agree with the evidence. A correct label could still come with an imprecise explanation, as cases 06 and 11 show. Several language errors survived revision.

This is one run on a small set of constructed census claims. The comparison measures the combined effect of receiving a skeptic's review and making another model call to revise. A revision-only comparison with the same model and evidence would help distinguish the contribution of the skeptic's feedback.

[Claim set and evidence catalogue](census-benchmark.json) · [Saved replies and timings](census-results.jsonl)

---
slug: wrong-answers-that-raise-no-error
title: The wrong answers that raise no error
date: 2026-09-28
summary: A fine-tuned 0.5B model writes the right SQL 83% of the time. What worries me is the 16% that runs cleanly and returns the wrong rows.
---

I fine-tuned a 0.5B model to write SQL and scored it by running the SQL. Right answers went from 43% to 83%, the number you would put on a slide. The number I care about is 16%: answers that run cleanly and return the wrong rows. Only 1% fail to run, so a schema check, the obvious guardrail, catches almost none of what goes wrong.

[[figure:outcomes]]

Reading 30 of the wrong answers, the most common problem was a changed string constant: "nouvelair" became "nouvelle-air". A rule that flags constants that are not in the question fires on 18.8% of the wrong answers and 0.3% of the right ones, and costs no extra inference. Adding a five-sample agreement check brought silent errors from 16.4% to 9.1% while still answering 76% of questions. Better, and still above the 5% target, which was my own assumption, and the repository says so.

So the decision I wrote down is: do not ship it as an autonomous answerer; ship it as a tool that suggests SQL for a person to review. The lesson is that accuracy tells you how often a model is right, and the product decision depends on how it fails. Measure the failure you cannot see.

The scoring method, the audit of the 30 cases, the guardrail table and what would change the decision are in the [llm-finetune-lab README](https://github.com/YuchenHe985/llm-finetune-lab#readme).

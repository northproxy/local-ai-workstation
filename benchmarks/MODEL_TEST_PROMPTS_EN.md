# MODEL_TEST_PROMPTS_EN.md

# Local LLM Benchmark Prompts

The goal of this file is to test local LLMs with **identical prompts** so that we can compare not only speed, but also the model's real-world usefulness.

Main principle:

> Do not change the wording of the prompts between models.

Ideally, run each model in a fresh, clean chat so that previous context does not affect the result.

---

# 1. What to record before each test

```text
Model: Qwen3.5-9B
Exact model/repository: qwen/qwen3.5-9b
Quantization: Q4_K_M
Runtime: LM Studio
Context length: 8192
GPU offload: 32 layers
Reasoning mode: Enabled, budget unrestricted
Temperature: 1
VRAM used: Not recorded
System RAM used: Not recorded
```

After each response:

```text
Tokens/sec:
Time to first token:
Total response time:
Output tokens:
```

---

# 2. Quality scoring

Score each response from 0 to 10.

| Metric | What to evaluate |
|---|---|
| Correctness | Factual and technical accuracy |
| Reasoning | How logically the model arrives at its conclusion |
| Instruction following | Whether all prompt requirements were followed |
| Clarity | How easy the explanation is to understand |
| Conciseness | Whether the answer avoids unnecessary verbosity |
| Practical usefulness | Whether the result can actually be used |
| Subjective quality | How much you personally like the answer |

---

# CORE BENCHMARK

Run these tests on **every model**.

---

## TEST 1 — Explanation / Teaching

### Prompt

```text
Explain the difference between RAM and VRAM so that I understand not only the definitions, but also why this difference is critical when running local LLMs.

Use a concrete example of a computer with:
- 32 GB RAM
- an NVIDIA GPU with 8 GB VRAM

Explain:
1. where the model weights are stored;
2. what happens if the model fits entirely in VRAM;
3. what happens if the model does not fit in VRAM;
4. why performance can drop sharply;
5. what role the KV cache plays.

Do not use analogies such as "a desk and a cabinet." Explain it technically, but clearly.
Maximum 700 words.
```

### What this tests

- technical knowledge;
- teaching ability;
- instruction following;
- structure;
- conciseness.

---

## TEST 2 — Troubleshooting

### Prompt

```text
There is a Windows 11 computer.

Symptoms:
- internet access by IP address works;
- ping 1.1.1.1 works;
- ping google.com does not work;
- the browser says the DNS name cannot be resolved;
- other devices on the same network work normally.

You must diagnose the problem as a system administrator.

Provide a step-by-step troubleshooting plan.

Requirements:
- start with the safest checks;
- do not immediately suggest reinstalling drivers or resetting Windows;
- for each step, explain exactly what we are checking;
- provide specific Windows commands;
- after each important test, explain how to interpret the possible results;
- at the end, list the 3 most likely causes in order of probability.

Do not invent command results.
```

### What this tests

- practical reasoning;
- Windows/network knowledge;
- diagnostic sequencing;
- hallucination resistance.

---

## TEST 3 — Logical Reasoning

### Prompt

```text
There are four servers: A, B, C, and D.

We know the following:

1. If server A is running, server B is also running.
2. If server B is not running, server C is running.
3. Server C is not running.
4. Server D is running only if server A is running.
5. Server D is running.

Determine the state of each server: running or not running.

Show the conclusion for each server separately and explain which condition it follows from.

If any conditions contradict each other, explicitly point this out.
```

### Expected logical result

```text
A = works
B = works
C = does not work
D = works
```

No contradiction.

### What this tests

- implication logic;
- avoiding inverse/converse errors;
- ability to show derivation.

---

## TEST 4 — Coding / Debugging

### Prompt

```text
Analyze this Python code:

def unique_users(users):
    result = []
    for user in users:
        if user.lower() not in result:
            result.append(user)
    return result

data = ["Alice", "alice", "BOB", "Bob", "Charlie"]

print(unique_users(data))

The goal of the function is to return users without duplicates, ignoring case, while preserving the capitalization of the first occurrence.

1. Find the bug.
2. Explain why the current implementation behaves incorrectly.
3. Write a corrected version.
4. Preserve the original order of elements.
5. Do not use third-party libraries.
6. State the expected output for the given `data`.
7. Briefly evaluate the time complexity of the original and corrected versions.

Do not rewrite the task in a completely different way unless necessary.
```

### Expected result

```python
["Alice", "BOB", "Charlie"]
```

A good solution should maintain a separate normalized `set`.

### What this tests

- code comprehension;
- bug detection;
- complexity knowledge;
- instruction following.

---

## TEST 5 — Instruction Following

### Prompt

```text
Answer the question: "What is CIDR?"

Strict requirements for the response:

- exactly 5 bullet points;
- each bullet point must contain no more than 2 sentences;
- you must use the example `192.168.1.0/24`;
- you must explain what `/24` means;
- you must state the subnet mask;
- you must state the network address;
- you must state the broadcast address;
- do not use tables;
- do not use headings;
- do not add a conclusion after the list.
```

### What this tests

- strict instruction following;
- formatting discipline;
- ability not to add unnecessary text.

---

# EXTENDED BENCHMARK

Run these if the model looks promising after the Core Benchmark.

---

## TEST 6 — Linux Analysis

### Prompt

```text
An application on a Linux server sometimes stops responding.

The following observations are available:

- CPU usage is normally 20–30%;
- RAM usage is 70%;
- load average rises sharply shortly before the freeze;
- `top` does not show any process with very high CPU usage;
- the disk is almost full: 94%;
- `dmesg` sometimes shows I/O timeout messages;
- after a reboot, the problem temporarily disappears.

Analyze the situation.

I do not want a list of every possible cause. I want a prioritized hypothesis.

Structure your answer as follows:

1. the most likely cause;
2. why the symptoms point to it;
3. which 5 checks to perform;
4. which results would confirm the hypothesis;
5. which results would make you reject the hypothesis.

Do not claim that the diagnosis has been proven.
```

---

## TEST 7 — Architecture / Local LLM

### Prompt

```text
I want to build a local AI workstation.

Hardware:

Laptop:
- Windows 11
- Ryzen 9
- 32 GB RAM
- RTX 5070 Laptop GPU with 8 GB VRAM

Desktop:
- a separate computer on the same LAN;
- GPU specifications are currently unknown.

Goals:
- local chat;
- coding assistant;
- RAG over documentation;
- MCP tools;
- automation;
- agents later.

Propose an MVP architecture.

Constraints:
- do not use Kubernetes;
- do not build a multi-agent system in the first phase;
- do not assume that the VRAM of the two computers can simply be added together;
- minimize the number of components;
- security is more important than convenience for shell/filesystem tools.

Provide:
1. an ASCII architecture diagram;
2. the purpose of each component;
3. the installation order;
4. what should NOT be installed yet;
5. criteria for considering the MVP complete.
```

---

## TEST 8 — Summarization with Constraints

### Prompt

```text
Create a concise summary of the following text.

Text:

"The company is moving its internal monitoring system from a single physical server to a virtualized infrastructure. The old server runs Ubuntu 20.04 and uses a local PostgreSQL database. The new architecture must use Ubuntu 24.04, with one separate virtual machine for the database and another for the application. Database access is allowed only from the application server. Backups must run daily at 02:00 and be retained for 14 days. External access to PostgreSQL is prohibited. The application must be accessible to users over HTTPS. The migration must be completed with no more than 30 minutes of downtime."

Summary requirements:

- maximum 120 words;
- divide the answer into "Goal", "Constraints", and "Critical Requirements";
- do not add any requirements that are not present in the source text;
- explicitly highlight the allowed downtime.
```

---

## TEST 9 — Ambiguity / Good Judgment

### Prompt

```text
A user says:

"My server is slow. What should I do?"

Respond as a good technical assistant.

You must not invent the server configuration or the cause of the problem.

Your task:
- explain which categories of problems are most likely;
- provide 3–5 safe initial checks;
- show Linux commands;
- clearly separate facts from hypotheses;
- state the minimum additional information needed for a more precise diagnosis.

The answer should still be useful before any additional information is provided.
```

---

## TEST 10 — Planning / Project Management

### Prompt

```text
A small Python function needs to be implemented. Every day it reads a JSON file containing product prices, compares the prices with the previous day's file, and records the changes in SQLite.

The project already exists.

Create an implementation plan, but do not write code yet.

Constraints:
- maximum 8 steps;
- each step must have a verifiable result;
- first inspect the existing project structure;
- changing the SQLite schema is allowed only if necessary;
- tests must be included;
- the case where yesterday's file is missing must be handled;
- do not suggest Docker or a new framework unless necessary.

At the end, list the 3 main technical risks.
```

---

# REASONING A/B TEST

If the model supports switching reasoning/thinking on and off, run this prompt twice:

1. Reasoning OFF
2. Reasoning ON

Keep all other settings identical.

## TEST R1

```text
A company has three backup servers: A, B, and C.

Rules:

- If A is used as primary, B must be available.
- If B is unavailable, C must be primary.
- A is currently primary.
- C is currently not primary.
- Exactly one server is currently unavailable.

Can we uniquely determine which server is unavailable?

Analyze all valid state combinations.

Do not guess. If the information is insufficient for a unique answer, say so explicitly.
```

### Expected reasoning

A is primary, therefore B must be available.

Assuming a server acting as primary must itself be available, A is also available.

Exactly one server is unavailable, therefore C is unavailable.

A strong answer should explicitly state that assumption.

---

# LONG RESPONSE CONTROL TEST

## TEST L1

```text
Explain what DNS cache poisoning is.

Response requirements:
- maximum 180 words;
- no history of DNS;
- no table;
- include one short example;
- separately explain how DNSSEC helps against this attack;
- do not provide instructions for carrying out the attack.
```

---

# PERSONAL QUALITY TEST

For every promising model, add 2–3 questions that you actually use in real work.

Example:

```text
I am learning the Linux CLI.

Explain the difference between:

grep
find
locate

I want to understand not just the definitions, but when I would choose one command instead of another in real work.

Give 2 practical examples for each command and finish with one small exercise for me to practice.
```

Score separately:

```text
Would I prefer receiving this answer from this model every day?

YES / NO
```

---

# STANDARD TEST PROCEDURE

For every new model:

1. Open a new clean chat.
2. Load the model.
3. Check the parameters.
4. Do not change the prompts.
5. Run Core tests 1–5.
6. Record tokens/sec and TTFT.
7. Score the responses.
8. If the model looks promising, run the Extended tests.
9. If reasoning mode is available, run R1 with reasoning ON and OFF.
10. Compare the results with the current baseline.

---

# CURRENT BASELINE

| Model | Quant | Approx. speed | Subjective status |
|---|---|---:|---|
| Gemma 4 E4B QAT | QAT | ~52 tok/s | Fast, but answers less preferred |
| Qwen3-14B | Q4_K_M | ~8.5 tok/s | Current quality baseline |
| Qwen3.8-27B | Q4 | ~0.7 tok/s | Too slow for interactive work |
| Qwen3.5-9B | TBD | TBD | Next candidate |

The goal is not to maximize tokens/sec.

The goal is:

> **maximum useful answer quality at acceptable interactive speed on the available hardware.**

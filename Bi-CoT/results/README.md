<sub>[🏠 Portfolio](https://github.com/heoneyzi) › [📄 Paper](../../README.md) › [Bi-CoT](../README.md) › **Results**</sub>

# 📊 Bi-CoT · draft-reported results

> **Question —** how much does each inference-only stage (self-aware forward CoT, then reverse verification) add over a frozen retrieve-and-read baseline on HotpotQA?

| | |
|---|---|
| **Status** | ✅ reported in the 2025 manuscript draft — transcribed here, **not re-run** |
| **Model / data** | HotpotQA full wiki · MDR retriever · `allenai/unifiedqa-t5-large` reader · GPT-4.1 / GPT-4o for the LLM stages |
| **Compute** | not recorded (hosted LLM API + a GPU for MDR / UnifiedQA) |
| **Headline** | answer EM / F1 **24.16 / 33.15 → 42.77 / 55.40** (+18.61 / +22.25 points) |

<details>
<summary><b>🇰🇷 한국어 요약</b></summary>

논문 초안의 첫 번째 결과 표를 옮긴 것입니다. 검색+QA 기준선에서 순방향 추론을 더하면 EM/F1이 32.67/42.62, 역방향 검증까지 더하면 42.77/55.40이 됩니다. 전체 질문 중 65.3%만 역방향 검증 단계에 들어갔고, 나머지는 검색·QA 단계에서 필요한 근거를 얻지 못했습니다. 다시 실행해 확인한 값은 아닙니다.

</details>

## Setup

- **Baseline** — the original question goes straight through MDR retrieval and UnifiedQA.
- **+ Self-aware forward CoT** — decomposition into dependency-coded sub-questions, per-sub-question retrieval and QA, and an LLM step that checks each answer against the retrieved evidence.
- **Full Bi-CoT** — the forward pipeline plus reverse verification from the original question back through the sub-questions.
- **Metric** — answer-only exact match (EM) and token F1 with SQuAD-style normalisation (the same functions ship in [`../code/tools/notebook_metrics.py`](../code/tools/notebook_metrics.py)); not HotpotQA supporting-fact or joint scores.

## Results

| Configuration | Answer EM (%) | Answer F1 (%) |
|---|---:|---:|
| Retrieve + QA baseline | 24.16 | 33.15 |
| + Self-aware forward CoT | 32.67 | 42.62 |
| **Full Bi-CoT** (+ reverse verification) | **42.77** | **55.40** |

File: [`reported_results.csv`](reported_results.csv) · chart: [`../assets/ablation.png`](../assets/ablation.png), drawn by [`plot_results.py`](plot_results.py).

- Forward CoT adds +8.51 EM / +9.47 F1 over the baseline; reverse verification adds a further +10.10 / +12.78.
- **Coverage:** about **65.3%** of questions entered reverse verification; for the remaining 34.7% retrieval and QA had not produced the evidence it needs (draft, §3.3).

## Takeaway

- Both stages help, and the reverse pass contributes at least as much as the forward pass, even though it only ran on about two thirds of the questions.
- The pipeline is inference-only: MDR and UnifiedQA stay frozen, so the gains come from how the questions, evidence and checks are organised.
- These are draft numbers on a sampled subset (an earlier draft note mentions 505 random full-wiki questions); they are not comparable to official HotpotQA leaderboard results.

## Files

| File | What it is |
|---|---|
| [`reported_results.csv`](reported_results.csv) | the three ablation rows (configuration, stage added, EM, F1) |
| [`plot_results.py`](plot_results.py) | renders `../assets/ablation.png` and `ablation_dark.png` (needs matplotlib) |

<sub>Provenance: values match the public repository's README and <code>docs/RESEARCH.md</code>, which summarise the supplied manuscript (<code>Plug_and_Play_Bi-CoT.docx</code>); one Notion draft of the same table writes the full-method F1 as 55.41. The manuscript itself is not published here. The draft's second table (a conditional comparison with fine-tuned systems) is not reproduced because its subset and protocol are not recoverable.</sub>

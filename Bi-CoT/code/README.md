<sub>[🏠 Portfolio](https://github.com/heoneyzi) › [📄 Paper](../../README.md) › [Bi-CoT](../README.md) › **Code**</sub>

# 🔬 Bi-CoT · research notebooks and offline evaluator

> **Question —** what code produced the Bi-CoT pipeline, and what can be run today without the original data, models or API access?

| | |
|---|---|
| **Status** | ✅ archival release — mirrored from the public repo (commit `5b96b7c`, Sep 2026); evaluator re-run for this portfolio on 2026-09-28 |
| **Model / data** | HotpotQA full wiki, MDR, UnifiedQA-T5-large, GPT-4.1 / GPT-4o / an earlier GPT-3.5 variant — all **external**, none bundled |
| **Compute** | evaluator: Python standard library, CPU · notebooks: a GPU for MDR / UnifiedQA plus OpenAI API access |
| **Headline** | synthetic evaluator check → **50.0 EM / 83.33 F1** (2 questions; a functionality test, not a result) |

<details>
<summary><b>🇰🇷 한국어 요약</b></summary>

Bi-CoT 공개 저장소의 연구 노트북 6개와 오프라인 평가 도구를 그대로 옮긴 폴더입니다. 노트북은 실제 실험 코드이지만 대안 셀과 외부 의존성(HotpotQA, MDR, UnifiedQA, OpenAI API)이 있어 한 번에 재현되는 형태는 아닙니다. 공개 전에 노트북 출력, API 키 문자열, 개인 경로를 제거했습니다. 평가 도구는 표준 라이브러리만으로 바로 실행되며, 합성 예제에서 EM 50.0 / F1 83.33을 확인했습니다.

</details>

## Setup

```bash
# offline evaluator — no model, key, network or extra package
python tools/evaluate_predictions.py --gold examples/gold.json --predictions examples/predictions.json

# research notebooks (read / adapt; not a one-command reproduction)
python -m pip install -r requirements.txt
jupyter lab notebooks        # API cells read OPENAI_API_KEY from the environment
```

The notebooks expect an external workspace at `data/workspace/` (see [`data/README.md`](data/README.md)); [`docs/WORKFLOW.md`](docs/WORKFLOW.md) explains how to obtain HotpotQA, MDR and UnifiedQA, and why MDR needs its own legacy environment.

| Stage | Notebook | Functions to read |
|---|---|---|
| Decomposition (GPT-4.1, ≤ 3 sub-questions, dependency codes, placeholders) | [`MDR_own.ipynb`](notebooks/MDR_own.ipynb) | `decompose_question_with_dependency`, `decompose_and_save_all` |
| Dependency bookkeeping | [`subQ_preparing.ipynb`](notebooks/subQ_preparing.ipynb) | `find_ids_by_depcode`, `list_and_update_dependency_code_all` |
| Retrieval + QA with placeholder substitution | [`MDR_own.ipynb`](notebooks/MDR_own.ipynb) | `run_step2_mdr_on_0json_all`, `run_step3_fused_qa_mdr_all_with_memory_management` |
| Initial QA and answer aggregation | [`CoT1.ipynb`](notebooks/CoT1.ipynb) | `run_qa_and_save_answers`, `run_cot_aggregation` |
| Evidence-support checks (forward CoT) | [`CoT1.ipynb`](notebooks/CoT1.ipynb), [`context_beready.ipynb`](notebooks/context_beready.ipynb) | `process_subq_cot2`, `run_cot2`, `is_answer_supported_by_context_return_idx` |
| Final answer + evidence aggregation | [`CoT1 copy.ipynb`](notebooks/CoT1%20copy.ipynb) | `find_final_answer_and_evidence_via_api`, `can_answer_now` |
| Prediction extraction and EM/F1 | [`MDR2DATA.ipynb`](notebooks/MDR2DATA.ipynb) | `get_final_predictions_from_basedir`, `evaluate_on_ids` |

## Results

Re-run on 2026-09-28: the command above prints `gold_count 2`, `missing_prediction_count 0`, `answer_em_percent 50.0`, `answer_f1_percent 83.33…` — the synthetic pair `"Blue bird!"` vs `"the blue bird"` (exact after normalisation) and `"red"` vs `"red green"` (F1 0.67). It checks the evaluator only; the paper's numbers are in [`../results/`](../results/README.md).

## Takeaway

- The evaluator reproduces the notebook's metric exactly (functions copied unchanged from `MDR2DATA.ipynb`), counts missing predictions as zero and reports them separately — safe to reuse on new prediction files.
- The notebooks are an honest archive of the experiment, including alternative cells, placeholder/dummy results for failed retrievals (exclude those from any evaluation) and cells that overwrite intermediate files; select one coherent path before running.
- A standalone, verified implementation of every reverse-verification step is not part of the recovered snapshot.

## Files

| File | What it is |
|---|---|
| [`notebooks/`](notebooks) | six recovered research notebooks — outputs, credentials, host metadata and absolute paths removed; setup/cleanup cells archived as markdown |
| [`tools/evaluate_predictions.py`](tools/evaluate_predictions.py) | CLI: JSON/JSONL gold (`_id`, `answer`) + prediction map → EM/F1 with missing/extra counts |
| [`tools/notebook_metrics.py`](tools/notebook_metrics.py) | normalisation, EM, F1 and best-reference functions from `MDR2DATA.ipynb` |
| [`examples/`](examples) | synthetic `gold.json` and `predictions.json` |
| [`docs/RESEARCH.md`](docs/RESEARCH.md) · [`docs/WORKFLOW.md`](docs/WORKFLOW.md) · [`docs/PROVENANCE.md`](docs/PROVENANCE.md) | research summary, external requirements and notebook entry points, release-preparation log |
| [`data/README.md`](data/README.md) | where the external workspace goes (ignored by Git upstream) |
| [`requirements.txt`](requirements.txt) · [`CITATION.cff`](CITATION.cff) | import-derived notebook environment (not a historical lockfile); upstream citation metadata |

<sub>Provenance: files are copied unchanged from <a href="https://github.com/heoneyzi/Bi-CoT">heoneyzi/Bi-CoT</a> at <code>5b96b7c</code>, except the method diagram, which lives in <a href="../assets/pipeline.png"><code>../assets/pipeline.png</code></a>. Upstream files use the manuscript title and the co-author spelling “Suhwan Jeong”; the CV spells it “Suhwan Jung”. MDR, HotpotQA, UnifiedQA and the API models remain their authors' and providers' work; no licence is asserted for the co-authored research code.</sub>

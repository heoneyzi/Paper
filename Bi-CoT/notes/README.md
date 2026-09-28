<sub>[🏠 Portfolio](https://github.com/heoneyzi) › [📄 Paper](../../README.md) › [Bi-CoT](../README.md) › **Notes**</sub>

# 🗒️ Bi-CoT · ideation notes

Paper notes from Jiheon's ideation database (“지헌 Ideation”, 2025) for the work that became Bi-CoT. The project began with the *lost in the middle* problem — language models overlook evidence placed in the middle of long contexts — and moved to multi-hop QA, where decomposing a question and checking each hop keeps the relevant evidence in focus. The notes are in Korean, as written.

| # | Note | Paper | Why it mattered for Bi-CoT |
|---|---|---|---|
| 1 | [DecompRC](01_decomprc.md) | *Multi-hop Reading Comprehension through Question Decomposition and Rescoring* — Min et al., ACL 2019 | Decomposition by reasoning type (bridging, intersection, composition, original) plus rescoring; the note decides to decompose with an LLM instead of span extraction, which became Bi-CoT's first stage |
| 2 | [Tree of Thoughts](02_tree_of_thoughts.md) | *Tree of Thoughts: Deliberate Problem Solving with Large Language Models* — Yao et al., 2023 | Branching reasoning with self-evaluation and backtracking, noted as a fallback when a reasoning loop fails |
| 3 | [Auto-CoT](03_auto_cot.md) | *Automatic Chain of Thought Prompting in Large Language Models* — Zhang et al., 2022 | Automatically built chain-of-thought demonstrations (clustered questions + “Let's think step by step”) |
| 4 | [HMT](04_hmt.md) | *HMT: Hierarchical Memory Transformer for Efficient Long Context Language Processing* — He et al., 2024 | Segment summaries as memory for long inputs, read during the lost-in-the-middle phase |

<sub>Converted from Notion with the portfolio's converter (spec: <code>multimodal_papers.json</code>); three empty rows of the database are omitted. The page that hosts this database also contains the Korean manuscript drafts, which are not published.</sub>

---
<sub>[Bi-CoT](../README.md) · [🏠 Portfolio](https://github.com/heoneyzi)</sub>

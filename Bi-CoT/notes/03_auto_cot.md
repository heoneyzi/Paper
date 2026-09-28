# Automatic Chain of Thought Prompting in Large Language Models (Auto-CoT)

<sub>[🏠 Portfolio](https://github.com/heoneyzi) › [📄 Paper](../../README.md) › [Bi-CoT](../README.md) › [Notes](README.md) › **Auto-CoT**</sub>

> [!NOTE]
> **Ideation note (2025, in Korean)** — Automatically built chain-of-thought demonstrations (clustering + "Let's think step by step"). From Jiheon Kang's ideation database (지헌 Ideation) for the work that became Bi-CoT; converted from Notion.

#### 🧩 핵심 아이디어

- 각 질문에 대해 **“Let’s think step by step” prompt**로 LLM이 스스로 CoT 시연을 생성하도록 함.
- 생성된 CoT 중 실질적으로 유용하고 자연스러운 것들을 골라 **few-shot prompt**에 자동으로 포함 → manual 시연과 동등한 성능 달성.
- **Diversity** 확보를 위해 질문 클러스터링 기반 샘플링과 quality filtering 적용.

---
<sub>[← Tree of Thoughts](02_tree_of_thoughts.md) · [🗒️ Notes index](README.md) · [Bi-CoT](../README.md) · [HMT →](04_hmt.md)</sub>

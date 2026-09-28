<sub>[🏠 Portfolio](https://github.com/heoneyzi) › [📄 Paper](../../README.md) › [FTF-VTG](../README.md) › **Code**</sub>

# 🔬 `ftf_vtg` · the released package

> **Question —** can the grounding algorithm run anywhere from a precomputed frame–query similarity curve, with validated inputs and honest evaluation accounting?

| | |
|---|---|
| **Status** | ✅ maintained — mirrored from the public repo (commit `727792f`, Sep 2026); tests re-run for this portfolio on 2026-09-28 |
| **Model / data** | input = one similarity curve per query (no VLM, videos or datasets bundled); `examples/` holds two real single-video curves |
| **Compute** | CPU only; Python ≥ 3.10 with NumPy, PyTorch, OpenCV |
| **Headline** | `pytest`: **12 passed** · demo curve (low–high–low) → samples **11–29** |

## Setup

```bash
python -m pip install -r requirements.txt     # numpy, torch, opencv-python-headless
python -m ftf_vtg --demo                      # synthetic curve; no model, data or GPU
python -m ftf_vtg --scores scores.json --theta-high 0.0015 --output prediction.json
python -m ftf_vtg --task vtg_vidstg --data-dir examples/vtg_VidSTG_json --theta-high 0.0015
python -m pytest -q tests
```

```python
from ftf_vtg import FTF_VTG
start, end = FTF_VTG([0.1] * 12 + [0.9] * 18 + [0.1] * 12)   # inclusive sample indices, or (None, None)
```

Convert sample indices to seconds with the sampling rate **of the similarity curve** (raw-video FPS only when there is one score per frame).

**Parameters** (Python API; the CLI exposes `--theta-high` and `--lambda-weight`):

| Parameter | Role | Package default | Historical variant¹ |
|---|---|---:|---:|
| `kernel_size` | Gaussian window and morphology kernel (odd) | 3 | 7 |
| `sigma` | Gaussian width | 1.0 | 1.0 |
| `alpha` | morphological vs first-order gradient mix | 0.5 | 0.5 |
| `theta_high` | strong-edge threshold | 0.1 | 0.1 |
| `theta_low_ratio` | weak / strong threshold ratio | 0.5 | 0.5 |
| `min_seg_len` | minimum elementary segment length (samples) | 1 | 3 |
| `gap_threshold` | maximum gap for chaining segments (samples) | 100 | 10 |
| `lambda_weight` | contrast term vs support term | 0.5 | 0.5 |

<sub>¹ Defaults of the monolithic file <code>ftf_vtg/src/model/FTF_VTG.py</code>, kept for provenance. The VidSTG setting in the result notes is θ_high = 0.0015, α = 0.05, λ ∈ [0.1, 0.5]; other values were not recorded.</sub>

> [!NOTE]
> The default `theta_high = 0.1` is far above the gradient scale of real CLIP curves (about 10⁻³ on the bundled examples), so on those files the default returns no prediction. Use a θ_high chosen on a validation split; the result notes used 0.0015.

**Dataset adapters** (`--task`, one JSON file per example in `--data-dir`):

| Task | Expected fields | Metrics |
|---|---|---|
| `vmr_didemo` | `similarities`, `fps`, `total_frames`, `num_segments`, `gt_times` (0-based inclusive 5-second bins) | R@1, R@5 over DiDeMo's candidate moments |
| `vtg_didemo` | `similarities`, `video`, `query`, `fps`, `total_frames` + a separate ground-truth list (`video`, `description`, `times`, `num_segments`) | mean IoU, R@1 at IoU ≥ 0.5 |
| `vtg_vidstg` | `used_segment.begin_fid/end_fid`, `ground.begin_fid/end_fid`, `text_queries.description.similarities` | mean IoU, R@1 at IoU ≥ 0.5 |

Examples with no prediction count as misses, DiDeMo ground truth is matched by **both** video and query, and malformed files stop with a filename-specific error.

## Results

Re-run on 2026-09-28 (CPU, PyTorch 2.14): `python -m pytest -q tests` → **12 passed**; `python -m ftf_vtg --demo` → `start_sample 11, end_sample 29`. The adapters also run end-to-end on the two files in `examples/`; with one video each these are smoke tests, not benchmark numbers (reported benchmark results: [`../results/`](../results/README.md)).

The figure on the [paper page](../README.md) is produced by `scripts/plot_pipeline_example.py`, which rebuilds every stage from the package functions and asserts that the result equals `FTF_VTG(...)`.

## Takeaway

- The algorithm needs nothing but a 1-D curve, so it can sit behind any image–text model; swapping the VLM changes only the similarity extraction step.
- Every stage exposes an inspectable intermediate (smoothed curve, gradient, boundary pairs, candidate scores), which is what makes the method explainable.
- The package does **not** include the CLIP extraction step, the datasets, or the final hyper-parameters, so it cannot by itself reproduce the paper's numbers.

## Files

| File | What it is |
|---|---|
| [`ftf_vtg/main.py`](ftf_vtg/main.py) | `FTF_VTG(...)` entry point with input and parameter validation |
| [`ftf_vtg/segment_detector.py`](ftf_vtg/segment_detector.py) | smoothing, hybrid gradient, hysteresis thresholds, start/end pairing |
| [`ftf_vtg/segment_merger.py`](ftf_vtg/segment_merger.py) | chains nearby elementary segments into candidates |
| [`ftf_vtg/segment_scorer.py`](ftf_vtg/segment_scorer.py) | inside/outside contrast + support score |
| [`ftf_vtg/evaluation.py`](ftf_vtg/evaluation.py), [`ftf_vtg/experiment/`](ftf_vtg/experiment) | fixed-parameter dataset adapters (DiDeMo VMR/VTG, VidSTG) |
| [`ftf_vtg/__main__.py`](ftf_vtg/__main__.py), [`test.py`](test.py) | portable CLI (`python -m ftf_vtg`) and its compatibility entry point |
| [`ftf_vtg/src/model/FTF_VTG.py`](ftf_vtg/src/model/FTF_VTG.py) | historical monolithic variant, kept for provenance |
| [`ftf_vtg/src/utils/eval_metrics.py`](ftf_vtg/src/utils/eval_metrics.py) | temporal IoU |
| [`tests/test_portable.py`](tests/test_portable.py) | synthetic inference, invalid/flat input, numerical stability, import safety, miss counting, ground-truth identity |
| [`examples/`](examples) | one DiDeMo curve (`man in red enters view`, 1,020 frames) and one VidSTG curve (5 query phrasings, 615 frames) |
| [`scripts/`](scripts) | portfolio figure scripts (`plot_pipeline_example.py`, `plot_reported_results.py`, shared `_viz.py`) |
| [`requirements.txt`](requirements.txt), [`CITATION.cff`](CITATION.cff) | runtime dependencies; citation metadata from the original repo |

<sub>Provenance: code files are byte-identical to <a href="https://github.com/heoneyzi/Frame_based_Training_Free-Video_Temporal_Grounding">heoneyzi/Frame_based_Training_Free-Video_Temporal_Grounding</a> at <code>727792f</code>; the two example curves moved from <code>data/extracted_json/</code> to <code>examples/</code>, and <code>scripts/</code> was added for this portfolio. The original repository has no licence file, and none is added here on behalf of the co-authors.</sub>

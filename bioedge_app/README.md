# BioEdge AI — Local-first Biomedical Research Companion

BioEdge AI is an experimental application layer built on the Drug–Target Interaction Prediction project.

## Features
- Local TF-IDF retrieval over the repository README.
- Optional local response generation through Ollama, if Ollama and a model are already installed.
- Interactive comparison of baseline and enhanced model R² metrics.
- Explicit scientific limitations and research-use disclaimer.

## Quick start (Windows 11)
Copy the `bioedge_app` folder into the root of your existing project repository, next to the original `README.md`.

From the repository root, run:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r bioedge_app\requirements-app.txt
streamlit run bioedge_app\app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501.

## Optional local LLM
If Ollama and a suitable local model are already installed, enable the Ollama toggle in the app. With 8 GB RAM, use a small quantized model and close memory-heavy applications. Retrieval-only mode does not require an LLM download.

## Architecture
- Streamlit interface
- scikit-learn TF-IDF retrieval and cosine similarity
- Optional Ollama local generation
- Plotly model-metric visualisation

## Scientific transparency
Displayed metrics are taken from the original project's README; they are not newly computed by this app. Protein-grouped R² remains negative, so generalisation to unseen protein targets is limited. This is a research prototype, not a clinical tool.

## Author
R Tharun Kumar | Dual Degree, Biological Sciences, IIT Madras

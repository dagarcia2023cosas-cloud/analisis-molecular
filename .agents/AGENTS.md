# Project Context for AI Agents

## Project
- **Name:** analisismolecular
- **Package:** libreria_analisismolecular
- **Type:** Computational chemistry / molecular analysis
- **Python:** 3.10+ (local: 3.14)
- **Colab integration:** Native support for Google Colab
- **GitHub:** https://github.com/dagarcia2023cosas-cloud/analisismolecular

## Structure
```
analisismolecular/
├── src/libreria_analisismolecular/   # Main package
│   ├── utils.py                      # General utilities
│   └── colab/                        # Google Colab integration
│       ├── setup.py                  # Environment setup
│       ├── drive_utils.py            # Google Drive I/O
│       └── visualization.py          # 3D molecular visualization
├── notebooks/                        # Colab-ready Jupyter notebooks
├── colab/                            # Standalone Colab scripts
├── scripts/                          # Dev sync utilities
├── .vscode/                          # VS Code workspace config
├── data/{raw,processed,external}     # Data directories
├── tests/                            # Pytest tests
└── docs/                             # Documentation
```

## Key Dev Commands (VS Code Tasks available)
- Install: `pip install -e .`
- Full env: `conda env create -f environment.yml`
- Tests: `pytest tests/ -v`
- Lint: `ruff check src/ tests/`
- Format: `black src/ tests/`
- Sync to Colab: `python scripts/sync_to_colab.py`

## VS Code Integration
- Config in `.vscode/` — recommended extensions, debug configs, tasks
- `F5` to debug current file
- Tasks via `Ctrl+Shift+P` → "Tasks: Run Task"
- Extensions auto-prompt on project open

## Workflow: VS Code → GitHub → Colab → VS Code
1. Edit code in VS Code
2. Commit + push to GitHub
3. Open notebook in Colab, clone repo
4. Run analysis (GPU/TPU), save results to Drive
5. Pull results in VS Code

## Dependencies
- rdkit, openbabel (cheminformatics)
- py3Dmol, nglview (3D visualization)
- mdanalysis, prody, biopython (MD analysis)
- numpy, scipy, pandas, matplotlib, seaborn, scikit-learn
- torch (optional ML)

---

## Project organization (collaborative work)

This repo is a clone of David García's project (`dagarcia2023cosas-cloud/analisismolecular`), where **Francisco Pinochet** and **David García** work together.

### Instruction files structure

| File | Purpose |
|------|---------|
| `.agents/AGENTS.md` | **General** project instructions (all agents) — this file must always be in **English** |
| `usuarios/francisco.md` | **Individual** opencode instructions for Francisco |
| `usuarios/david.md` | **Individual** opencode instructions for David |

General instructions apply to every agent interaction with the project.
Individual files contain personal preferences, contact info, and user-specific context.

### Git remotes

- `origin` → `https://github.com/dagarcia2023cosas-cloud/analisismolecular` (David)
- `francisco` → `https://github.com/fpino73/analisismolecular` (Francisco's fork)

**Workflow:**
- **Francisco:** push to `francisco` (fork), create PR → David reviews & merges on GitHub
- **David:** push/pull directly to `origin`, review & merge Francisco's PRs

Since Francisco's token only has access to his own fork, he **cannot push directly** to `origin`. All his contributions go through **Pull Requests** that David must accept on GitHub. When opencode is asked to "pull/push to David's repo", it should push to `francisco` and provide a GitHub PR link.

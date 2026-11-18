# AI Engineering Handbook

A project-based tutorial for building, evaluating, and operating AI applications. Follow **Document Assistant** from a small Python script to an Azure production design. [Read the introduction](docs/index.md) or [pick a chapter](docs/roadmap.md). [Project guide](AI_Engineering_Tutorial.md)

## Preview the handbook

Run these commands from the project root with Python 3.11 or later. The virtual environment keeps the documentation dependencies isolated.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-docs.txt
.\.venv\Scripts\python.exe -m mkdocs serve
```

On Bash, use `.venv/bin/python` for the last two commands. Open <http://127.0.0.1:8000/> and use the search bar or chapter sidebar. MkDocs reloads pages when you save edits.

Run `python -m mkdocs build --strict` with that environment to check the site and write static HTML to `site/`.

## Run the examples

Core scripts in [examples](examples/) use Python and synthetic data. Run chapter commands from the project root. For the API and streaming chapters, install `requirements-examples.txt` in your environment. The hosted model example has separate prerequisites in its chapter. Azure and deployment chapters use walkthroughs and configuration excerpts.

## Edit a chapter

Register new pages in `mkdocs.yml` and link them from the roadmap. When a chapter includes a runnable script, edit the source in `examples/` so the site and the learner execute the same code. Check the build and rerun the script after making changes.

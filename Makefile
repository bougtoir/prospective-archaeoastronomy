PYTHON ?= python3

.PHONY: setup test simulate summarize figures tables manuscript-results package qc all

setup:
	pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest tests -x -q

simulate:
	$(PYTHON) scripts/run_simulations.py

summarize:
	$(PYTHON) scripts/summarize_results.py

figures:
	$(PYTHON) scripts/make_figures.py

tables:
	$(PYTHON) scripts/make_tables.py

catalogs:
	$(PYTHON) scripts/fetch_catalogs.py || true

manuscript-results:
	$(PYTHON) scripts/manuscript_values.py
	$(PYTHON) scripts/build_manuscript.py

package:
	$(PYTHON) scripts/build_docx_inline.py
	$(PYTHON) scripts/make_submission_package.py

qc:
	$(PYTHON) scripts/qc_audit.py

all: test simulate summarize figures tables manuscript-results package qc

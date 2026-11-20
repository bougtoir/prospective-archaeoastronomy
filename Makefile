PYTHON ?= python3

.PHONY: setup test simulate summarize figures tables manuscript-results package qc all calibrated theory-vs-cal

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

calibrated:
	$(PYTHON) scripts/run_calibrated_simulations.py
	$(PYTHON) scripts/run_calibrated_simulations.py --sensitivity

theory-vs-cal:
	$(PYTHON) scripts/theory_vs_calibrated.py

manuscript-results:
	$(PYTHON) scripts/manuscript_values.py
	$(PYTHON) scripts/build_manuscript.py
	$(PYTHON) scripts/build_docx_omml.py

package:
	$(PYTHON) scripts/build_docx_inline.py
	$(PYTHON) scripts/make_submission_package.py

qc:
	$(PYTHON) scripts/qc_audit.py

all: test simulate summarize calibrated theory-vs-cal figures tables manuscript-results package qc

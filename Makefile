install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

run:
	. .venv/bin/activate && uvicorn app.main:app --reload --port 8000

gen-data:
	. .venv/bin/activate && python scripts/generate_synthetic_data.py

features:
	. .venv/bin/activate && python -m app.pipelines.build_features

train:
	# export DYLD_LIBRARY_PATH=/opt/homebrew/opt/libomp/lib:$$DYLD_LIBRARY_PATH
	. .venv/bin/activate && python -m app.pipelines.train_forecast --data data/processed/features.parquet --out models/demand_lgbm.txt

format:
	. .venv/bin/activate && ruff check . --fix && black .

test:
	. .venv/bin/activate && pytest -q

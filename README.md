# Smart Fulfillment Optimizer

Smart Fulfillment Optimizer is a toolkit for experimenting the reduction of fulfillment
time and cost, with order-to-warehouse assignment, batching, and routing strategies. 
The repository is organized to support quick experimentation, reproducible runs, and an optional app layer for visualization or interaction.

## Setup 

### 1. Clone the repository

```
git clone https://github.com/jennifers415/SmartFulfillmentOptimizer.git

python -m venv .venv
source .venv/bin/activate   # for macOS/Linux
# .venv\Scripts\Activate.ps1  # for Windows PowerShell

pip install -r requirements.txt
```

### 2. Pre-commit Hooks (Optional)

```
pip install pre-commit
pre-commit install
```

### 3. Environment Variables

```
cp .env.example .env
```

### 4. Running the App

This depends on the framework used in `app/`, the following are some examples on how to start:

```

# FastAPI example
uvicorn app.main:app --reload

# Flask example
export FLASK_APP=app.app:app && flask run --debug

# Streamlit example
streamlit run app/App.py
```

## Using Makefile

These are some common targets:

```
make setup # install dependencies
make lint  # run formatting/lint checks
make test  # run tests
make run   # start the app or default scenario
```

## Working With Notebooks

You can place exploratory analysis and optimization experiments in `notebooks/`. Suggested notebook flow:

1. EDA.ipynb: data exploration and cleaning
2. model_baselines.ipynb: heuristic or baseline models
3. optimizer_tuning.ipynb: experiments with parameters
4. results_viz.ipynb: comparing KPIs across scenarios

## Data and Configuration

- `data/` should contain example datasets and a short schema description.
- Consider adding configuration files (e.g., YAML or JSON) to define different optimization scenarios.

## Testing

You can add minimal unit tests for:

- Cost function correctness
- Constraint satisfaction
- Deterministic runs with fixed seeds
- Data loading and validation

This can be run with `pytest` or your preferred framework.

```
pytest
```
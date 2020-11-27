# Interference-aware scheduler

Installation

```
python3 -m venv <X>
source <X>/bin/activate
pip install -e .
```

Tests

```
pip install pytest
pytest
```

Example command:

```
python main.py run config.yaml jobs.xml experiment.xml -s RoundRobin -e Gradient -ep estimations_folder
```
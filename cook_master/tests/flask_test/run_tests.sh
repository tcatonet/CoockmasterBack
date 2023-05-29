export PYTHONPATH=$PYTHONPATH:../../backend/
pytest tests.py --capture=tee-sys -x

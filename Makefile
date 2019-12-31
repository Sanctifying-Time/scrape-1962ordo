SRCDIR = ./src

.DEFAULT_GOAL := run

clean:
	rm -rf build dist .coverage coverage.xml .eggs .scannerwork .pytest_cache *.egg-info $(SRCDIR)/__pycache__ $(TESTDIR)/__pycache__ MANIFEST

depend:
	python3 -m pip install -r requirements.txt

run: depend
	python3 src/scrape-1962ordo.py

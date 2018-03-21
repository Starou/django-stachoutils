tests:
	@PYTHONPATH=..:${PYTHONPATH} python runtests.py

coverage-report: coverage
	@coverage report -m

coverage:
	@PYTHONPATH=..:${PYTHONPATH} coverage run --rcfile=coveragerc runtests.py

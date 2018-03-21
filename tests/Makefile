python_version_full := $(wordlist 2,4,$(subst ., ,$(shell python --version 2>&1)))
python_version_major := $(word 1,${python_version_full})

tests:
	@PYTHONPATH=..:${PYTHONPATH} python runtests.py

coverage-report: coverage
	@coverage report -m

coverage:
	@PYTHONPATH=..:${PYTHONPATH} COVERAGE_FILE=.coverage_py${python_version_major} coverage run --rcfile=coveragerc runtests.py

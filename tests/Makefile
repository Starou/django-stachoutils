all: coverage-report-html

tests:
	@PYTHONPATH=..:${PYTHONPATH} python runtests.py

coverage-report: coverage
	@coverage report -m

coverage-report-html: coverage
	@coverage html -d ./coverage-report
	@echo "Visit ./coverage-report/index.html in your Web browser for a coverage report.";

coverage:
	@PYTHONPATH=..:${PYTHONPATH} coverage run --rcfile=coveragerc runtests.py

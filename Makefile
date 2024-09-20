pylint-validate:
	@echo "running pylint validation"
	@black main.py
	@pylint main.py
	
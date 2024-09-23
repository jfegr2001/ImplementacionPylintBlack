pylint-validate:
	@echo "running pylint validation"
	@black main.py
	@pylint main.py

deploy:

	@docker compose build
	@docker compose up -d


	
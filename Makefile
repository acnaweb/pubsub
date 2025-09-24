install:
	python -m venv venv; \
	. venv/bin/activate; \
	pip install --upgrade pip setuptools wheel pip-tools; \
	pip install pre-commit; \
	pip install -e .[dev,quality]; \
	pre-commit install; \
	git config --bool flake8.strict true; \
	pip-compile pyproject.toml -o requirements.txt; \
	pip-compile pyproject.toml --extra dev -o requirements-dev.txt; \
	pip-compile pyproject.toml --extra quality -o requirements-quality.txt; \

run:	
	@python src/pubsub.py

version:	
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Existem alterações pendentes. Faça um commit antes de executar o push."; \
		exit 1; \
	fi
	@if [ "$$(git rev-list --count @{upstream}..HEAD)" -gt 0 ]; then \
		echo "Existem commits locais não enviados. Faça o push."; \
		exit 1; \
	else \
		echo "Digite a versão (exemplo: v0.0.1): "; \
		read TAG; \
		if [ -z "$$TAG" ]; then \
			echo "Erro: A tag não foi informada!"; \
		else \
			echo "Você digitou a tag: $$TAG"; \
			git tag $$TAG && \
			git push origin $$TAG && \
			echo "Tag $$TAG criada com sucesso!"; \
		fi; \
	fi	

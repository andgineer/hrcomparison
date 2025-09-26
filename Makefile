#!make

.HELP: reqs  ## Upgrade requirements including pre-commit
reqs:
	pre-commit autoupdate
	bash ./scripts/compile_requirements.sh
	scripts/include_pyproject_requirements.py requirements.in
	uv pip install -r requirements.dev.txt

.HELP: ver-release  ## Bump major version
ver-release:
	./scripts/verup.sh release

.HELP: ver-feature  ## Bump minor version
ver-feature:
	./scripts/verup.sh feature

.HELP: ver-bug  ## Bump patch version
ver-bug:
	./scripts/verup.sh bug

.HELP: help  ## Display this message
help:
	@grep -E \
		'^.HELP: .*?## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ".HELP: |## "}; {printf "\033[36m%-19s\033[0m %s\n", $$2, $$3}'

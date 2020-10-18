FROM python:3.8

WORKDIR /code/


installDependencies:
    RUN pip install poetry==1.0.10
    COPY pyproject.toml pyproject.toml
    COPY poetry.lock poetry.lock
    RUN poetry install --no-dev --no-interaction --no-root
    SAVE IMAGE


installDevDependencies:
    FROM +installDependencies
    RUN poetry install --no-interaction --no-root
    SAVE IMAGE


checkTypes:
    FROM +installDevDependencies
    COPY setup.cfg setup.cfg
    COPY bfpy/ bfpy/
    COPY tests/ tests/
    RUN poetry run mypy | tee typeChecking.out && \
        mkdir typeChecking/ && mv typeChecking.out typeChecking/
    SAVE ARTIFACT typeChecking/ AS LOCAL .local/reports/typeChecking/

codeMetrics:
    FROM +installDevDependencies
    COPY setup.cfg setup.cfg
    COPY bfpy/ bfpy/
    COPY tests/ tests/
    RUN poetry run radon cc --output-file=cyclomaticComplexity.out bfpy/ tests/ && \
        echo "=== Cyclomatic Complexity ===" && cat cyclomaticComplexity.out && echo "\n" && \
        poetry run radon mi --output-file=maintainabilityIndex.out bfpy/ tests/ && \
        echo "=== Maintainability Index ===" && cat maintainabilityIndex.out && echo "\n" && \
        poetry run radon raw --output-file=rawMetrics.out bfpy/ tests/ && \
        echo "=== Raw Code Metrics ===" && cat rawMetrics.out && echo "\n" && \
        poetry run radon hal --output-file=halsteadComplexity.out bfpy/ tests/ && \
        echo "=== Halstead Complexity ===" && cat halsteadComplexity.out && echo "\n" && \
        mkdir codeMetrics/ && \
        mv cyclomaticComplexity.out maintainabilityIndex.out rawMetrics.out halsteadComplexity.out codeMetrics/
    SAVE ARTIFACT codeMetrics/ AS LOCAL .local/reports/codeMetrics/


runTests:
    FROM +installDevDependencies
    COPY bfpy/ bfpy/
    COPY tests/ tests/
    RUN ls -la && poetry run pytest --cov-report html:testCoverage/
    SAVE ARTIFACT testCoverage/ AS LOCAL .local/reports/testCoverage/


buildPackage:
    FROM +installDependencies
    COPY bfpy/ bfpy/
    RUN poetry build
    SAVE ARTIFACT dist/ AS LOCAL .local/build/

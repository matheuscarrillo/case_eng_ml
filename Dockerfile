FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

ENV PYTHONPATH="${LAMBDA_TASK_ROOT}"

# copiar tudo primeiro (inclui src/)
COPY . .

# instalar projeto
RUN pip install --upgrade pip setuptools wheel && pip install .

# handler
CMD ["src.app.lambda_handler"]
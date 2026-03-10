FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser && mkdir logs qr_codes && chown appuser:appuser logs qr_codes

COPY --chown=appuser:appuser . .

USER appuser

ENTRYPOINT ["python", "main.py"]
CMD ["--url", "https://www.njit.edu"]
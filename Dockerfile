FROM python:3-slim

ENV PGHOST ""
ENV PGUSER ""
ENV PGDATABASE ""
ENV PGPASSWORD ""
ENV PGPORT ""

CMD ["python3", "worker.py"]

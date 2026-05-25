FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py agentpay_client.py config.py ./

ENV MCP_PORT=8005
ENV AGENTPAY_URL=http://localhost:8004

EXPOSE 8005

CMD ["python", "server.py"]

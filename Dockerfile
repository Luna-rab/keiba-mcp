# uvの公式docker image
FROM ghcr.io/astral-sh/uv:python3.13-bookworm AS builder

WORKDIR /build
COPY pyproject.toml uv.lock ./

# 依存関係をインストール
RUN uv sync --frozen --no-install-project
RUN uv pip freeze > requirements.txt

# 実行ステージ: スリム化した最終イメージ
FROM python:3.13-slim-bookworm

WORKDIR /app

# ビルドステージからrequirements.txtをコピー
COPY --from=builder /build/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY weather.py ./

# 実行ユーザーを設定 (セキュリティのため)
RUN useradd -m mcpuser
USER mcpuser

# MCPサーバーを実行 (コンテナ組み込みのpythonを使用)
CMD ["python", "weather.py"]

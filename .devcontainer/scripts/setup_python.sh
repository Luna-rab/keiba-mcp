#!/bin/bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.13
uv run python --version

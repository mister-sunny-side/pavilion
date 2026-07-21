# Pavilion cloud agent base image.
# Toolchains only — Cursor checks out the repo; do not COPY the project.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    clang \
    curl \
    git \
    lld \
    pkg-config \
    libssl-dev \
    python3 \
    python3-venv \
    sudo \
    # Playwright / Chromium runtime libs
    libasound2t64 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    fonts-liberation \
    fonts-noto-color-emoji \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Non-root user (matches environment.json "user")
RUN useradd -m -s /bin/bash ubuntu \
    && echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ubuntu \
    && chmod 0440 /etc/sudoers.d/ubuntu

USER ubuntu
WORKDIR /home/ubuntu

ENV RUSTUP_HOME=/home/ubuntu/.rustup \
    CARGO_HOME=/home/ubuntu/.cargo \
    PATH=/home/ubuntu/.cargo/bin:/home/ubuntu/.local/bin:$PATH

# Rust stable + wasm target + format/lint components
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
    | sh -s -- -y --default-toolchain stable --profile minimal \
    && rustup target add wasm32-unknown-unknown \
    && rustup component add rustfmt clippy

# Dioxus CLI (dx)
RUN curl -LsSf https://dioxus.dev/install.sh | bash \
    && dx --version

# uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && uv --version

WORKDIR /workspace

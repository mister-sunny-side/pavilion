# Pavilion cloud agent base image.
# Toolchains only — Cursor checks out the repo; do not COPY the project.
#
# ubuntu:24.04 already ships a non-root `ubuntu` user (UID 1000). Reuse it —
# do not useradd, or the image build fails.
# Official dx install.sh binaries can be glibc-picky; pin dioxus-cli via cargo
# (same approach as docker/Dockerfile.local).

FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    CARGO_NET_RETRY=10 \
    CARGO_HTTP_TIMEOUT=600 \
    CARGO_REGISTRIES_CRATES_IO_PROTOCOL=sparse

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    binaryen \
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
    unzip \
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
    && rm -rf /var/lib/apt/lists/* \
    # Passwordless sudo for the stock ubuntu user (matches environment.json)
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

# Pin dx to the project Dioxus version; cargo-install links against this image's glibc.
RUN cargo install dioxus-cli --version 0.7.9 --locked \
    && dx --version

# uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && uv --version

WORKDIR /workspace

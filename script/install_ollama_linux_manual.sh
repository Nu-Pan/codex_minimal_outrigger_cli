#!/usr/bin/env bash
set -Eeuo pipefail

# Manual Ollama installer for cmoc local-SLM testing.
#
# This script intentionally performs only the manual Linux tarball install.
# It does NOT:
#   - create or enable a systemd service
#   - start `ollama serve`
#   - pull any model
#   - modify Codex or cmoc configuration
#
# Intended environment:
#   - Ubuntu 24.04 on WSL2 / Windows 11
#   - x86_64 by default
#
# Run from <cmoc-root> manually, for example:
#   bash script/install_ollama_linux_manual.sh
#   bash script/install_ollama_linux_manual.sh --yes

DEFAULT_AMD64_URL="https://ollama.com/download/ollama-linux-amd64.tar.zst"
DEFAULT_ARM64_URL="https://ollama.com/download/ollama-linux-arm64.tar.zst"
DEFAULT_ROCM_URL="https://ollama.com/download/ollama-linux-amd64-rocm.tar.zst"

assume_yes=0
dry_run=0
skip_apt=0
remove_old_libraries=0
with_rocm=0
package_url=""

usage() {
  cat <<'USAGE'
Usage:
  bash script/install_ollama_linux_manual.sh [options]

Options:
  -y, --yes
      Do not prompt before making changes.

  --dry-run
      Print the commands that would be run, but do not change the system.

  --skip-apt
      Do not install prerequisite packages automatically. The script will fail
      if required commands are missing.

  --remove-old-libraries
      Remove /usr/lib/ollama before extracting the new package. Ollama's manual
      Linux install documentation recommends this when upgrading from a prior
      version, but this script requires an explicit option before doing it.

  --rocm
      Also install the optional AMD ROCm package. This is usually unnecessary
      for Ubuntu WSL2 on Windows 11 with an NVIDIA GPU.

  --url URL
      Override the base Ollama package URL. By default, the script chooses the
      official amd64 or arm64 Linux tarball based on `uname -m`.

  -h, --help
      Show this help.

Environment variables:
  SUDO
      Override the sudo command. Set SUDO=doas if needed. If running as root,
      sudo is not used.

What this script installs:
  - Ollama files extracted into /usr from the official Linux tarball.

What this script intentionally does not do:
  - It does not create, enable, start, stop, or edit an ollama systemd service.
  - It does not run `ollama serve`.
  - It does not pull qwen3 or any other model.
  - It does not edit ~/.codex, CODEX_HOME, or .cmoc/config.json.
USAGE
}

log() {
  printf '[cmoc-ollama-install] %s\n' "$*" >&2
}

fail() {
  printf '[cmoc-ollama-install] ERROR: %s\n' "$*" >&2
  exit 1
}

run() {
  if [[ "$dry_run" == 1 ]]; then
    printf '[dry-run]'
    printf ' %q' "$@"
    printf '\n'
    return 0
  fi
  "$@"
}

confirm() {
  local prompt="$1"
  if [[ "$assume_yes" == 1 ]]; then
    return 0
  fi
  local answer=""
  read -r -p "$prompt [y/N] " answer
  case "$answer" in
    y|Y|yes|YES) return 0 ;;
    *) return 1 ;;
  esac
}

have_cmd() {
  command -v "$1" >/dev/null 2>&1
}

sudo_cmd() {
  if [[ "${EUID}" -eq 0 ]]; then
    return 0
  fi
  local sudo_bin="${SUDO:-sudo}"
  if ! have_cmd "$sudo_bin"; then
    fail "sudo command not found: $sudo_bin"
  fi
  printf '%s' "$sudo_bin"
}

is_wsl() {
  grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -y|--yes)
        assume_yes=1
        shift
        ;;
      --dry-run)
        dry_run=1
        shift
        ;;
      --skip-apt)
        skip_apt=1
        shift
        ;;
      --remove-old-libraries)
        remove_old_libraries=1
        shift
        ;;
      --rocm)
        with_rocm=1
        shift
        ;;
      --url)
        [[ $# -ge 2 ]] || fail "--url requires an argument"
        package_url="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        usage >&2
        fail "unknown option: $1"
        ;;
    esac
  done
}

package_url_for_arch() {
  local arch
  arch="$(uname -m)"
  case "$arch" in
    x86_64|amd64)
      printf '%s\n' "$DEFAULT_AMD64_URL"
      ;;
    aarch64|arm64)
      printf '%s\n' "$DEFAULT_ARM64_URL"
      ;;
    *)
      fail "unsupported architecture: $arch"
      ;;
  esac
}

install_prerequisites_if_needed() {
  local missing=()
  local cmd
  for cmd in curl tar zstd ca-certificates; do
    if ! have_cmd "$cmd"; then
      missing+=("$cmd")
    fi
  done

  if [[ "${#missing[@]}" -eq 0 ]]; then
    return 0
  fi

  if [[ "$skip_apt" == 1 ]]; then
    fail "missing required commands/packages: ${missing[*]}"
  fi

  if ! have_cmd apt-get; then
    fail "missing required commands/packages and apt-get is unavailable: ${missing[*]}"
  fi

  log "Missing prerequisites: ${missing[*]}"
  log "Installing prerequisite packages with apt-get."
  local sudo_bin
  sudo_bin="$(sudo_cmd)"
  run "$sudo_bin" apt-get update
  run "$sudo_bin" apt-get install -y --no-install-recommends curl zstd ca-certificates
}

download_package() {
  local url="$1"
  local output_path="$2"
  run curl -fL --retry 3 --retry-delay 2 --connect-timeout 20 -o "$output_path" "$url"
}

verify_ollama() {
  if ! have_cmd ollama; then
    fail "ollama command was not found on PATH after installation"
  fi
  log "Installed Ollama: $(ollama --version 2>&1 || true)"
}

main() {
  parse_args "$@"

  [[ "$(uname -s)" == "Linux" ]] || fail "this installer is for Linux only"

  if ! is_wsl; then
    log "Warning: this does not appear to be WSL. Continuing because plain Linux is supported by Ollama."
  fi

  if [[ -z "$package_url" ]]; then
    package_url="$(package_url_for_arch)"
  fi

  if [[ "$with_rocm" == 1 && "$(uname -m)" != "x86_64" && "$(uname -m)" != "amd64" ]]; then
    fail "--rocm is supported only on x86_64/amd64 by this script"
  fi

  cat >&2 <<EOF
[cmoc-ollama-install] Planned manual Ollama install
  base package:      $package_url
  install target:    /usr
  remove old libs:   $remove_old_libraries
  install ROCm pkg:  $with_rocm
  dry run:           $dry_run

This script will not create or enable a systemd service, will not start
ollama serve, and will not pull any model.
EOF

  if [[ -e /etc/systemd/system/ollama.service || -e /usr/lib/systemd/system/ollama.service ]]; then
    log "Warning: an Ollama systemd service file already exists. This script will not modify it."
  fi

  if [[ -d /usr/lib/ollama && "$remove_old_libraries" != 1 ]]; then
    log "Warning: /usr/lib/ollama already exists."
    log "Ollama's manual upgrade notes recommend removing old libraries first."
    log "Re-run with --remove-old-libraries if this is an upgrade and you accept that deletion."
  fi

  if ! confirm "Proceed with the install"; then
    log "Aborted."
    exit 0
  fi

  install_prerequisites_if_needed

  local tmpdir
  tmpdir="$(mktemp -d)"
  trap 'rm -rf "$tmpdir"' EXIT

  local base_pkg="$tmpdir/ollama-linux.tar.zst"
  log "Downloading Ollama package."
  download_package "$package_url" "$base_pkg"

  local sudo_bin
  sudo_bin="$(sudo_cmd)"

  if [[ "$remove_old_libraries" == 1 ]]; then
    log "Removing old Ollama libraries: /usr/lib/ollama"
    run "$sudo_bin" rm -rf /usr/lib/ollama
  fi

  log "Extracting Ollama package into /usr."
  run "$sudo_bin" tar -x -C /usr -f "$base_pkg"

  if [[ "$with_rocm" == 1 ]]; then
    local rocm_pkg="$tmpdir/ollama-linux-amd64-rocm.tar.zst"
    log "Downloading optional ROCm package."
    download_package "$DEFAULT_ROCM_URL" "$rocm_pkg"
    log "Extracting optional ROCm package into /usr."
    run "$sudo_bin" tar -x -C /usr -f "$rocm_pkg"
  fi

  if [[ "$dry_run" != 1 ]]; then
    verify_ollama
  fi

  cat >&2 <<'EOF'
[cmoc-ollama-install] Done.

Next steps are intentionally manual / test-wrapper controlled, for example:

  # Start a test-scoped Ollama server in another terminal or via a cmoc test wrapper:
  OLLAMA_HOST=127.0.0.1:11435 \
  OLLAMA_MODELS="$HOME/.cache/cmoc/ollama/models" \
  OLLAMA_NO_CLOUD=1 \
  OLLAMA_CONTEXT_LENGTH=32768 \
  OLLAMA_KEEP_ALIVE=0 \
  OLLAMA_MAX_LOADED_MODELS=1 \
  OLLAMA_NUM_PARALLEL=1 \
  ollama serve

  # Then pull the model manually against that server:
  OLLAMA_HOST=127.0.0.1:11435 \
  OLLAMA_MODELS="$HOME/.cache/cmoc/ollama/models" \
  ollama pull qwen3:4b-instruct-2507-q4_K_M
EOF
}

main "$@"

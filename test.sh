CMOC_ROOT=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE:-$0}")" && pwd)
export CMOC_ROOT
export PATH="$CMOC_ROOT/bin:$CMOC_ROOT/.venv/bin:$PATH"

#!/usr/bin/env bash
VENV="venv"
V=3.4
[[ "$BASH_SOURCE" == "$0" ]] && {
    myself="$(readlink -m ${0#-*})"
    echo "Usage: . $myself" > /dev/stderr
    exit 1
} || {
    [[ -d "$VENV" ]] || virtualenv -p "/usr/bin/python${V}" "$VENV"
    echo ">> Entering virtual environment \"$VENV\"" > /dev/stdout
    source "$VENV/bin/activate"
}

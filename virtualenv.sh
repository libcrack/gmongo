#!/usr/bin/env bash
# 28/05/2016 16:24:27
# devnull@libcrack.so

V=
VENV="venv"

[[ -n "${1}" ]] && V="${1}"

[[ "$BASH_SOURCE" == "${0}" ]] && {
    # myself="$(readlink -f "${0#-*}")"
    myself="$(realpath -e "${0#-*}")"
    printf "Usage: . ${myself##*/}\n" > /dev/stderr
    exit 1
} || {
    [[ -d "${VENV}" ]] || {
        printf "\e[33m[W]\e[0m Creating virtual environment at \"${VENV}\"\n" > /dev/stdout
        "virtualenv${V}" -p "/usr/bin/python${V}" "${VENV}"
    }
    printf "\e[32m[+]\e[0m Entering virtual environment \"${VENV}\"\n" > /dev/stdout
    source "${VENV}/bin/activate"
    printf "\e[32m[+]\e[0m Done\n" > /dev/stdout
}

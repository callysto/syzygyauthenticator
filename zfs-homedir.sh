#!/usr/bin/env bash

set -e
set -u
set -o pipefail

ZFSHOME="tank/home"
ZFSOPTS="-o quota=1G"

sys_user_exists() {
    local username="$1"
    ret=false
    getent passwd ${username} > /dev/null 2>&1 && ret=true
    if ! ${ret}; then
        echo "username \"${username}\" does not correspond to a system user!" >&2
        echo >&2
        exit 1
    fi
}

main() {
    local username

    local zfshome="tank/home"

    # Accept two and only two arguments
    if [[ -z "${1:-}" || -z ${2:-} || ! -z ${3:-} ]]; then
        echo "Usage ${0} <USERNAME> <OWNER>" >&2
        echo >&2
        exit 1
    elif [[ ${1} =~ ^[a-z0-9][-a-z0-9.]*$ ]]; then
        username=${1}
	owner=${2}
    else
        echo "Username \"${1}\" doesn't match schema ^[a-z0-9][-a-z0-9.]*\$" >&2
        echo >&2
        exit 1
    fi
    sys_user_exists $owner
    
    local homefs="${zfshome}/${username}"
    local homedir="/$homefs"
    if [[ -d "${homedir}" ]] ; then
        echo "Homedir already exists, not recreating"
    else
        echo "Creating Homedir: ${homedir}"
        zfs create ${ZFSOPTS} ${homefs}
        chown -R ${owner}:${owner} ${homedir}
    fi
}

main "${@:-}"

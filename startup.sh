#! /bin/zsh

function startup ()
{
    EXP=$1; shift; EXEC=$@
    if [ -z $EXEC ]; then
        return 1
    fi

    if ! ps -A | grep -q $EXP; then
        exec $EXEC > /dev/null &!
        return 0
    fi
    return 1
}

startup $@

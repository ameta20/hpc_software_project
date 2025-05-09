#!/bin/bash

_onerror()
{
    exitcode=$?
    echo "-reframe: command \`$BASH_COMMAND' failed (exit code: $exitcode)"
    exit $exitcode
}

trap _onerror ERR

make -j 1 CC="mpicc" CXX="mpicxx" FC="ftn" NVCC="nvcc"

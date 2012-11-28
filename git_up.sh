! /usr/bin/env/ bash

_gitrepo="git://git.naquadah.org/awesome.git"
_gitname="awesome"
_rootdir="~/repo/awesome/"

main()
{
    cd $_rootdir
    cd $_gitname
    git pull naquadah/master
}

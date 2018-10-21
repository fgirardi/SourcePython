#!/bin/bash

function compilador {
		for c in $(find /usr/share/spm/*.py -type f -ctime -1 -exec ls -all {} \; | awk '{print $9}')
		do
			#echo "Compiling Python $c"
			python -OOm compileall $c
		done
}
compilador

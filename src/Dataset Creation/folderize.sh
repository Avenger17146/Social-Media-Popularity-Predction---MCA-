#!/bin/bash

maxfilesperdir=5000

cd hello


        declare -i filecount=0 # number of moved files per dir
        declare -i dircount=0  # number of subdirs created per top level dir

        # loop through all files in that directory and below
        while IFS= read -r -d $'\0' filename
        do
                # whenever file counter is 0, make a new dir:
                if [ "$filecount" -eq 0 ]
                then
                        mkdir "$dircount"
                fi

                # move the file into the current dir:
                mv "$filename" "${dircount}/"
                filecount+=1

                # whenever our file counter reaches its maximum, reset it, and
                # increase dir counter:
                if [ "$filecount" -ge "$maxfilesperdir" ]
                then
                        dircount+=1
                        filecount=0
                fi
        done < <(find -type f -print0)
cd ..
#!/bin/bash

# Checking the IaC YAML files to determine the unique values for a particular parameter used as Ansible extra-var
# Goal is to avoid running a playbook with all tasks included, instead handle creation of unique objects first  (referenced by many)
# then run playbook for the objects that depend on all unique objects
# Bogdan Adrian Burciu 08/02/2021 vers 1

# -------------------------
# Credits:
# https://stackoverflow.com/questions/1494178/how-to-define-hash-tables-in-bash
# https://www.baeldung.com/linux/use-command-line-arguments-in-bash-script

# configure script to exit as soon as any line in the bash script fails and show that line
set -e

# using flags for passing input to script
while getopts d:e: flag
do
    case "${flag}" in
        d) dir_path_iac=${OPTARG};;
        e) extra_var=${OPTARG};;
    esac
done

# create a dictionary (called associative array in bash 4) with key=extra-var output in yaml file and value=yaml file
declare -A associative_array
for i in ` ls -lX $dir_path_iac/external_vars*  | awk '{print $9}' `; do associative_array+=([`cat $i | grep "$extra_var" | awk '{print $2}'`]=$i); done
# show the values (yaml files) for the keys (values of extra-var), hence files for which the extra-var is unique
for j in ` echo "${!associative_array[*]}" `; do echo ${associative_array[$j]}; done


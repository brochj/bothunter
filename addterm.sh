#!/bin/sh

newTerm=$1

if [ "$newTerm" != "" ]; then
    echo $newTerm >> $HOME/pj/bothunter/terms.txt
    printf "\n>> $newTerm added to list\n"
else
    printf "\n You need to type the new term\n"
    printf "\n~>> ./addterm.sh myNewTerm\n"
    echo ""
    echo ""
fi
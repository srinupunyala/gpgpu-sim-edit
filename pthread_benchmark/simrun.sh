#!/bin/bash

if [ "$1" = "-sing" ]
then 
	echo "single app $2 running on 15 SMs"
	./gpgpu_ptx_sim__mergedapps -sing $2 > raw_file_"$2".txt
	echo "run parser"
	python filter.py "-sing" raw_file_"$2".txt
elif [ "$1" = "-sing0" ]
then 
	echo "single app $2 running on 60 SMs"
	./gpgpu_ptx_sim__mergedapps $1 $2 > raw_file_"$2".txt
	echo "parsing"
	python filter.py -sing0 raw_file_"$2".txt
elif [ "$1" = "-apps" ]
then 
	echo "running two apps $2 $3"
	./gpgpu_ptx_sim__mergedapps $1 $2 $3 > aging_1_ilpSMRA/two_apps_"$2"_"$3".txt
	mv stream1.txt aging_1_ilpSMRA/"$2"_with_"$2"_"$3".txt
	mv stream2.txt aging_1_ilpSMRA/"$3"_with_"$2"_"$3".txt
	#echo "parsing"
	#python filter.py "-apps" "$2"_with_"$2"_"$3".txt
	#python filter.py "-apps" "$3"_with_"$2"_"$3".txt
	#echo "done parsing" 

elif [ "$1" = "-apps3" ]
then 
	echo "running three apps"
	./gpgpu_ptx_sim__mergedapps $1 $2 $3 $4 > threeapps_"$2"_"$3"_"$4".txt
	mv stream1.txt stream1_"$2"_"$3"_"$4".txt
        mv stream2.txt stream2_"$2"_"$3"_"$4".txt
        mv stream3.txt stream3_"$2"_"$3"_"$4".txt
fi



#!/bin/bash
tau experiment select scaling
for i in {0..16}
do
tau trial delete $i
done




python3 cableGenerator.py -nopopup
mpirun -np 1 python3 -u main.py |tee ResultsDir/output.log
# mpirun -np 4 python3 -u main.py
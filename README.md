# xor-secret-sharing

Python application that generates deceptive secrets using an XOR-based scheme

To run NAIVE:
python ./xor_secret_sharing.py --secret "hello world" --n 5 --m 5 --NAIVE --output output.txt

To run SIMPLE:
python ./xor_secret_sharing.py --secret "hello world" --n 5 --m 5 --SIMPLES --output output.txt

To run CYCLIC:
python ./xor_secret_sharing.py --secret "hello world" --n 5 --m 5 --r 2 --CYCLIC --output output.txt


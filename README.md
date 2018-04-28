# xor-secret-sharing

Python application that generates deceptive secrets using an XOR-based scheme

To run NAIVE:
python ./xor_secret_sharing.py --secret "this is my secret" --n 5 --m 5 --NAIVE --output naive_output.txt

To run SIMPLE:
python ./xor_secret_sharing.py --secret "this is my secret" --n 5 --m 5 --SIMPLE --output simple_output.txt

To run CYCLIC:
python ./xor_secret_sharing.py --secret "this is my secret" --n 5 --m 5 --r 2 --CYCLIC --output cyclic_output.txt


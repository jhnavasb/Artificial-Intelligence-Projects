To execute the file, please follow the next steps:

1- Open a terminal
2- cd to the current "RLN.py" location
3- Copy and paste the following line in your terminal "python ./RLN.py -h" or "python3 ./RLN.py -h" to see the different options available
	3.1- The program let you adjust the different variables for the learning:
		 -n number of episodes
		 -a alpha or learning rate
		 -g gamma or discounting rate
		 -e epsilon or exploration rate
	3.2- The program also let you do an "auto" mode in which the program will find the minimum number of episodes needed to find a path.
		 You have to choose between 0 or 1:
		 0 - no "auto" mode
		 1 - with "auto" mode
		 
		 If "auto" mode is activated, the number of episodes will still work as with no "auto" mode, trying to find the path with the specified
		 number of episodes, if a path is not found, then, the "auto" mode will add more episodes and keep trying until finding a path.
		 
	3.3- For example:
		 no "auto": 	python ./RLN.py -n 500 -a 0.5 -g 1 -e 0.1 -t 0
		 with "auto":	python ./RLN.py -n 30 -a 0.5 -g 1 -e 0.1 -t 1
4- Enjoy!

Our team work is formed by
* Andrés Mejía
* Jhonatan Navas

TESTING THE CODE:

1) Add the fork of Electrum we are coding to the environment PATH:

- export PATH=$PATH:<fork_directory> where <fork_directory> is the path of the file '.. /core/electrum_fork'

- cd /usr/bin

- sudo ln -s <fork_directory>/elefork

source ~/.profile

source ~/.bashrc


2) Move to the core folder and test the wrapper.py we're coding (you need to have python 3.6.3 or above installed)

- cd core

- python3

>> import wrapper

>> wrapper.create_from_seed("truly all decline duck apple across note vivid leaf weapon dice plug", wrapper.get_free_wid(), "12345") #this will create a wallet encypted with the password "12345" just outside the repo's folder

>> wrapper.create_from_seed("truly all decline duck apple across note vivid leaf weapon dice plug", wrapper.get_free_wid()) #this will create a wallet without encryption just outside the repo's folder

>> wrapper.get_mpk(1) #you will get the master public key of the first wallet

>> wrapper.get_mpk(2) #you will get the master public key of the second wallet (the same since the seed was the same)




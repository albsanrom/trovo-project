# First, install necessary tools to actually use the program (Firefox, Python, bash, and pip those modules)
# Download geckodriver and put it in a folder, then export the path to the environment

export PATH=$PATH:~/trovo_projects

while IFS=: read -r username password ;
do
  python3.8 account_checker.py $username $password ;
done < account_checker_details.txt

rm -r ../../../tmp/*

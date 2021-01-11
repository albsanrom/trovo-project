PS3=$'\nThis is a Trovo account creator and checker.\n\nPlease select your option: '
options=("Create accounts" "Created accounts" "Check accounts" "Checked accounts" "Quit")
quit=0
while [[ quit -ne 1 ]]; do
    select opt in "${options[@]}"
    do
        case $opt in
            "Create accounts")
                nano account_creator_details.txt
                ./account_creator.sh 
                ;;
            "Created accounts")
                nano created_accounts.txt
                ;;
            "Check accounts")
                nano account_checker_details.txt
                ./account_checker.sh
                ;;
             "Checked accounts")
                nano checked_accounts.txt
                ;;
             "Quit")
                (( quit=quit+1 ))
                break
                ;;
             *) echo "invalid option $REPLY";;
        esac
        break
    done
done

exit

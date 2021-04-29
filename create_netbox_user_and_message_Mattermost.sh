#!/bin/bash


last_name=(BURCIU	BURCIU)
first_name=(Bogdan	Bogdan)	
mail=(Bogdan.Burciu@orange.com	Bogdan.Burciu@orange.com)

for i in "${!last_name[@]}"; do
    ln=${last_name[$i]}
    echo "last name is $ln"
    fn=${first_name[$i]}
    echo "first name is $fn"
    email=${mail[$i]}
    echo "email is $email"
    un=${mail[$i]}      # mail from list/array
    un_string=${un%@*}  # get the text prior to @ in mail
    username=${un_string,,}   # transform to lowercase
    pwd_hash=`echo -n $username | sha384sum`
    password=Pikeo${pwd_hash:0:10}
    echo "username is $username"

    # NetBox: create user account and assign to permissive group
    curl -i -X POST "http://127.0.0.1:8000/api/users/users/" -H  "accept: application/json" -H  "Content-Type: application/json" -H  "Authorization: Token <NETBOX_USER_TOKEN>" -d "{  \"username\": \"$username\",  \"password\": \"$password\",  \"first_name\": \"$fn\",  \"last_name\": \"$ln\",  \"email\": \"$email\",  \"is_staff\": true,  \"is_active\": true,  \"date_joined\": \"2021-04-29T08:27:58.921Z\",  \"groups\": [1]}"

    # send Mattermost private message and inform of password
    curl -i -X POST -d 'payload={"channel": "@'$username'", "text": ":robot: Hey '$fn'. The password for your Pikeo NetBox https://192.168.71.75:8000 account __'$username'__ is __'$password'__ :zipper_mouth_face:. If you want, you can change it after login. For issues, please refer to Bogdan Burciu. Thanks"}' https://mattermost.tech.org/hooks/<MATTERMOST_INCOMING_WEBHOOK>

    wait
done


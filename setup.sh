USER_ID_FILE="/lib/security/pamuser.txt"
PASSWORD_FILE="/lib/security/password.txt"

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

#install the necessary pacakges
apt-get update -y
apt-get install -y python-passlib
apt-get install libpam0g-dev
apt-get install pwgen

password=$(pwgen 50 1)
username="pamuser"

#create new user with random password which we will never need, so we will never store it for security purposes
useradd -m -p $password $username

user_id=$(id -u $username)
group_id=$(id -u $username)

#create a file where we store the gid and uid of this pam user account
touch "$USER_ID_FILE"
chmod 777 "$USER_ID_FILE"

echo "$group_id" >> "$USER_ID_FILE"
echo "$user_id" >> "$USER_ID_FILE"

#setup the password file where we store the eye-tracking passwords
touch "$PASSWORD_FILE"
chown "$user_id" "$PASSWORD_FILE"
chmod 404 "$PASSWORD_FILE"

#setup to allow the wx python to be run by non-privledged users
xhost + local:

#compile the module, store it in the correct location
gcc -fPIC -fno-stack-protector -c /lib/security/simple-pam/src/mypam.c
sudo ld -x --shared -o /lib/security/mypam.so mypam.o

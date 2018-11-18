# Install notifier.py

Use the following install steps on a fresh install of Rasbian to install the notifier:

    .sudo apt-get update
    sudo apt install -y git python3-pip
    git clone https://github.com/burrowsa/christmas-bar.git
    cd christmas-bar
    pip3 install socketIO_client rpi.gpio
    echo "@reboot python3 ${PWD}/notifier.py" > crontab
    crontab crontab
    rm crontab
    sudo reboot

#!/bin/sh

# DIR=./ecert-issuer
# if [ -d "$DIR" ]; then
#     echo "$DIR exists."
# else 
#     echo "$DIR does not exist. Clone project"
#     git clone https://github.com/fungjojo/ecert-issuer.git
# fi

cd ../..
# echo "???? pwd"
# pwd
# touch conf.ini
# echo "issuing_address=0x3c0ba0445c8a3882ac050cc03c45c5ac89f65de9 # matching with the private key above
#    chain=ethereum_ropsten # one of ['ethereum_ropsten', 'ethereum_mainnet']

#    usb_name=/etc/cert-issuer/
#    key_file=pk_issuer.txt

#    unsigned_certificates_dir=/etc/cert-issuer/data/unsigned_certificates
#    blockchain_certificates_dir=/etc/cert-issuer/data/blockchain_certificates
#    work_dir=/etc/cert-issuer/work

#    no_safe_mode" >> conf.ini

# sed -i 's/bitcoin/ethereum/g' app.py

# sudo apt-get update -y
# sudo apt install -y docker.io
# sudo chmod 666 /var/run/docker.sock
# sed -i '/.bitcoin/d' Dockerfile    

# touch pk_issuer.txt
# echo "0xc4097115e76d1fc722ad6ac1fc88b7b31b7baa54ea0ea0b981741f3d85d02f08" >> pk_issuer.txt

# # step 10

# cp examples/data-testnet/unsigned_certificates/verifiable-credential.json data/unsigned_certificates/

# docker build -t bc/cert-issuer:1.0 .
# docker image list

# sudo apt-get update
# sudo apt-get install python-is-python3 python3-pip
# python setup.py experimental --blockchain=ethereum

# pip install -r requirements.txt
# pip install -r ethereum_requirements.txt

# pip install --upgrade pip
# pip install wheel
# pip install coincurve
# echo "arg"
# echo $1
# echo "start time:"
# echo $(date +"%Y-%m-%dT%T.%3N%z")

# echo "??? before sleep"
# sleep 35
# touch sleep.txt
# echo "??? after sleep"
# echo "end time:"
# echo $(date +"%Y-%m-%dT%T.%3N%z")
# docker build -t bc/cert-issuer:1.0 .
sudo sh -c "truncate -s 0 /var/lib/docker/containers/*/*-json.log"
docker run -e ENV_NONCE=$1 --rm --name test1 -d bc/cert-issuer:1.0
# docker start test1
docker logs test1 -f > /tmp/docker_log.log
# cat /etc/cert-issuer/data/blockchain_certificates/test1.json
docker cp test1:/etc/cert-issuer/data/blockchain_certificates /tmp/
docker rm --name test1

# while [ true ]
# do
#     if grep -q "print log" log.txt; then
#         echo "Issue cert done"
#         echo "end time:"
#         echo $(date +"%Y-%m-%dT%T.%3N%z")
#         rm -rf log.txt
#         exit 0
#     fi
# done

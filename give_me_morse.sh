if [ $# = 0 ]
then
    stack_name="morse_stack"
else
    stack_name=$1
fi
# Confirm the existence of required elements.
# - Keypair to inject into the VMs.
keypair_id=$(openstack keypair list | awk '/mykey/ { print $2 }')
echo $keypair_id
# - Free floating ip connected to the public network.
lbaas_ip_id=$(openstack floating ip list | awk '/None/ { print $2 }')
echo $lbaas_ip_id

if [[ -z "$keypair_id" || -z "$lbaas_ip_id" ]]; then
  echo "Please create a keypair and a floating IP for the LBaaS."
  exit 1
fi

echo $stack_name

cd Heat
# heat stack-create -f morse_service.yaml $stack_name
openstack stack create -t morse_service.yaml $stack_name --parameter key_name=$keypair_id --parameter lb_floatingip_id=$lbaas_ip_id
cd ..

echo "Waiting until the stack creation is completed."
while [ $(openstack stack list | awk '/'"$stack_name"'/ { print $6 }') != "CREATE_COMPLETE" ]
do
    echo -n "...."
    sleep 10
done
echo "Starting with Ansible."

cd Ansible
# . install_ansible.sh
. venv/bin/activate
ansible-playbook -u ubuntu -i staging/openstack.py site.yml
# deactivate
cd ..

. test_curl

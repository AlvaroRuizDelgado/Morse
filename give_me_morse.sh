if [ $# = 0 ]
then
    stack_name="morse_stack"
else
    stack_name=$1
fi

echo $stack_name

cd Heat
# heat stack-create -f morse_service.yaml $stack_name
openstack stack create -t morse_service.yaml $stack_name
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

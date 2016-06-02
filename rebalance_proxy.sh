#!/bin/bash
add_to_ring(){
    # $1 = > destworker
    # $2 = > Zone
    # $3 => username
    # $4 => destmaster
    # insert into proxy
    echo "adding to ring $1 in zone$2"
    cd /etc/swift/


    swift-ring-builder account.builder add z$2-$1:6002/sdb1 100
    swift-ring-builder container.builder add z$2-$1:6001/sdb1 100
    swift-ring-builder object.builder add z$2-$1:6000/sdb1 100
}

rebalance_ring(){
    # rebalance the ring
    echo "balancing ring"
    swift-ring-builder /etc/swift/account.builder rebalance
    swift-ring-builder /etc/swift/container.builder rebalance
    swift-ring-builder /etc/swift/object.builder rebalance
    sudo chmod a+rw /etc/swift/*.gz
    sudo swift-init proxy restart


}
copy_to_node(){
    # $1=> node_ip
    # $2=> username 
    # $3=> password
    
    echo "copying to $2@$1"
    fulldestworker=$2@$1
    /usr/bin/sshpass -p $3 ssh ${fulldestworker} -o StrictHostKeyChecking=no 'echo $2 | sudo -S chmod 777 /etc/swift/*'
    /usr/bin/sshpass -p $3 ssh ${fulldestworker} -o StrictHostKeyChecking=no 'echo $2 | sudo -S chown swift:swift /etc/swift/*'
    scp /etc/swift/*.gz ${fulldestworker}:/etc/swift
    /usr/bin/sshpass -p $3 ssh ${fulldestworker} 'echo $2 | sudo -S  swift-init all restart'


}

change_permission(){
#$1 username
#$2 password
  echo $2| sudo -S chown -R $1:$1 /etc/swift/
  echo $2| sudo -S chmod 777 /etc/swift/*

}

username="cloudsys"
password="cloudsys"
destmaster=proxy
mkdir -p ./logs
zonename=1

change_permission $username $password


for destworker in $(<~/workers); do
  echo "running"
  if [[ $destworker =~ ^[^\#] ]]
  then
     #fulldestworker=$username'@'$destworker
     echo $destworker $destmaster $username
     
     add_to_ring  $destworker $zonename $username $destmaster

     #copy_to_node $destworker $username
  fi
done

rebalance_ring

#for destworker in $(<~/workers); do
#  copy_to_node $destworker $username $password
#done

wait


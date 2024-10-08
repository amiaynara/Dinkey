#!/bin/bash

# Define variables
IMAGE_ID="ami-0dee22c13ea7a9a67"
INSTANCE_TYPE="t2.micro"
KEY_NAME="onprem-keypair"
SECURITY_GROUP_ID="sg-04a994513079424e1"
TAG_SPEC="ResourceType=instance,Tags=[{Key=Name,Value=onprem-burner},{Key=Type,Value=onprem-testing}]"
REGION="ap-south-1"
DEVICE_NAME="/dev/sdh"  # This will be the device name for the additional EBS volume

# Run an EC2 instance with an additional 8 GB EBS volume
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $IMAGE_ID \
    --count 1 \
    --region $REGION \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --tag-specifications $TAG_SPEC \
    --block-device-mappings "[{\"DeviceName\":\"/dev/sda1\",\"Ebs\":{\"VolumeSize\":20}},{\"DeviceName\":\"$DEVICE_NAME\",\"Ebs\":{\"VolumeSize\":8}}]" \
    --associate-public-ip-address \
    --query "Instances[0].InstanceId" \
    --output text)

if [ -z "$INSTANCE_ID" ]; then
    echo "Failed to create the EC2 instance."
    exit 1
fi

echo "Instance ID: $INSTANCE_ID"
echo "Retrieving the public IP address..."

# Wait until the instance is running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION

# Retrieve the public IP address
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --region $REGION \
    --query "Reservations[0].Instances[0].PublicIpAddress" \
    --output text)

if [ -z "$PUBLIC_IP" ]; then
    echo "Failed to retrieve the public IP address."
    exit 1
fi

echo "EC2 instance is running. Public IP address: $PUBLIC_IP"
echo "waiting for 10 sec..."
# $TAR_ARCHIVE="$1"
sleep 10
echo "ssh -i ~/work/aws-keys/onprem-keypair.pem ubuntu@$PUBLIC_IP"
echo "scp -i ~/work/aws-keys/onprem-keypair.pem $1 ubuntu@$PUBLIC_IP:~/"
# echo "scp -i ~/work/aws-keys/onprem-keypair.pem /Users/amiaynarayan/work/scripts/aws/mount_ebs.sh ubuntu@$PUBLIC_IP:~/"
#scp -i ~/work/aws-keys/onprem-keypair.pem ./onprem_0.0.1_all.deb ubuntu@$PUBLIC_IP:~/
# scp -i ~/work/aws-keys/onprem-keypair.pem /Users/amiaynarayan/work/scripts/aws/mount_ebs.sh ubuntu@$PUBLIC_IP:~/
scp -i ~/work/aws-keys/onprem-keypair.pem $1 ubuntu@$PUBLIC_IP:~/


# # Terminate the EC2 instance
# echo "Terminating the EC2 instance..."
# aws ec2 terminate-instances --region $REGION --instance-ids $INSTANCE_ID

# # Wait until the instance is terminated
# aws ec2 wait instance-terminated --instance-ids $INSTANCE_ID

# echo "EC2 instance terminated."
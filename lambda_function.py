import boto3

def lambda_handler(event, context):
    # On connecte boto3 au LocalStack local
    ec2 = boto3.client('ec2', endpoint_url="http://localhost:4566", region_name="us-east-1")
    
    action = event.get('action')
    instance_id = event.get('instance_id')
    
    if action == 'start':
        ec2.start_instances(InstanceIds=[instance_id])
        return {"message": f"Demarrage en cours de l'instance {instance_id}"}
    elif action == 'stop':
        ec2.stop_instances(InstanceIds=[instance_id])
        return {"message": f"Arret en cours de l'instance {instance_id}"}
    else:
        return {"message": "Action inconnue. Utilisez 'start' ou 'stop'."}

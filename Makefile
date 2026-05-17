
compose_up:
	docker compose up -d --build

compose_down:
	docker compose down

swarm_init:
	docker swarm init

swarm_deploy:
	docker compose build
	docker stack deploy -c docker-compose.yaml sre_stack

swarm_remove:
	docker stack rm sre_stack

terraform_init:
	cd terraform && terraform init

terraform_plan:
	cd terraform && terraform plan

terraform_apply:
	cd terraform && terraform apply -auto-approve

terraform_destroy:
	cd terraform && terraform destroy -auto-approve

ansible_deploy:
	cd ansible && wsl cp ./assignment-key.pem ~/assignment-key.pem
	wsl chmod 600 ~/assignment-key.pem
	wsl ls -l ~/assignment-key.pem
	cd ansible && wsl -d Ubuntu -- ansible-playbook -i inventory.ini playbook.yml
#!/bin/bash
VERSION=${1-001}
home=$(pwd)
function build-and-push(){
	docker build -t tahootyhoot/hootcache:"${VERSION}"
	docker push tahootyhoot/hootcache:"${VERSION}"
}

function launch_cluster(){
	minikube start
	installed=$(minikube addons list | grep 'ingress: enabled')
	if [[ -z $installed ]]; then minikube addons enable ingress; fi
}
function run(){
	installed=$(minikube addons list | grep 'ingress: enabled')
	if [[ -z $installed ]]; then minikube addons enable ingress ; fi
	kubectl apply -f deploy_artifacts/memcache.yaml  
	kubectl expose deployment memcache-hoot --type=NodePort --port=11211 --labels app='hootcache' && service=$(minikube service memcache-hoot --url)
	echo $service
	sed -e "s|SERVICE_VALUE|"${service}"|g" deploy_artifacts/hootcache.yml > deploy_artifacts/hootcache.yaml
	kubectl apply -f deploy_artifacts/hootcache.yaml
	kubectl expose deployment hootcache-api --type=LoadBalancer --labels app='hootcache' --port=5000 && api=$(minikube service hootcache-api --url)
	echo "Send Curl and postman requests to $api/hootcache/api/v1.0/files" 
}


function clean_services(){
	kubectl delete deployments -l app=hootcache
	kubectl delete services -l app=hootcache
}

function run_local(){
	docker run -d -p 11211:11211 tahootyhoot/memcache-hoot
	python3 app/app.py "localhost:11211"
}

function clean_cluster(){
	minikube stop 
}
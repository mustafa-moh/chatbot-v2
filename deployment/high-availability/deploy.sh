#!/bin/bash

NAMESPACE_PROD="chatbot-prod"

helm repo add bitnami https://charts.bitnami.com/bitnami

## Create default storage class on aws eks
kubectl apply -f storage-class.yaml

kubectl apply -f namespace.yaml
kubectl apply -f app-config.yaml
kubectl apply -f secrets.yaml

helm install redis bitnami/redis --version 20.7.0 \
        --namespace $NAMESPACE_PROD \
        -f redis-values.yaml \
        --wait

helm install mongodb bitnami/mongodb --version 16.4.3 \
        --namespace $NAMESPACE_PROD \
        -f mongodb-values.yaml \
        --wait

kubectl apply -f api-hpa.yaml

# Deploy Application Server
kubectl apply -f app-deployment.yaml

# Deploy Frontend
kubectl apply -f frontend-deployment.yaml

echo "Deployment completed!"
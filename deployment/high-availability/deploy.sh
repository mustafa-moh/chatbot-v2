#!/bin/bash

NAMESPACE_PROD="chatbot-prod"

helm repo add bitnami https://charts.bitnami.com/bitnami

kubectl apply -f namespace.yaml

helm install redis bitnami/redis --version 20.7.0 \
        --namespace $NAMESPACE_PROD \
        --values redis-values.yaml \
        --wait

helm install mongodb bitnami/mongodb --version 16.4.3 \
        --namespace $NAMESPACE_PROD \
        --values mongodb-values.yaml \
        --wait

# Apply secrets
kubectl apply -f secrets.yaml
kubectl apply -f app-config.yaml

# Deploy MongoDB
kubectl apply -f mongo-deployment.yaml

# Deploy Redis
kubectl apply -f redis-deployment.yaml

# Deploy Application Server
kubectl apply -f app-deployment.yaml

# Deploy Frontend
kubectl apply -f frontend-deployment.yaml

echo "Deployment completed!"
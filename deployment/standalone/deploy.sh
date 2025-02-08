#!/bin/bash

kubectl apply -f namespace.yaml

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
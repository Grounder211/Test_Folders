#!/bin/bash
# Complete setup script - everything in one file!

set -e

echo "🚀 Setting up Python File Server CI/CD Pipeline..."

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    sudo usermod -aG docker $USER
fi

# Install kubectl
if ! command -v kubectl &> /dev/null; then
    echo "☸️ Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
fi

# Install kind for local Kubernetes
if ! command -v kind &> /dev/null; then
    echo "🔧 Installing kind..."
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
fi

# Create Kubernetes cluster
echo "🏗️ Creating Kubernetes cluster..."
cat > kind-config.yaml << EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
  - containerPort: 443
    hostPort: 443
- role: worker
- role: worker
EOF

kind create cluster --config=kind-config.yaml --name=file-server

# Install NGINX Ingress
echo "🌐 Installing NGINX Ingress..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s

# Create storage class
kubectl apply -f - << EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
EOF

# Generate self-signed certificate
echo "🔐 Generating HTTPS certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout tls.key -out tls.crt \
    -subj "/CN=file-server.local/O=FileServer"

kubectl create secret tls file-server-tls \
    --cert=tls.crt --key=tls.key \
    -n file-server --dry-run=client -o yaml | kubectl apply -f -

# Setup Jenkins with Docker
echo "🔨 Setting up Jenkins..."
docker run -d --name jenkins \
    -p 8080:8080 -p 50000:50000 \
    -v jenkins_home:/var/jenkins_home \
    -v /var/run/docker.sock:/var/run/docker.sock \
    --group-add $(getent group docker | cut -d: -f3) \
    jenkins/jenkins:lts

echo "⏳ Waiting for Jenkins to start..."
sleep 30

echo "🎉 Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Jenkins: http://localhost:8080"
echo "   Initial password: $(docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword)"
echo ""
echo "2. Add to /etc/hosts:"
echo "   127.0.0.1 file-server.local"
echo ""
echo "3. Deploy the application:"
echo "   ./deploy.sh"

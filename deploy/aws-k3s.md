# Kubernetes na AWS (créditos de conta nova) — k3s numa EC2

O EKS (Kubernetes gerenciado da AWS) **não tem free tier** — o control plane
sozinho custa ~US$73/mês. Este guia usa **k3s** (distribuição Kubernetes leve,
certificada CNCF — é Kubernetes de verdade: `kubectl`, os mesmos manifests de
`deploy/k8s/`) numa única instância EC2, coberta pelos créditos de conta nova
da AWS (tipicamente US$100-200 por 6 meses). Custo real: ~zero enquanto os
créditos durarem.

## 1. Subir a instância

- Console AWS → EC2 → Launch instance
- AMI: **Ubuntu 22.04 LTS**
- Tipo: `t3.small` (2 vCPU/2GB) é suficiente para 1 réplica da API
- Storage: 20GB gp3
- Security Group: liberar portas **22** (SSH), **80** e **443** (HTTP/HTTPS)
- Aloque um **Elastic IP** e associe à instância (IP fixo — necessário para o sslip.io)

## 2. Instalar k3s (1 comando)

```bash
ssh ubuntu@SEU_IP_ELASTICO
curl -sfL https://get.k3s.io | sh -
sudo k3s kubectl get nodes   # confirma o node Ready
mkdir -p ~/.kube && sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
```

k3s já vem com o **Traefik** (ingress controller) instalado — não precisa
instalar nada além disso para expor a API.

## 3. cert-manager (HTTPS grátis via Let's Encrypt)

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
kubectl wait --for=condition=Available deployment --all -n cert-manager --timeout=120s
```

Crie o ClusterIssuer (`deploy/k8s/cluster-issuer.yaml` — ajuste o e-mail):

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata: { name: letsencrypt-prod }
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: SEU_EMAIL@exemplo.com
    privateKeySecretRef: { name: letsencrypt-prod }
    solvers:
      - http01: { ingress: { ingressClassName: traefik } }
```

```bash
kubectl apply -f deploy/k8s/cluster-issuer.yaml
```

## 4. Publicar a imagem e aplicar os manifests

A imagem é a mesma do Hugging Face Space (`deploy/hf-space/Dockerfile`):

```bash
# numa máquina com Docker (ou na própria EC2):
docker build -t ghcr.io/SEU_USUARIO/anti-ruido-api:latest -f deploy/hf-space/Dockerfile .
docker push ghcr.io/SEU_USUARIO/anti-ruido-api:latest
```

Edite `deploy/k8s/deployment.yaml` (campo `image:`) e `deploy/k8s/ingress.yaml`
(troque `SEU.IP.PUBLICO.AQUI` pelo Elastic IP com pontos trocados por hífen,
ex. IP `3.85.12.9` → host `anti-ruido.3-85-12-9.sslip.io`), depois:

```bash
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml
kubectl apply -f deploy/k8s/ingress.yaml
kubectl get certificate   # aguardar READY=True (~1-2 min)
curl https://anti-ruido.SEU-IP-COM-HIFENS.sslip.io/api/health
```

## 5. Apontar o site para essa URL

Trocar `API_BASE` em `site/demo.html` pela URL do sslip.io e fazer push — o
Cloudflare redeploya o site automaticamente (ver README principal).

## Por que sslip.io em vez de um domínio

`sslip.io` resolve `anti-ruido.<IP>.sslip.io` para `<IP>` automaticamente —
DNS "de graça", sem comprar domínio nem configurar Route53. Quando/se
comprarem um domínio de verdade, é só trocar o `host:` do Ingress.

## Monitorar os créditos

Console AWS → Billing → Credits. Quando esgotarem, ou destrua a instância
(`Terminate` no console) ou migre de volta para o Hugging Face Space (grátis
permanente) — o código e a imagem são os mesmos, não há vendor lock-in.

# Deploy Elasticsearch with Docker Stack and Persistent Storage

This guide explains how to deploy a single-node Elasticsearch setup using Docker Swarm (`docker stack deploy`) with persistent storage.

## 🧰 Prerequisites

- Docker installed
- Docker Swarm initialized (`docker swarm init`)

---

## 📦 Step 1: Create the Docker Compose File

Make sure the [`docker-stack.yml`](./../docker-stack.yml) file is present in the same directory with the following content.

---

## 🚀 Step 2: Deploy elastic-search Service

```bash
docker stack deploy -c docker-stack.yml elasticsearch  # to create service
```
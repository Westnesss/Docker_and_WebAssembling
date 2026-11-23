# 🐳 Docker Container PoC - FICA UCE

> **Course:** Software Architecture
> **Faculty / Program:** FICA — Information Systems Engineering, Universidad Central del Ecuador (UCE)
> **Topic chosen:** Docker (over WebAssembly)

| Team member | GitHub |
|---|---|
| `Member 1 — Full Name` | `@username` |
| `Member 2 — Full Name` | `@username` |
| `Member 3 — Full Name` *(optional)* | `@username` |

---

## Table of Contents

1. [What is Docker?](#1-what-is-docker)
2. [How does it work?](#2-how-does-it-work)
3. [Where can we use it?](#3-where-can-we-use-it)
4. [Who is implementing it?](#4-who-is-implementing-it)
5. [Who created it?](#5-who-created-it)
6. [So what? (Why does it matter?)](#6-so-what-why-does-it-matter)
7. [The Proof of Concept](#7-the-proof-of-concept)
8. [How to run the PoC](#8-how-to-run-the-poc)
9. [References](#9-references)

---

## 1. What is Docker?

**Docker** is an open-source platform for **building, shipping and running applications inside containers**.
A *container* is a lightweight, isolated process that bundles an application together with everything it needs to run — code, runtime, system libraries and configuration — so it behaves the same on a developer's laptop, a test server or a cloud cluster.

In short: Docker solves the classic *"it works on my machine"* problem by packaging the **machine environment** together with the application.

---

## 2. How does it work?

### OS-level virtualization

Unlike a Virtual Machine (VM), which emulates hardware and boots a full guest operating system on top of a hypervisor, Docker uses **OS-level virtualization**: all containers **share the host's Linux kernel**, and the kernel isolates them from one another. This makes containers start in milliseconds and use only megabytes of overhead.

```
        Virtual Machines                         Containers (Docker)
┌─────────┬─────────┬─────────┐       ┌─────────┬─────────┬─────────┐
│  App A  │  App B  │  App C  │       │  App A  │  App B  │  App C  │
│  Libs   │  Libs   │  Libs   │       │  Libs   │  Libs   │  Libs   │
│Guest OS │Guest OS │Guest OS │       ├─────────┴─────────┴─────────┤
├─────────┴─────────┴─────────┤       │        Docker Engine         │
│         Hypervisor          │       ├─────────────────────────────┤
├─────────────────────────────┤       │   Host OS (shared kernel)    │
│      Host OS / Hardware     │       ├─────────────────────────────┤
└─────────────────────────────┘       │          Hardware            │
                                      └─────────────────────────────┘
```

### The two Linux kernel features behind containers

| Feature | What it does | Example |
|---|---|---|
| **Namespaces** | **Isolation** — they control *what a process can see*. Each container gets its own view of processes (`pid`), network interfaces (`net`), filesystem mounts (`mnt`), hostname (`uts`), IPC and users (`user`). | Inside the container, the app sees itself as **PID 1** and has its own hostname. |
| **Control groups (cgroups)** | **Resource limiting** — they control *how much a process can use*: CPU, memory, disk I/O, number of processes. | `docker run --memory=64m --cpus=0.5` caps the container. |

A third ingredient is a **layered union filesystem** (e.g. *OverlayFS*): images are built from read-only layers stacked on top of each other, and each container adds a thin writable layer on top. Layers are cached and shared, so images are fast to build and cheap to store.

### Docker Engine (architecture)

Docker follows a **client–server architecture**:

```
 docker CLI  ──REST API──►  dockerd (Docker daemon)  ──►  containerd  ──►  runc  ──►  container
 (client)                   builds images, manages        manages container      creates namespaces
                            networks & volumes            lifecycle              & cgroups (OCI runtime)
                                   │
                                   └──► Registry (Docker Hub, GHCR, ECR…)  push / pull images
```

- **Docker CLI** — the `docker` command the user types.
- **Docker daemon (`dockerd`)** — the background service that does the actual work.
- **containerd / runc** — lower-level runtimes that talk to the kernel, following the **Open Container Initiative (OCI)** standard.
- **Registry** — a store for images (Docker Hub is the public default).

### Images vs. Containers

| | **Image** | **Container** |
|---|---|---|
| What it is | A **read-only template** (blueprint) | A **running instance** of an image |
| Analogy | A *class* in OOP | An *object* of that class |
| Created by | `docker build` from a `Dockerfile` | `docker run <image>` |
| State | Immutable, versioned with tags (`app:1.0`) | Has a writable layer; can be started, stopped, deleted |
| Multiplicity | One image… | …can spawn many containers |

**Workflow:** `Dockerfile` → `docker build` → **Image** → `docker push/pull` → `docker run` → **Container**

---

## 3. Where can we use it?

- **Local development** — every developer gets an identical environment (DB, cache, API) with a single `docker compose up`.
- **CI/CD pipelines** — builds and tests run in clean, reproducible containers (GitHub Actions, GitLab CI, Jenkins).
- **Microservices architectures** — each service is packaged, deployed and scaled independently.
- **Cloud & hybrid deployments** — the same image runs on AWS, Azure, Google Cloud or on-premise servers.
- **Container orchestration** — Kubernetes, Docker Swarm and Amazon ECS schedule containers at scale.
- **Legacy application modernization** — wrapping old apps in containers to move them to the cloud.
- **Data science & ML** — reproducible notebooks, model training and model serving environments.
- **Edge & IoT** — lightweight images running on small devices (ARM boards, gateways).
- **Education & testing** — spin up disposable environments (databases, tools) in seconds and delete them afterwards.

---

## 4. Who is implementing it?

Docker and containers are an industry standard. Some well-known adopters:

| Company | How they use containers |
|---|---|
| **Netflix** | Runs large-scale workloads on *Titus*, its own container management platform. |
| **Spotify** | Early adopter of Docker for microservices; created the *Helios* orchestrator. |
| **PayPal** | Migrated thousands of applications to containers to standardize deployment. |
| **Uber, Airbnb, Shopify** | Microservice platforms built on containers and Kubernetes. |
| **Google** | Has run everything in containers for years (Borg), which inspired Kubernetes. |
| **AWS, Microsoft Azure, Google Cloud** | Offer managed container services: ECS/EKS, AKS/ACI, GKE/Cloud Run. |
| **GitHub / GitLab** | CI runners execute jobs inside Docker containers. |

Beyond big tech, banks, governments, universities and startups use Docker daily — containers are now a default skill expected of software engineers.

---

## 5. Who created it?

- **Creator:** **Solomon Hykes**, founder of **dotCloud**, a Platform-as-a-Service (PaaS) startup.
- **Origin:** Docker started as an internal dotCloud tool and was **released as open source in March 2013**, first shown publicly at PyCon 2013 ("The future of Linux Containers").
- **Docker, Inc.:** In late 2013 dotCloud renamed itself **Docker, Inc.** to focus entirely on the new technology.
- **Evolution:** Early versions were built on LXC; Docker later wrote its own runtime (*libcontainer*, now **runc**) and in 2015 helped found the **Open Container Initiative (OCI)** under the Linux Foundation to standardize image and runtime formats.
- Docker is written in the **Go** programming language.

---

## 6. So what? (Why does it matter?)

| Benefit | Why it matters for software architecture |
|---|---|
| **Portability** | "Build once, run anywhere" — the same image runs on any host with a container runtime. |
| **Consistency** | Dev, test and production use the exact same environment → fewer deployment bugs. |
| **Efficiency** | Containers share the kernel: they start in seconds and use far fewer resources than VMs, so more workloads fit on the same hardware. |
| **Isolation** | Dependencies of one app don't conflict with another (e.g. Python 3.8 and 3.12 side by side). |
| **Scalability** | Containers are the building block of microservices and orchestration (Kubernetes), enabling horizontal scaling. |
| **DevOps & automation** | Infrastructure becomes code (`Dockerfile`, `docker-compose.yml`), versioned in Git and automated in CI/CD. |

**Bottom line:** Docker changed *how software is delivered*. It turned the server environment into a versioned, shareable artifact, which made microservices, cloud-native architectures and modern DevOps practical for everyone.

**Limitations to keep in mind:** containers share the host kernel (weaker isolation than VMs), Linux containers need a Linux kernel (Docker Desktop uses a lightweight VM on Windows/macOS), and persistent data requires volumes.

---

## 7. The Proof of Concept

A lightweight **container status dashboard**: a zero-dependency Python 3 HTTP server (`http.server`) packaged in a multi-stage Alpine image. When the container is running, the page at <http://localhost:8080> shows:

- A live green **"Container Running"** badge.
- **Container hostname** (the container ID, not your PC's name → UTS namespace in action).
- **OS / Platform** (Alpine Linux userland running on the host's shared kernel).
- **Runtime** version (Python 3.11).
- **Server timestamp** (refreshed every 5 seconds from the backend).
- A summary card explaining the container architecture.

### Project structure

```
docker-container-poc/
├── app/
│   ├── index.html       # Light-themed dashboard (embedded CSS + vanilla JS)
│   └── server.py        # Zero-dependency HTTP server: /, /api/status, /health
├── Dockerfile           # Multi-stage python:3.11-alpine, non-root, HEALTHCHECK
├── docker-compose.yml   # Service "docker-poc" mapped to 8080:8080
├── .dockerignore
├── .gitignore
└── README.md
```

### Endpoints

| Route | Description |
|---|---|
| `GET /` | Dashboard (`index.html`) |
| `GET /api/status` | JSON container metadata: `hostname`, `platform`, `os`, `runtime`, `timestamp` |
| `GET /health` | Liveness probe used by the Docker `HEALTHCHECK` |

### Dockerfile highlights

- **Multi-stage build:** the `builder` stage byte-compiles the code; the final stage copies only the app.
- **`python:3.11-alpine`** base → small image (~50 MB).
- Runs as an unprivileged **non-root user** (`appuser`).
- **`EXPOSE 8080`** and a **`HEALTHCHECK`** so `docker ps` reports `(healthy)`.

---

## 8. How to run the PoC

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) or Docker Engine (Linux).

```bash
docker --version
```

Clone the repository:

```bash
git clone https://github.com/<your-user>/docker-container-poc.git
cd docker-container-poc
```

### Option A — Docker Compose (recommended)

```bash
docker-compose up --build
```

> On newer Docker versions you can also use `docker compose up --build` (without the hyphen).
> Add `-d` to run it in the background.

Open 👉 **<http://localhost:8080>**

Stop and remove:

```bash
docker-compose down
```

### Option B — `docker build` + `docker run`

```bash
# 1. Build the image
docker build -t docker-poc:1.0 .

# 2. Run the container (detached, port 8080 → 8080)
docker run -d --name docker-poc -p 8080:8080 docker-poc:1.0
```

Open 👉 **<http://localhost:8080>**

### Verify the PoC

```bash
# Container is up; after a few seconds STATUS shows "(healthy)"
docker ps

# JSON metadata from the backend
curl http://localhost:8080/api/status

# Health endpoint used by the HEALTHCHECK
curl http://localhost:8080/health

# Server logs
docker logs docker-poc

# Image size
docker images docker-poc
```

Expected `/api/status` response (values vary):

```json
{
  "status": "running",
  "hostname": "3f2a9c1b7e4d",
  "platform": "Linux 6.6.x (x86_64)",
  "os": "Alpine Linux v3.20",
  "runtime": "Python 3.11.x",
  "in_container": true,
  "timestamp": "2026-11-23T22:30:00+00:00"
}
```

> On Windows PowerShell, use `curl.exe` or simply open the URLs in the browser.

### Clean up

```bash
docker rm -f docker-poc
docker rmi docker-poc:1.0
```

---

## 9. References

- Docker Docs — Overview: <https://docs.docker.com/get-started/docker-overview/>
- Docker Docs — Dockerfile best practices: <https://docs.docker.com/build/building/best-practices/>
- Docker Docs — Multi-stage builds: <https://docs.docker.com/build/building/multi-stage/>
- Python docs — `http.server`: <https://docs.python.org/3/library/http.server.html>
- Open Container Initiative: <https://opencontainers.org/>
- Linux man pages — `namespaces(7)`, `cgroups(7)`: <https://man7.org/linux/man-pages/man7/namespaces.7.html>
- Solomon Hykes, *"The future of Linux Containers"*, PyCon 2013.

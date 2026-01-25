# =========================
# Configuration
# =========================

PROJECT=bafa.kubernetes
OWNER=thomas.brunko

NAMESPACE := demo
KUBECTL   := kubectl
DOCKER   := docker

MS_RANDOM_IMAGE_1    := ms-random:1.0.0
MS_RANDOM_IMAGE_2    := ms-random:2.0.0
MS_TEMPERATURE_IMAGE := ms-temperature:1.0.0
FRONTEND_IMAGE       := frontend:1.0.0

DOCKER_OPTS := --label "PROJECT=$(PROJECT)" --label "OWNER=$(OWNER)" --progress=plain 
# DOCKER_OPTS += --no-cache

# =========================
# Targets
# =========================
.PHONY: all build deploy clean

all: build deploy

# -------------------------
# Build
# -------------------------
build: build-random build-temperature build-frontend

build-random: build-random-1 build-random-2

build-random-1:
	$(DOCKER) build $(DOCKER_OPTS) -t $(MS_RANDOM_IMAGE_1) --build-arg "VERSION=1.0.0" ms-random

build-random-2:
	$(DOCKER) build $(DOCKER_OPTS) -t $(MS_RANDOM_IMAGE_2) --build-arg "VERSION=2.0.0" ms-random

build-temperature:
	$(DOCKER) build $(DOCKER_OPTS) -t $(MS_TEMPERATURE_IMAGE) --build-arg "VERSION=1.0.0" ms-temperature

build-frontend:
	$(DOCKER) build --no-cache $(DOCKER_OPTS) -t $(FRONTEND_IMAGE) frontend

# -------------------------
# Deploy
# -------------------------
deploy:
	$(KUBECTL) create namespace $(NAMESPACE) --dry-run=client -o yaml | $(KUBECTL) apply -f -
	$(KUBECTL) apply -n $(NAMESPACE) -f k8s/v1/

# -------------------------
# Clean
# -------------------------
clean:
	$(KUBECTL) delete namespace $(NAMESPACE) --ignore-not-found

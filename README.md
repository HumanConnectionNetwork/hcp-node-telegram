# HCP Client — Telegram
+-------------------------------+
|     Telegram User             |
+---------------+---------------+
                |
                v
+-------------------------------+
|     HCP Telegram Client       |
+---------------+---------------+
                |
                v
+-------------------------------+
|  Canonical HCP Humanitarian   |
|          Record               |
+---------------+---------------+
                |
                v
+-------------------------------+
|   Local Storage (MVP)         |
| Future: HCP Node API          |
+-------------------------------+

> The first official client implementation of the **Humanitarian Connection Protocol (HCP)**.

![Status](https://img.shields.io/badge/status-Production%20MVP-success)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Protocol](https://img.shields.io/badge/HCP-v0.1-orange)

---
## Learn More

- **Human Connection Network:** https://github.com/HumanConnectionNetwork/human-connection-network
- **Humanitarian Connection Protocol:** https://github.com/HumanConnectionNetwork/hcp-specification

- ## Project Status

✅ Production MVP

Current implementation includes:

- Humanitarian Record creation
- Humanitarian Record search
- Local correlation engine
- Search by Report ID
- Docker deployment
- Production deployment

# Overview

This repository contains the first production implementation of an **HCP Client**.

The Telegram Bot allows anyone to create and search **Humanitarian Records** using a standardized, open and interoperable protocol designed for humanitarian emergencies.

It demonstrates how HCP can be used by real people without requiring a custom application, making humanitarian reporting immediately accessible from one of the world's most widely used messaging platforms.

The client is intentionally lightweight.

Its responsibility is to collect structured humanitarian observations, build Canonical HCP Records, perform local correlation when appropriate, and communicate with HCP Nodes through the protocol.

---

# The Problem

During humanitarian emergencies, information becomes fragmented.

Families, hospitals, volunteers, shelters, rescue teams and governments often collect the same information using incompatible systems.

This creates:

- duplicated reports
- inconsistent information
- isolated databases
- difficult searches
- poor interoperability
- slower reunification of people and animals

HCP proposes a different approach.

Instead of sharing databases, independent systems share a common language.

---

# What is HCP?

The **Humanitarian Connection Protocol (HCP)** is an open protocol that standardizes humanitarian observations.

It is **not** a centralized platform.

It is **not** a database.

It is an interoperability standard.

Any application can implement HCP while maintaining complete control over its own infrastructure.

---

# Role of this Repository

This project implements an **HCP Client**.

Its responsibilities include:

- Collect humanitarian information from Telegram users
- Build Canonical HCP Records
- Validate user input
- Search existing records
- Explain correlation results
- Store records locally (MVP)
- Communicate with HCP Nodes (future distributed mode)

The client does **not** define the protocol.

The protocol is specified in the HCP Specification repository.

---

# Current Features

## Create Humanitarian Records

### People

- Missing Person
- Hospitalized Person
- Sheltered Person
- Located Person
- Public Emergency

### Animals

- Missing Animal
- Found Animal

---

## Search Humanitarian Records

Search by:

- Name
- Estimated Age
- Species
- Size
- Breed
- Location
- Visible Characteristics

The client performs local correlation and returns the most probable matching cases.

Each result includes an explainable correlation score.

---

## Search by Report ID

Every Humanitarian Record receives a unique UUID.

The bot allows direct retrieval of a record using its Report ID.

---

## Multilingual Architecture

Current language:

- Spanish

Planned:

- English
- Portuguese

The localization system was designed to support additional languages contributed by the community.

---

# Architecture

```
Telegram User
        │
        ▼
Telegram Bot
        │
        ▼
Conversation Flow
        │
        ▼
Canonical HCP Record
        │
        ▼
Local Storage (MVP)
        │
        ▼
Future HCP Node API
```

---

# Project Structure

```
app/

├── bot.py
├── config.py
├── conversation/
├── hcp/
├── locales/
├── models/
├── search/
└── storage/
```

Main components:

| Folder | Purpose |
|----------|----------|
| conversation | Telegram conversation flows |
| hcp | Canonical HCP Record builder |
| search | Correlation engine |
| storage | Local record storage |
| locales | User interface translations |

---

# Running Locally

## Requirements

- Python 3.12+
- Telegram Bot Token

Clone the repository:

```bash
git clone https://github.com/HumanConnectionNetwork/hcp-client-telegram.git

cd hcp-client-telegram
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example environment:

```bash
cp .env.example .env
```

Configure:

```
TELEGRAM_BOT_TOKEN=YOUR_TOKEN
```

Run:

```bash
python main.py
```

---

# Running with Docker

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

---

# Current Storage Model

The current MVP stores records locally as JSON.

This allows:

- simple deployment
- offline experimentation
- protocol validation

Future versions will communicate with independent HCP Nodes using the standardized Node API.

---

# Ecosystem

This repository is part of the Human Connection Network ecosystem.

| Repository | Purpose |
|------------|----------|
| human-connection-network | Project overview |
| hcp-specification | Official HCP specification |
| hcp-reference | Reference HCP Node |
| hcp-client-telegram | Telegram Client |

---

# Roadmap

Planned improvements include:

- HCP Node integration
- Distributed search
- Online synchronization
- English localization
- Portuguese localization
- Media support (if adopted by the protocol)
- Additional client implementations

---

# Contributing

We welcome contributors interested in:

- Python
- Telegram Bots
- Humanitarian Technology
- Distributed Systems
- Protocol Design
- Localization
- Documentation
- Testing

Please read:

- CONTRIBUTING.md
- CODE_OF_CONDUCT.md

before submitting pull requests.

---

# License

Licensed under the Apache License 2.0.

---

# Human Connection Network

Humanitarian technology should be interoperable.

Not because every organization should use the same software.

But because every person deserves to be found, regardless of which software collected the information.

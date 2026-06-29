# HCP Node

> Reference implementation of the Human Connection Protocol (HCP).

HCP Node is the first reference implementation of the **Human Connection Protocol (HCP)**, an open standard for exchanging humanitarian information between applications, organizations, governments, volunteers, and communities.

This project provides the core building blocks required to operate an HCP node, including:

* 🤖 Telegram Bot
* 🌐 REST API
* 🗄️ Humanitarian Records Database
* 🔄 HCP Data Exchange
* 📜 Record History & Traceability
* 🔍 Search & Query Services
* 🤝 Integration with external humanitarian platforms

The objective is not to replace existing humanitarian tools, but to allow them to communicate through a common language.

---

# Vision

During humanitarian emergencies, thousands of volunteers and organizations create incredible solutions.

Unfortunately, most of these systems operate in isolation.

The Human Connection Protocol enables interoperability between them by defining a common structure for humanitarian information.

Every HCP Node contributes to a distributed humanitarian network where information can be shared securely, transparently, and efficiently.

# Core Principles

* Humanity First
* Open Standards
* Interoperability
* Transparency
* Traceability
* Privacy by Design
* Decentralization
* AI-Ready Architecture

# Features

Current roadmap includes:

* Telegram Bot
* REST API
* HCP Record Management
* Humanitarian Resource Registry
* Missing Persons Registry
* Shelters Registry
* Medical Centers Registry
* Volunteers Registry
* Duplicate Detection
* Confidence Scoring
* Event History
* OpenAPI Documentation


# Architecture

                  Human Connection Protocol

                          REST API
                              │
      ┌───────────────────────┼────────────────────────┐
      │                       │                        │
 Telegram Bot           Web Platform           Future Applications
      │                       │                        │
      └───────────────────────┼────────────────────────┘
                      HCP Core Services
                              │
                    Humanitarian Database


# Project Structure

text
hcp-node/

app/
    bot.py
    api.py
    database.py
    models.py
    hcp.py
    config.py

docs/

schemas/

examples/

tests/

requirements.txt


# Humanitarian Record Lifecycle

Every humanitarian record follows a complete lifecycle.

Created
    │
Verified
    │
Updated
    │
Merged (if duplicated)
    │
Resolved
    │
Archived

No information is deleted.

Every modification is preserved in the record history.


# HCP Records

Each report is converted into a standardized HCP record.

Example:

json
{
  "id": "hcp:ve:person:000001",
  "version": "0.1",
  "type": "person_missing",
  "status": "active",
  "created_at": "2026-06-29T20:00:00Z",
  "updated_at": "2026-06-29T20:00:00Z",
  "confidence": 40,
  "source": {
    "platform": "telegram"
  }
}


# Roadmap

## Phase 1

* Telegram Bot
* Local Database
* REST API
* HCP JSON Records

## Phase 2

* AI-assisted Report Processing
* Duplicate Detection
* Confidence Model
* Image Processing
* Geolocation

## Phase 3

* Federation between HCP Nodes
* NGO Integration
* Government Integration
* Hospital Integration
* International Humanitarian Network

---

# Contributing

We welcome developers, designers, humanitarian organizations, researchers, and volunteers from around the world.

Together we can build an open infrastructure for humanitarian collaboration.

---

# License

Apache License 2.0

---

# About Human Connection Protocol

The Human Connection Protocol (HCP) is an open protocol designed to facilitate humanitarian coordination through interoperable, decentralized, and transparent data exchange.

This repository contains the first reference implementation of an HCP Node.

Together, HCP Nodes form the foundation of a global humanitarian network capable of connecting people, organizations, and resources during emergencies.

> Connecting Humanity Through Open Humanitarian Infrastructure.

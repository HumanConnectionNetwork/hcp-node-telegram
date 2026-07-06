# HCP Client Role

## HCP Telegram Client

Version: 0.1 Draft
Status: Draft
Project: Human Connection Network
Repository: hcp-client-telegram

---

## 1. Purpose

The HCP Telegram Client is a conversational interface that allows people to interact with the Humanitarian Connection Protocol through Telegram.

Its main purpose is to make HCP accessible to non-technical users in emergency, humanitarian, community or low-connectivity contexts.

The Telegram Client allows a user to:

* Create a Humanitarian Record.
* Search for possible matching records.
* Submit structured humanitarian observations.
* Communicate with an HCP-compatible Node.
* Use HCP without needing to understand the technical protocol.

---

## 2. The Telegram Client is not an HCP Node

The Telegram Client is not an HCP Node.

It does not permanently store humanitarian records.

It does not synchronize records with other nodes.

It does not validate consensus.

It does not participate directly in the distributed HCP network.

Instead, it acts as a user-facing client that communicates with an HCP Node through the HCP API.

---

## 3. Position in the HCP Ecosystem

```text
User
 │
 ▼
Telegram Bot
 │
 ▼
HCP Telegram Client
 │
 ▼
HCP Node API
 │
 ▼
HCP Node
 │
 ▼
Other HCP Nodes
```

The Telegram Client is the entry point for the user.

The HCP Node is responsible for storing, processing, exposing and synchronizing Humanitarian Records.

---

## 4. Responsibilities of the Telegram Client

The Telegram Client is responsible for:

### 4.1 User Interaction

The client guides the user through a simple conversation flow.

Examples:

* `/start`
* Create record
* Search record
* Help
* Cancel operation

The client must make the process simple, clear and accessible.

---

### 4.2 Data Collection

The client collects the minimum necessary information to build a Humanitarian Record.

Example fields:

* Reported name
* Estimated age
* Reported location
* Event type
* Current status
* Source type
* Short description

The client should avoid collecting unnecessary or highly sensitive information.

---

### 4.3 Record Construction

After collecting the information, the client transforms the user input into a valid HCP-compatible JSON object.

The client must follow the Humanitarian Record structure defined in the HCP Specification.

---

### 4.4 Communication with an HCP Node

The client sends requests to an HCP Node API.

Examples:

```text
POST /hcp/records
GET /hcp/records/search
GET /hcp/health
```

The client does not decide how records are stored or synchronized.

That responsibility belongs to the HCP Node.

---

### 4.5 User Feedback

The client must clearly inform the user about the result of each operation.

Examples:

* Record created successfully.
* Record could not be created.
* No possible matches found.
* Possible correlation candidates found.
* The HCP Node is unavailable.

---

## 5. Responsibilities the Telegram Client does not have

The Telegram Client must not:

* Act as the source of truth.
* Store humanitarian records permanently.
* Replace an HCP Node.
* Decide identity verification.
* Confirm that two records belong to the same person.
* Perform final humanitarian validation.
* Expose private data unnecessarily.
* Depend on a single centralized server by design.

---

## 6. Record Creation Flow

```text
User starts the bot
 │
 ▼
Selects "Create Humanitarian Record"
 │
 ▼
Bot asks structured questions
 │
 ▼
Bot validates basic input
 │
 ▼
Bot builds HCP JSON
 │
 ▼
Bot sends JSON to HCP Node
 │
 ▼
Node returns response
 │
 ▼
Bot shows result to user
```

The Telegram Client only prepares and submits the record.

The HCP Node processes the record.

---

## 7. Search Flow

```text
User selects "Search Record"
 │
 ▼
Bot asks for search criteria
 │
 ▼
Bot sends query to HCP Node
 │
 ▼
Node returns possible correlation candidates
 │
 ▼
Bot shows possible matches to the user
```

Search results must be presented as possible matches, never as absolute identity confirmation.

---

## 8. Correlation Candidates

When searching for a person, the client may receive a list of possible matches.

These are called Correlation Candidates.

A Correlation Candidate does not mean that a person has been identified with certainty.

It only means that the HCP Node found records that may be related based on available humanitarian observations.

Example:

```text
Possible match found

Reported name: María Pérez
Estimated age: 34
Reported location: Caracas
Status: Hospitalized
Confidence: Medium
```

The client must always communicate uncertainty clearly.

---

## 9. Offline-first Considerations

The first version of the Telegram Client depends on Telegram and internet connectivity.

However, the design should remain compatible with future offline-first clients such as:

* SMS client
* WhatsApp client
* Mesh network client
* Local radio gateway
* Low-connectivity mobile client

For this reason, the Telegram Client should keep a clean separation between:

* User interface
* HCP record construction
* HCP API communication

---

## 10. Security and Privacy Principles

The Telegram Client should follow these principles:

* Collect only the minimum necessary data.
* Avoid exposing sensitive information in public messages.
* Avoid storing records locally unless explicitly needed.
* Use environment variables for tokens and API URLs.
* Never commit secrets to the repository.
* Treat every humanitarian record as sensitive by default.
* Communicate uncertainty honestly.

---

## 11. Recommended Internal Architecture

```text
app/
├── bot.py
├── config.py
├── conversation/
│   ├── start.py
│   ├── create_record.py
│   ├── search_record.py
│   └── help.py
├── hcp/
│   ├── client.py
│   ├── records.py
│   ├── search.py
│   └── health.py
├── models/
│   ├── humanitarian_record.py
│   └── correlation_candidate.py
├── utils/
│   ├── validation.py
│   └── formatting.py
└── messages.py
```

---

## 12. Summary

The HCP Telegram Client is the conversational bridge between people and the Humanitarian Connection Protocol.

It allows users to create and search Humanitarian Records through Telegram, while the HCP Node remains responsible for storage, processing, synchronization and interoperability.

The client should be simple, safe, transparent and reusable as a model for future HCP clients.


# BOT-FLOW

Version: 0.1 (Draft)

Status: Draft

Category: Client Specification

Project: Human Connection Network

Repository: hcp-client-telegram

License: Apache-2.0

Depends On:

* HCP-0000 Overview
* HCP-0001 Humanitarian Record
* HCP-0004 Correlation Candidate
* HCP Client Role

---

# 1. Purpose

This document defines the complete conversational experience (UX) of the HCP Telegram Client.

Its objective is to provide an intuitive, accessible and universal interface that allows any person to create or search Humanitarian Records without requiring technical knowledge.

The Telegram Client should feel like a simple conversation rather than a technical application.

---

# 2. UX Principles

The Telegram Client should always follow these principles.

## Simple

Every message should use short and understandable language.

Avoid technical terminology.

---

## Universal

The client should be understandable regardless of the user's country or culture.

Questions should be clear even for people unfamiliar with technology.

---

## Accessible

Every action should contain:

* clear text
* emoji/icon support
* screen-reader friendly descriptions

Icons should complement the text, never replace it.

Example:

📍 Reported Location

instead of only

📍

---

## Progressive

The client asks only one question at a time.

Never overwhelm the user with large forms.

---

## Respectful

The client should never assume facts.

It only records what the user reports.

---

## Honest

The client must never claim certainty when certainty does not exist.

It should communicate probability clearly.

---

# 3. Main Menu

After executing:

/start

the client displays:

---

🤝 Human Connection Network

Welcome.

This service allows you to create or search humanitarian reports.

What would you like to do?

📝 Create Report

🔍 Search Report

🌐 Language

❓ Help

---

The menu should always remain simple.

---

# 4. Create Humanitarian Record

Selecting

📝 Create Report

starts a guided conversation.

Each question occupies a single screen.

---

## Step 1

👤 Reported Name

"What name was reported?"

Example:

Maria Perez

---

## Step 2

🎂 Estimated Age

"If you don't know the exact age, provide an estimate."

Example:

34

or

Around 30

---

## Step 3

📍 Reported Location

"In which city or place was the person reported?"

---

## Step 4

🚨 Event Type

Examples:

Missing

Hospitalized

Shelter

Evacuated

Injured

Safe

Other

---

## Step 5

📌 Current Status

Example:

Reported

Confirmed

Updated

Closed

---

## Step 6

🏥 Information Source

Examples:

Family

Volunteer

Hospital

Fire Department

Police

NGO

Government

Other

---

## Step 7

📝 Short Description

The client asks for a brief description.

Example:

Reported by relatives after the landslide.

---

## Step 8

Review

The client displays a summary.

The user may:

✅ Confirm

✏ Edit

❌ Cancel

---

## Step 9

If confirmed

The client creates the Humanitarian Record JSON.

The JSON is sent to the configured HCP Node.

---

## Step 10

The user receives:

✅ Report successfully submitted.

Reference ID:

xxxxxxxx

---

# 5. Search Humanitarian Reports

Selecting

🔍 Search Report

starts the search assistant.

The client explains:

---

"We do not search for people by identity.

We search for humanitarian reports that may describe the same reported event.

The results below represent possible similarities, not confirmed identities."

---

The user understands from the beginning how HCP works.

---

## Search Fields

👤 Reported Name

🎂 Estimated Age (optional)

📍 Reported Location (optional)

---

After confirmation

The client sends the query to the HCP Node.

---

# 6. Search Results

The HCP Node may return:

No matches

One possible match

Two possible matches

Three possible matches

The Telegram Client should present a maximum of three Correlation Candidates ordered by confidence.

Example:

────────────────────

Possible Match #1

Confidence:

🟢 High

Maria Perez

Estimated age:

34

Location:

Caracas

Status:

Hospitalized

View Details

────────────────────

Possible Match #2

Confidence:

🟡 Medium

Maria Perez

Estimated age:

35

Location:

Petare

Status:

Missing

View Details

────────────────────

Possible Match #3

Confidence:

🟠 Low

Maria Perez

Estimated age:

33

Location:

Baruta

Status:

Shelter

View Details

---

If no candidates exist

The client displays

"No similar humanitarian reports were found."

---

# 7. Explaining Correlation Candidates

Whenever results are shown, the client should explain:

"This system does not identify people by identity.

Instead, it searches for humanitarian reports that may describe the same person based on the similarity of the reported event.

The results shown are possible correlations and should not be interpreted as confirmed identification."

This explanation should always accompany the results.

---

# 8. Confidence Indicators

To simplify understanding, confidence should be represented visually.

🟢 High

Very similar information.

🟡 Medium

Several important fields match.

🟠 Low

Some fields match, but uncertainty remains.

The colors complement the explanation and must not be the only indicator.

---

# 9. Accessibility

The Telegram Client should be usable by the widest possible audience.

Recommendations:

• Use icons together with text.

• Avoid long paragraphs.

• Ask one question at a time.

• Avoid technical language.

• Keep buttons large and descriptive.

• Ensure every icon has accompanying text for screen readers.

• Never rely solely on colors to communicate meaning.

---

# 10. Conversation Flow

```text
/start

↓

Main Menu

↓

Create Report
            ↓
        Guided Questions
            ↓
      Review Information
            ↓
        Confirm Submission
            ↓
     POST /hcp/records
            ↓
     Success Message
```

```text
/start

↓

Main Menu

↓

Search Report
        ↓
   Search Criteria
        ↓
 GET /hcp/search
        ↓
Correlation Candidates
        ↓
   View Details
```

---

# 11. Future Compatibility

This conversational flow should remain consistent across future HCP clients, including:

* Telegram
* WhatsApp
* SMS
* Mobile applications
* Web interfaces
* Offline-first clients
* Mesh network gateways

Only the communication channel should change.

The user experience and the HCP concepts should remain consistent across all implementations.

---

# 12. Summary

The Telegram Client should provide a calm, accessible and trustworthy conversational experience.

It does not identify people.

It helps users create and search Humanitarian Records while clearly communicating uncertainty whenever search results are presented.

Its primary objective is to make HCP understandable and usable by anyone, regardless of technical knowledge, literacy level or cultural background.


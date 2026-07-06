# SEARCH-RECORD-FLOW

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
* BOT-FLOW
* CREATE-RECORD-FLOW

---

# 1. Purpose

This document defines the conversational flow used by the HCP Telegram Client to search Humanitarian Records.

Unlike traditional systems, HCP does not search for people by identity.

Instead, it searches for humanitarian observations that may describe the same reported case.

The objective is to help users find relevant humanitarian information while clearly communicating uncertainty.

---

# 2. Fundamental Principle

The HCP Telegram Client must never claim that it has identified a person.

Instead, it should communicate that it has found one or more reported cases whose characteristics are similar to the information provided.

The client always presents **possible correlations**, never confirmed identities.

---

# 3. Explaining the Search

Before asking for any information, the client should explain the purpose of the search.

Example:

---

🔍 Search Reported Cases

This service searches humanitarian reports that may describe the same reported event.

It does **not** identify people by identity.

Results are presented according to the similarity of the available information.

---

This explanation should always appear before the first question.

---

# 4. Search Flow

```text
Search Reported Cases

↓

Reported Name

↓

Estimated Age (optional)

↓

Reported Location (optional)

↓

Search

↓

GET /hcp/search

↓

Correlation Candidates

↓

View Details

↓

End
```

---

# 5. Search Criteria

The Telegram Client should request only the information necessary to perform the search.

---

## 👤 Reported Name

Question

"What name was reported?"

The name is recommended.

If unknown, the user may skip this field.

---

## 🎂 Estimated Age

Question

"What is the estimated age?"

Approximate values are acceptable.

This field is optional.

---

## 📍 Reported Location

Question

"Where was this person reported?"

Examples

City

Hospital

Shelter

Neighborhood

Region

This field is optional.

---

The search may proceed even when only one field is available.

---

# 6. Sending the Query

After confirmation

The Telegram Client sends the search request to the configured HCP Node.

The client does not perform correlation calculations.

Correlation is always performed by the HCP Node.

---

# 7. Search Results

The HCP Node may return:

• No results

• One Correlation Candidate

• Two Correlation Candidates

• Three Correlation Candidates

The Telegram Client should display a maximum of three candidates ordered by **Correlation Probability (%)**.

---

# 8. Correlation Candidate

Each candidate represents a humanitarian report that may correspond to the reported case.

The client should display information similar to the following.

────────────────────────

Possible Report #1

Probability

92%

Reported Name

Maria Perez

Estimated Age

34

Reported Location

Caracas

Current Status

Hospitalized

Source

Hospital

View Details

────────────────────────

Possible Report #2

Probability

78%

Reported Name

Maria Perez

Estimated Age

35

Reported Location

Petare

Current Status

Missing

Source

Volunteer

View Details

────────────────────────

Possible Report #3

Probability

64%

Reported Name

Maria Perez

Estimated Age

33

Reported Location

Baruta

Current Status

Shelter

Source

NGO

View Details

---

Candidates should always appear ordered from highest to lowest probability.

---

# 9. Explaining Probability

Whenever results are displayed, the Telegram Client should explain:

---

Probability (%) represents the estimated similarity between your search and each humanitarian report.

It is calculated from the reported information available at the time of the search.

A higher percentage indicates greater similarity, but it does **not** confirm that both reports refer to the same person.

---

This explanation should always accompany the results.

---

# 10. Viewing Details

Selecting a candidate displays additional information about that humanitarian report.

Example

Reported Name

Estimated Age

Reported Location

Event Type

Current Status

Information Source

Description

Report Date

Correlation Probability

Reference ID

The client should not expose unnecessary personal information.

---

# 11. No Results

If no candidates are found

The Telegram Client should display

---

No similar humanitarian reports were found.

This does not necessarily mean that no report exists.

New humanitarian reports may be submitted over time.

You may try again later.

---

The message should avoid suggesting failure.

---

# 12. Communication Principles

The Telegram Client should always communicate uncertainty honestly.

Recommended wording

✔ Possible Match

✔ Possible Correlation

✔ Similar Report

Avoid

✘ Identified Person

✘ Exact Match

✘ Confirmed Identity

---

# 13. Probability Presentation

Correlation Probability should always be presented as a percentage.

Example

Probability

96%

83%

71%

58%

The percentage should never be interpreted as certainty.

It represents only the estimated similarity calculated by the HCP Node.

---

# 14. Accessibility

The search flow should remain accessible.

Recommendations

• One question at a time.

• Short sentences.

• Icons together with descriptive text.

• Large buttons.

• Screen-reader friendly wording.

• Never rely only on color to communicate information.

---

# 15. Future Compatibility

This search flow should remain identical across future HCP clients.

Examples

* Telegram

* WhatsApp

* SMS

* Mobile Applications

* Web Clients

* Mesh Network Clients

Only the communication channel should change.

The search experience should remain consistent throughout the HCP ecosystem.

---

# 16. Summary

The Search Record flow enables users to search humanitarian reports using simple information such as a reported name, estimated age and reported location.

The Telegram Client does not identify people.

Instead, it presents up to three Correlation Candidates ranked by Correlation Probability (%), helping users understand which humanitarian reports are most similar while clearly communicating that every result represents a probability rather than a confirmed identity.

This approach preserves both the technical integrity of the Humanitarian Connection Protocol and the trust of the people who depend on it during humanitarian emergencies.


# CREATE-RECORD-FLOW

Version: 0.2 (Draft)

Status: Draft

Category: Client UX Specification

Project: Human Connection Network

Repository: hcp-client-telegram

License: Apache-2.0

Depends On:

- HCP Client Role
- BOT-FLOW
- CLIENT-ARCHITECTURE
- Humanitarian Record (HCP-0001)

---

# 1. Purpose

This document defines the complete user experience for creating a Humanitarian Record using the HCP Telegram Client.

The objective is to guide users through a simple, structured and accessible conversation while maximizing data quality and minimizing unnecessary free text.

The client should behave as a humanitarian assistant rather than a traditional form.

---

# 2. Design Principles

The Create Report flow follows these principles.

## Progressive

Only one question is presented at a time.

Users should never feel overwhelmed.

---

## Guided

Whenever possible, predefined options should be presented using buttons.

Free text should only be requested when necessary.

---

## Accessible

Questions should be short, clear and understandable for users with different educational backgrounds.

---

## Human-centered

The conversation should feel natural and respectful.

The client assists the user instead of interrogating them.

---

## Honest Data

The system encourages honest reporting.

Approximate information is acceptable when exact information is unavailable.

---

# 3. Flow Overview

```text
/start

↓

📝 Crear Reporte

↓

¿Qué deseas reportar?

↓

🚨 Persona desaparecida
🏥 Persona hospitalizada
🏠 Persona refugiada / en albergue
✅ Persona localizada / segura
🚑 Emergencia pública

↓

Formulario correspondiente

↓

Resumen

↓

Confirmar

↓

Enviar al Nodo HCP

↓

Respuesta del Nodo
```

---

# 4. Event Selection

The first decision determines the type of Humanitarian Observation.

The user selects one option.

- 🚨 Missing Person
- 🏥 Hospitalized Person
- 🏠 Sheltered Person
- ✅ Safe / Located Person
- 🚑 Public Emergency

Internally this becomes:

```text
missing
hospitalized
sheltered
safe
public_emergency
```

These values populate the `event_type` field of the Humanitarian Record.

---

# 5. Missing Person Flow

The following conversation is used.

---

## Step 1

🎂

**What is the estimated age of the person?**

Examples

34

Around 50

Child

Adult

Unknown

---

## Step 2

👤

**Do you know the person's name?**

If you know it, write the reported name.

If you don't know it, write:

Unknown

---

## Step 3

📍

**Where is the person located?**

Examples

City

Neighborhood

Hospital

Shelter

Reference point

---

## Step 4

📣

**Who is reporting this event?**

The user selects one option.

👨‍👩‍👧 Family

🏥 Hospital

🚒 Fire Department

🤝 Volunteer

👮 Police

👤 Friend / Acquaintance

❓ Unknown

No free text is allowed in this step.

---

## Step 5

📝

Describe the situation briefly.

Only useful humanitarian information should be included.

---

# 6. Other Event Types

Hospitalized Person

Sheltered Person

Safe Person

Public Emergency

follow the same conversational model whenever possible.

Future versions may introduce event-specific questions while preserving protocol compatibility.

---

# 7. Temporary Draft

During the conversation no Humanitarian Record is created.

Each answer is temporarily stored in the user session.

Example

```text
context.user_data
```

If the user cancels the conversation all temporary information is discarded.

---

# 8. Review Screen

After all required information has been collected, the client displays a review page.

---

📋 **Review your report before sending**

You have completed the available information for this report.

This record will become part of an open humanitarian service whose purpose is to help relate information during emergency situations.

Please submit only information that you believe to be true or reasonably reliable.

An honest report may help connect important information for other people.

Would you like to send this report?

---

The collected information is displayed in a user-friendly format.

Internal protocol identifiers must never be shown.

Example

Instead of

```text
event_type = missing
```

Display

```text
🚨 Missing Person
```

---

# 9. Available Actions

Three buttons are displayed.

✅ Confirm and Send

✏️ Edit Information

❌ Cancel

---

# 10. Edit Information

Selecting Edit allows the user to modify individual fields.

Examples

🎂 Estimated Age

👤 Reported Name

📍 Location

📣 Reporter

📝 Description

After editing, the client returns to the Review Screen.

---

# 11. Cancel

If the user cancels,

all temporary information is deleted.

The client displays

---

Report cancelled.

No information has been sent.

You may create a new report at any time from the main menu.

---

# 12. Confirmation

Only after the user selects

✅ Confirm and Send

does the client create a Humanitarian Record.

The object is validated.

Converted to HCP JSON.

Sent to the configured HCP Node.

---

# 13. Successful Response

If the Node accepts the record the client displays

---

✅ Report successfully submitted

Thank you for contributing.

Your report has been registered as a Humanitarian Observation.

HCP does not attempt to identify people.

HCP relates humanitarian observations submitted by families, hospitals, emergency organizations and volunteers in order to facilitate future searches and possible correlations.

As additional compatible observations are received, this report may contribute to new humanitarian correlations.

---

📄 HCP Record

Record ID

Date

Status

🟢 Successfully Registered

---

The user is also informed

You may share this Record ID with relatives, humanitarian organizations or search teams whenever you need to reference this report.

---

# 14. Failed Submission

If the HCP Node cannot be reached

the client informs the user that the report could not be delivered.

Future versions may allow automatic retry or offline synchronization.

---

# 15. Design Philosophy

Creating a Humanitarian Record is not the same as identifying a person.

The report represents a humanitarian observation recorded at a particular place and time using the information available to the reporter.

Multiple observations may refer to the same person without claiming certainty.

HCP preserves each observation independently and enables future correlation between compatible reports.

This approach maximizes interoperability while avoiding assumptions about identity.

---

# 16. Summary

The Create Report flow guides users through a structured humanitarian conversation that prioritizes accessibility, data quality and protocol consistency.

The user provides only the information available, reviews the complete report before submission and explicitly confirms its publication.

The resulting Humanitarian Record becomes a reusable humanitarian observation that may later be correlated with other compatible observations across the HCP ecosystem.

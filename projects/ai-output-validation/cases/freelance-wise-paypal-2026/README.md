# Case: freelance.de / Wise / PayPal — Structured Escalation 2026

## Classification
**Type:** Consumer dispute — unauthorized auto-renewal + double billing  
**Tools applied:** FactBoundKernel (core_mechanism.py), Validator.py  
**Outcome:** Full restitution achieved

---

## Case Summary

freelance.de GmbH automatically renewed a STARTER membership 
(Invoice P279144, €35,70) on 09.03.2026 without verifiable 
delivery of the contracted core service (direct client access, 
project mediation). The renewal triggered a payment chain failure:
PayPal's primary source (bank transfer) was rejected, 
causing a secondary charge to Wise card ••••9678 
(Transaction #3564035935, ARN 74004766076075230851386).

---

## Evidence Structure

| Date | Event | Result |
|------|-------|--------|
| 11.12.2025 | Invoice P271670 — initial 3-month subscription | €35,70 charged |
| 09.03.2026 | Invoice P279144 — auto-renewal | 2nd charge €35,70 |
| 11.03.2026 | Structured refund demand sent to freelance.de | Kulanz refund granted |
| 12.03.2026 | PayPal Dispute PP-R-AQU-619937308 | Closed — €35,70 returned |
| 16.03.2026 | Bank rejection → Wise card charged as fallback | Double billing confirmed |
| 18.03.2026 | Wise Dispute #3564035935 filed + signed declaration | Formally opened |
| 07.04.2026 | Wise Complaint acknowledged (Sophie, Complaints Admin) | Under investigation |

---

## Methodology Applied

### FactBoundKernel — Evidence Classification
All claims separated into:
- **OBSERVATION:** Platform data (0 real client messages, 
  0 contracts mediated, 110 profile views with no contact access)
- **INFERENCE:** Structural paywall design prevents 
  STARTER-tier contact — service delivery structurally impossible
- **HYPOTHESIS:** Auto-renewal constitutes unjust enrichment 
  under §812 BGB where core service was not rendered

Forbidden pattern blocked: intention attribution 
("freelance.de intentionally deceived") — replaced with 
structural analysis of platform architecture.

### Validator.py — Claim Verification
- Refund demand grounded in platform-verifiable data: VERIFIED
- Wise double-charge via ARN cross-reference: VERIFIED
- PayPal fallback charge mechanism confirmed by PayPal agent: VERIFIED
- freelance.de "Kulanz" framing (denying contractual obligation): SPIN

---

## Documents
- `documents/P271670_invoice.pdf` — Original subscription invoice
- `documents/P279144_invoice.pdf` — Auto-renewal invoice
- `documents/CH_Letter_Wise_dispute.pdf` — Signed Wise dispute declaration
- `documents/communication_transactions.pdf` — Full correspondence log
- `screenshots/` — PayPal dispute closed, double charge, 
  Wise acknowledgement, freelance.de refund confirmation

---

## Outcome
PayPal dispute resolved in full (€35,70).  
Wise complaint formally acknowledged, investigation ongoing.  
Escalation pathway prepared: Ombudsfin (FSMA) as next step 
if Wise does not resolve within statutory timeframe.

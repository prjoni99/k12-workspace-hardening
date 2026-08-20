# Playbooks

Numbered, 2am-executable. Each step has a **verify** line. Do not skip verify lines —
they are how you know the step worked when you are tired and being watched.

| # | Playbook | Trigger | First action |
| --- | --- | --- | --- |
| [01](01-compromised-staff-account.md) | Compromised staff account | Alert, user report, or anomalous activity | **Suspend the account** |
| [02](02-compromised-student-account.md) | Compromised student account | Same, student OU | Reset password |
| [03](03-post-delivery-phish-purge.md) | Post-delivery phish purge | Phish confirmed delivered to multiple users | Scope the campaign |
| [04](04-payroll-diversion-attempt.md) | Payroll diversion attempt | Banking-change request, tripwire hit, or payroll report | **Freeze the change** |
| [05](05-vendor-invoice-fraud.md) | Vendor invoice fraud | Remittance change on an invoice | **Stop the payment** |
| [06](06-mass-calendar-spam-cleanup.md) | Mass calendar spam | Multiple users report unwanted events | Change the invitation setting |
| [07](07-lookalike-domain-response.md) | Lookalike domain | Domain-spoofing quarantine hit or report | Confirm and document |

## Before any incident

Fill these in now. Hunting for them mid-incident is how thirty-minute incidents become
three-hour ones.

| Role | Name | Mobile | Backup |
| --- | --- | --- | --- |
| Security admin (primary) | | | |
| Technology director | | | |
| Superintendent / designee | | | |
| CFO / finance director | | | |
| Communications | | | |
| District legal counsel | | | |
| Cyber insurance carrier — claims | | | |
| Google Workspace support (PIN/case) | | | |
| Law enforcement — local | | | |
| FBI field office / IC3 | tips.fbi.gov | 1-800-CALL-FBI | ic3.gov |
| MS-ISAC SOC | | | |

## Universal rules

1. **Contain before you investigate.** A running compromise gets worse while you read logs.
2. **Preserve before you remediate.** Vault hold first — remediation destroys evidence.
3. **Write down what you do, with timestamps.** You will be asked. Insurance and counsel
   both need it, and memory is not evidence.
4. **Never punish a reporter**, including the person who clicked.
5. **Assume more than one account.** Pivot on login IP.
6. **Escalate money early.** Any funds movement → CFO and superintendent immediately.
   Under 72 hours, a wire can sometimes be recalled. After that, rarely.
7. **No PII in tickets, chat, or notes.** Reference accounts by OU and role, not by name,
   wherever the record will persist.

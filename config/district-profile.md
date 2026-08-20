# District Profile — fill this in first

Every doc in this repo references the tokens below instead of hard-coded values.
Fill this in, run the substitution snippet at the bottom, commit the result.

## Identity

| Token | Value | Notes |
| --- | --- | --- |
| `<DISTRICT_NAME>` | | e.g. "Example County Schools" |
| `<PRIMARY_DOMAIN>` | | the domain in staff email addresses |
| `<STUDENT_DOMAIN>` | | same as primary in most districts; separate in some |
| `<SECONDARY_DOMAINS>` | | alias/legacy domains — **each needs its own DMARC record** |
| `<SECURITY_ALIAS>` | | monitored group for alerts, e.g. `security@` — see note |
| `<ABUSE_ALIAS>` | | where users forward suspected phish, e.g. `phishing@` |

> **`<SECURITY_ALIAS>` must be a Google Group, not an individual.** Alert center
> routing to a personal address dies when that person leaves or takes leave. Lock the
> group per `docs/04-groups.md` (internal posting only) or alert routing becomes an
> injection path.

## Scale

| Token | Value |
| --- | --- |
| `<STAFF_COUNT>` | |
| `<STUDENT_COUNT>` | |
| `<SCHOOL_COUNT>` | |

## OU map

Record the real tree. The settings tables use four role archetypes — map each to a real
OU path here:

| Archetype (table column) | Real OU path(s) |
| --- | --- |
| Staff | |
| Students | |
| Finance-HR | |
| Admins | |
| Shared Devices | |
| Service Accounts | |

## Mail flow

- MX points at: ☐ Google direct  ☐ third-party gateway → name: ______________
- Inbound gateway configured in Gmail (required if a gateway fronts Google): ☐ Y ☐ N
- SMTP relay service in use for copiers/scripts: ☐ Y ☐ N

## Bulk senders sending AS `<PRIMARY_DOMAIN>`

**This table gates DMARC enforcement.** Do not move past `p=none` until every row is
filled and every row is DKIM-aligned. Start from the assumed list in `ASSUMPTIONS.md` §A5.

| System | Vendor | Sends as | SPF mechanism | DKIM selector | Aligned? | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| SIS | | | | | ☐ | |
| Mass notification | | | | | ☐ | |
| LMS | | | | | ☐ | |
| Food service | | | | | ☐ | |
| Transportation | | | | | ☐ | |
| Copiers / scan-to-email | | | | | ☐ | |
| Helpdesk / ticketing | | | | | ☐ | |
| Survey tools | | | | | ☐ | |
| SMTP relay users | | | | | ☐ | |

## Tooling

- GAM7 / GAMADV-XTD3 with super admin: ☐ Y ☐ N
- Docker host for parsedmarc: ☐ Y ☐ N
- Existing SIEM / log destination: ______________

## Cabinet & high-risk name list

Names used by the display-name warning rule in `docs/01-gmail.md` §7 and the employee-name
spoofing control. **Roles, not a roster** — keep the actual names in the Admin console
rule only, never committed here (FERPA discipline; see `CLAUDE.md`).

| Role | In cabinet name rule? | In Finance-HR OU? |
| --- | --- | --- |
| Superintendent | ☐ | ☐ |
| Deputy/Assistant Superintendent(s) | ☐ | ☐ |
| CFO / Finance Director | ☐ | ☐ |
| HR Director | ☐ | ☐ |
| Payroll Supervisor | ☐ | ☐ |
| Accounts Payable | ☐ | ☐ |
| Technology Director | ☐ | ☐ |
| Principals (each school) | ☐ | ☐ |
| Board Chair | ☐ | ☐ |

## Substitution

Once filled in, replace tokens across the repo:

```bash
grep -rl '<PRIMARY_DOMAIN>' --include='*.md' --include='*.sh' . \
  | xargs sed -i '' \
    -e 's/<DISTRICT_NAME>/Example County Schools/g' \
    -e 's/<PRIMARY_DOMAIN>/example.k12.st.us/g' \
    -e 's/<SECURITY_ALIAS>/security@example.k12.st.us/g'
```

Review the diff before committing — the token list above is not exhaustive for every doc.

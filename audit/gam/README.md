# GAM Audit Scripts

Read-only audit scripts for a Google Workspace for Education tenant. Every script writes
CSV to `audit/gam/out/`, which is **`.gitignore`d**.

> ## ⚠ Output contains PII
>
> These scripts export staff and student email addresses, forwarding destinations, and
> delegate relationships. **`audit/gam/out/` is gitignored — keep it that way.** Do not
> commit output, do not paste it into a ticket, do not email it. Store on district-managed
> storage with access controls, and delete when the audit is closed.
> See [CLAUDE.md](../../CLAUDE.md).

---

## If GAM is not installed

**These scripts are still useful as documentation.** Every script header names the **Admin
console equivalent** for the same check. Work the console paths manually — slower, same
findings.

To install: [GAM7](https://github.com/GAM-team/GAM) or
[GAMADV-XTD3](https://github.com/taers232c/GAMADV-XTD3). Requires a super admin to authorize
a project. **The GAM service account itself becomes a high-value credential** — see §Safety.

---

## Requirements

- GAM7 or GAMADV-XTD3, authorized with super admin
- `bash`, `jq` (optional, for a couple of summaries)
- Run from the repo root or from `audit/gam/`

Verify before first run:

```bash
gam version
gam info domain
```

---

## Scripts — all read-only

| Script | Finds | Admin console equivalent |
| --- | --- | --- |
| [01-users-without-2sv.sh](01-users-without-2sv.sh) | Accounts not enrolled/enforced in 2SV | Directory > Users, add 2SV column |
| [02-forwarding-and-filters.sh](02-forwarding-and-filters.sh) | External forwarding, forwarding addresses, suspicious filters | Not fully available in console — this is the gap GAM fills |
| [03-delegates.sh](03-delegates.sh) | Mailbox delegates and send-as aliases | Not available in console at scale |
| [04-oauth-tokens.sh](04-oauth-tokens.sh) | OAuth grants per user and per app | Security > API controls > App access control |
| [05-app-passwords.sh](05-app-passwords.sh) | App-specific passwords | Per user only, in console |
| [06-group-settings.sh](06-group-settings.sh) | Group posting/join/external-member settings | Directory > Groups, one at a time |
| [07-admin-roles.sh](07-admin-roles.sh) | Admin role assignments | Account > Admin roles |
| [08-ou-service-state.sh](08-ou-service-state.sh) | Service on/off state per OU | Apps > (each service), one at a time |
| [run-all.sh](run-all.sh) | Runs all of the above | — |

**Scripts 02, 03, and 06 are the ones that justify GAM.** Those checks are impractical at
district scale through the console, and they are where compromises hide.

---

## Cadence

| Script | Frequency | Why |
| --- | --- | --- |
| 01 — 2SV | Monthly | Enforcement drift, new hires |
| **02 — forwarding/filters** | **Monthly** (weekly on Fundamentals) | **#1 attacker persistence mechanism** |
| 03 — delegates | Monthly | Quiet persistent access |
| 04 — OAuth tokens | Quarterly | [docs/07](../../docs/07-oauth-app-control.md) §7 |
| 05 — app passwords | Quarterly | Bypass 2SV by design |
| 06 — group settings | Quarterly | [docs/04](../../docs/04-groups.md) §7 |
| 07 — admin roles | Quarterly | Privilege creep |
| 08 — OU service state | Quarterly | New services arrive enabled |

**Diff against the previous run.** The diff is more valuable than the report — it shows what
someone changed since last time.

```bash
diff <(sort out/2026-07-01-forwarding.csv) <(sort out/2026-08-01-forwarding.csv)
```

---

## Interpreting output

### 01 — 2SV
Expected non-compliant: `/Service Accounts`, `/Shared Devices`, students (not enforced by
design — [docs/06](../../docs/06-accounts-mfa-admins.md) §10). **Any staff account in the
list is a finding.**

### 02 — Forwarding and filters
**Every external forwarding destination is a finding until proven otherwise.** Common
legitimate cases: a staff member forwarding to a district-owned alias, an approved
integration. Everything else needs a conversation.

**Filters matter as much as forwarding rules.** Look specifically for filters that forward
externally, or that delete/archive messages matching `payroll`, `invoice`, `direct deposit`,
`password`, or `security` — that pattern is attacker suppression, not user preference.

### 03 — Delegates
Legitimate: an admin assistant delegated to an administrator's mailbox. Findings:
delegates outside the expected relationship, delegates on Finance-HR mailboxes, delegates
granted to accounts that are now suspended or departed.

### 04 — OAuth tokens
Sort by app, count users. High user counts on unrecognized apps are the priority. Check
scopes against necessity — [docs/07](../../docs/07-oauth-app-control.md) §5.

### 05 — App passwords
**App-specific passwords bypass 2SV by design.** Each one is a standing credential. If
POP/IMAP is off per [docs/01](../../docs/01-gmail.md) §5, most of these should not exist —
their presence usually means a legacy client nobody migrated. Known exceptions (e.g. the
parsedmarc IMAP account, [docs/09](../../docs/09-dmarc-spf-dkim.md) §7) should be
**documented** so a future sweep doesn't revoke them blindly.

### 06 — Group settings
Findings: `whoCanPostMessage` allowing anyone or the public, `allowExternalMembers = true`,
external posting enabled. Prioritize by member count — see the tier model in
[docs/04](../../docs/04-groups.md) §3.

### 07 — Admin roles
**Expect to find more super admins than the district needs.** Vendor accounts from completed
projects are the most common orphan. Target: 2–4 —
[docs/06](../../docs/06-accounts-mfa-admins.md) §5.

### 08 — OU service state
Every `On` service is attack surface. Feed into
[docs/05](../../docs/05-other-services.md) §7.

---

## Safety

- **Everything in this directory is read-only.** Write operations live in
  [remediation/](remediation/), separately, with warnings.
- Scripts use `set -euo pipefail` and will stop on error rather than continue silently.
- The GAM service account is a **super-admin-equivalent credential**. Protect
  `~/.gam/` accordingly: restricted filesystem permissions, on a managed workstation, never
  in a shared or synced folder. **A compromised GAM credential is a compromised domain.**
- Run from a managed workstation, not a personal machine.

---

## Verify before trusting output

Scripts were written against GAM7 / GAMADV-XTD3 syntax as documented on 2026-08-20
([GAMADV-XTD3 wiki](https://github.com/taers232c/GAMADV-XTD3/wiki)). **GAM syntax varies
between GAM7 and GAMADV-XTD3 and changes across versions.**

**Run each script once and inspect the output before relying on it in an audit.** An empty
CSV may mean "no findings" or may mean the command silently returned nothing — those look
identical in a report and lead to opposite conclusions. Each script prints a row count so
you can tell.

# Playbook 01 — Compromised Staff Account

**Trigger:** suspicious-login alert, leaked-password alert, user report, mail the user
didn't send, or unexplained forwarding/filter/delegate changes.

**Target: contained in 15 minutes.**

> **The core fact for this playbook:** a password reset **does not** invalidate an OAuth
> refresh token, an app-specific password, a forwarding rule, or a delegate grant. If you
> stop at step 3, the attacker still has the mailbox. Steps 5–9 are the incident.

---

## Phase 1 — Contain (0–15 min)

### 1. Suspend the account
`Admin console > Directory > Users` → user → **Suspend user**

Faster and more complete than a password reset: it kills active sessions and blocks
re-authentication in one action.

**Verify:** user shows `Suspended`. Attempt to load their Gmail in an incognito window with
a known-good session — access denied.

### 2. Place a Vault hold — before remediating
`vault.google.com` → Matters → new matter → hold on this account, Gmail + Drive.

**Do this before steps 5–9.** Those steps delete the evidence you will need.

**Verify:** hold shows active, account listed.

### 3. Reset the password
`Admin console > Directory > Users` → user → **Reset password**. Require change at next
sign-in. Deliver out of band — **phone call or in person, never email or text.**

**Verify:** reset confirmed in console.

### 4. Sign out all sessions
User page → **Security** → **Sign out user** (sign out of all sessions)

**Verify:** login audit shows session termination.

---

## Phase 2 — Remove persistence (15–45 min)

**This phase is the one that determines whether you're back here next week.**

### 5. Revoke all OAuth tokens
`Admin console > Directory > Users` → user → **Security** → **Connected applications** →
remove all.

```bash
gam user <account> show tokens
gam user <account> delete tokens
```

**Verify:** re-run `show tokens` — empty.

### 6. Delete app-specific passwords
User → **Security** → **App passwords** → revoke all.

```bash
gam user <account> show asps
gam user <account> delete asps all
```

**Verify:** `show asps` returns none.

### 7. Check and remove forwarding
```bash
gam user <account> show forward
gam user <account> show forwardingaddresses
gam user <account> print filters
```

Remove any forwarding to an external address. **Also check filters** — attackers use a
filter that forwards *and* archives, so the user never sees the mail. A filter is easier to
miss than a forwarding rule and does the same job.

**Verify:** no forwarding, no filters with external forward or delete actions.

### 8. Check delegates and send-as
```bash
gam user <account> show delegates
gam user <account> show sendas
```

Remove unrecognized delegates. Remove unverified or unfamiliar send-as aliases.

**Verify:** delegate and send-as lists match expectation.

### 9. Check recovery options
User → **Security** → recovery email/phone. Attackers change these to retain a path back in.

**Verify:** recovery details are district-controlled and expected.

### 10. Check for admin role changes
```bash
gam print admins
```
**Verify:** the account holds no admin role it shouldn't. If it does — treat as a
domain-level incident, escalate to the technology director immediately, and check every
other admin account.

---

## Phase 3 — Assess blast radius (45–120 min)

### 11. What did it send?
`Security > Security center > Investigation tool` → **Gmail log events** → Sender =
account, date range = suspected compromise window (**default to 30 days**, not "since the
alert").

**Verify:** every outbound message in the window reviewed. Note recipients — internal and
external.

### 12. Purge anything malicious it sent
→ [Playbook 03](03-post-delivery-phish-purge.md)

### 13. What did it access?
Investigation tool → **Drive log events** → Actor = account. Look for mass downloads, mass
external sharing, access to student-records or finance folders.

**Verify:** file access reviewed; anything exfiltrated documented for step 20.

### 14. Where did they sign in from?
Investigation tool → **Login audit** → Actor = account. Record every IP and location.

**Verify:** unauthorized IPs identified and written down.

### 15. Pivot on the IP — find the rest
Investigation tool → **Login audit** → filter by the attacker IP across **all users**.

**This step finds the accounts you don't know about yet.** One compromised account is
almost never one compromised account.

**Verify:** all accounts touching that IP identified. **Run this playbook for each.**

### 16. Did they reach finance or student data?
If the account had SIS access, finance system access, or student-records access:
**escalate to the technology director and CFO now**, and check for a payroll change
([Playbook 04](04-payroll-diversion-attempt.md)).

---

## Phase 4 — Restore (2–24 h)

### 17. Restore access
Unsuspend. Require 2SV enrollment if not already —
[docs/06](../docs/06-accounts-mfa-admins.md) §3.

**If the user is Finance-HR or admin, enroll a passkey or security key before restoring
access.** This is the moment they will accept the friction.

**Verify:** user signs in successfully with 2SV.

### 18. Verify the settings stayed clean
Re-run steps 5–9. Attackers sometimes re-establish persistence between containment and
restoration.

**Verify:** all clean.

### 19. Brief the user
Explain what happened, what was done, what to watch for. **Do not blame.** The next report
depends on how this conversation goes.

---

## Phase 5 — Close out (24–72 h)

### 20. Notification assessment
If student or staff PII was accessed or exfiltrated: **engage district legal counsel and the
records officer.** FERPA and state breach-notification obligations may apply. **This
determination is not IT's to make alone.**

### 21. Report externally
- Cyber insurance carrier — often required within a contractual window
- IC3 (`ic3.gov`) if there was financial loss or attempted loss
- MS-ISAC, if a member
- State education agency, per state requirement

### 22. Root cause
How did they get in? Phish (which one? is it still in other inboxes?), reused password,
AiTM, OAuth grant? **Feed the answer back into the controls** —
[docs/00-threat-landscape.md](../docs/00-threat-landscape.md).

### 23. Timeline document
Timestamped, factual, no speculation. Store it with the Vault matter. Insurance and counsel
will both ask for it.

---

## GAM one-liner: full persistence check

```bash
for f in tokens asps forward forwardingaddresses delegates sendas filters; do
  echo "=== $f ==="
  gam user <account> show "$f" 2>/dev/null || gam user <account> print "$f" 2>/dev/null
done
```

Run at step 5 and again at step 18. **The second run is the one that catches re-establishment.**

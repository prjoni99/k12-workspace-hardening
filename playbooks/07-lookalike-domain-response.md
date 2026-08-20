# Playbook 07 — Lookalike Domain Response

**Trigger:** a domain-spoofing quarantine hit ([docs/01](../docs/01-gmail.md) §3), a user
report, or a routine domain-monitoring alert.

Examples of what you're looking for: `<district>-schools.org` vs `<district>schools.org`,
`.net` for `.org`, `rn` for `m`, `l` for `I`, added or removed hyphens, a plural, or an
added word like `-hr` or `-payroll`.

---

## 1. Confirm and document (0–30 min)

### 1.1 Verify it's hostile
Not every similar domain is an attack. Check for: a legitimate business with a similar name,
a district vendor, a parked domain with no mail, or a domain the district itself registered
years ago and forgot.

**Verify:** classification recorded with reasoning.

### 1.2 Capture evidence — before it disappears

```bash
whois <lookalike-domain>
dig <lookalike-domain> ANY +noall +answer
dig MX <lookalike-domain> +short
dig TXT <lookalike-domain> +short
```

Record: registrar, registration date, name servers, MX records, SPF/DKIM/DMARC presence,
hosting IP, and any registrant details not behind privacy.

**Screenshot any website**, with timestamp. **Do not visit from a district machine** — use
an isolated system or a URL analysis service.

**Verify:** artifacts saved to the incident record.

> **Registration date is the highest-signal field.** A domain registered in the last 72
> hours with MX records configured is an active campaign in its setup phase, and you may be
> ahead of the first message.

---

## 2. Contain (30–60 min)

### 2.1 Block inbound
Content compliance rule ([docs/01](../docs/01-gmail.md) §7): reject or quarantine all
inbound from the domain **and its subdomains**.

**Verify:** rule active and scoped to all OUs.

### 2.2 Block Drive sharing to it
Trust rule ([docs/03](../docs/03-drive.md) §5, rule 6): **Block** sharing to the domain.
**[Standard]/[Plus]**

**Verify:** rule active.

### 2.3 Block at the network layer
DNS filtering / web filter / firewall — block the domain district-wide. This covers the
QR-code and SMS vectors that never touch email.

**Verify:** blocked from a test client on the district network.

### 2.4 Check whether it already sent
Investigation tool → **Gmail log events** → sender domain = lookalike, widest available
date range.

If mail was delivered → [Playbook 03](03-post-delivery-phish-purge.md).

**Verify:** delivery history checked; purge completed if needed.

---

## 3. Take it down (1–5 business days)

### 3.1 Registrar abuse report
Find the registrar from `whois`; submit to their abuse contact. Include:

- The lookalike domain and the district's real domain
- Evidence of impersonation (screenshots, message samples, headers)
- A statement that it is being used to impersonate a public school district
- Any evidence of active phishing

**Verify:** ticket/case number recorded.

### 3.2 Hosting provider abuse report
If a website is hosted, report separately — hosting and registration are usually different
companies, and hosting takedowns are often faster.

**Verify:** case number recorded.

### 3.3 Google Safe Browsing
Report at `safebrowsing.google.com/safebrowsing/report_phish/`. Gets it flagged in Chrome
and Gmail broadly, often within hours — frequently the fastest real-world mitigation.

**Verify:** submitted.

### 3.4 Law enforcement
- **IC3** at `ic3.gov` — always, even with no loss. It builds the pattern record.
- Local law enforcement if there's a loss or a credible threat.
- **MS-ISAC**, if a member — they can escalate and may already be tracking the actor.

**Verify:** IC3 complaint number recorded.

### 3.5 If it's impersonating for financial fraud
Notify the district's bank so they can flag payments to accounts connected to this campaign.

---

## 4. Notify

### 4.1 Staff
> We've identified a fraudulent domain, `<lookalike>`, being used to impersonate the
> district. Legitimate district email always comes from `@<PRIMARY_DOMAIN>`.
> **Check the sender address carefully**, especially on anything about payments, payroll, or
> passwords. Forward anything suspicious to `<ABUSE_ALIAS>`.

### 4.2 Parents/guardians — if they're being targeted
Coordinate with communications. Post on the district site and push through the
mass-notification system. **Parents are often the target** — fake fundraiser, fake lunch
balance, fake registration.

### 4.3 Vendors and partner districts
If the domain is being used against them in the district's name, tell them directly. They
will do the same for you.

### 4.4 Cyber insurance
Notify per policy.

---

## 5. Monitor

- [ ] Watch for **additional lookalikes** — actors register in batches, and the second one
      is usually already registered
- [ ] Re-check registration/MX weekly until taken down
- [ ] Watch for the campaign shifting to a new domain after takedown — **the takedown
      usually moves the actor rather than stopping them**
- [ ] Keep the content compliance and trust rules in place after takedown; domains get
      re-registered

---

## 6. Prevent

### 6.1 Defensive registration
Register the obvious variants of the district domain: common TLDs (`.net`, `.com`, `.us`),
common typos, hyphenated forms. **~$15/year each.** For 10 variants that's $150/year against
an incident class that costs six figures. Take that ratio to the CFO once; it is an easy yes.

Point them at the district website, and give each `v=spf1 -all`, a null MX, and
`p=reject` — see [docs/09](../docs/09-dmarc-spf-dkim.md) §5.

### 6.2 Domain monitoring
Set up alerting for newly-registered domains similar to `<PRIMARY_DOMAIN>`. Free and
commercial options exist; DMARC `rua` reports also surface some of this
([docs/09](../docs/09-dmarc-spf-dkim.md) §7).

### 6.3 Controls that must already be on
- **Protect against domain spoofing based on similar domain names** → `Quarantine`
  ([docs/01](../docs/01-gmail.md) §3)
- **DMARC at `p=reject`** ([docs/09](../docs/09-dmarc-spf-dkim.md)) — stops the *exact*
  domain being spoofed, though **not** a lookalike, which is a different domain entirely and
  can publish its own perfectly valid SPF and DKIM

> That distinction is worth stating to leadership: DMARC does not stop lookalike domains.
> People assume it does. The control for lookalikes is the §3 similar-domain setting plus
> defensive registration.

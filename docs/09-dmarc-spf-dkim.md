# 09 — SPF, DKIM & DMARC

Research date **2026-08-20**.

> ## ⚠ Read this before touching DNS
>
> **Enforcing DMARC before every third-party sender is aligned will break parent
> communication district-wide.** Not degrade — break. Mass-notification messages, SIS
> alerts, lunch-balance notices, and attendance calls will be rejected by receiving
> servers, silently, at scale, and the district will find out from parents.
>
> The inventory in [config/district-profile.md](../config/district-profile.md) is not
> paperwork. It is the gate. **Do not pass §5 until it is complete.**

---

## 1. What each record does

| | Answers | Fails when |
| --- | --- | --- |
| **SPF** | Which servers may send for this domain? | Sender IP isn't listed |
| **DKIM** | Was this message signed by the domain and unmodified? | Signature missing or invalid |
| **DMARC** | What should a receiver do when SPF *and* DKIM both fail to align? | Neither aligns |

**Alignment is the concept people miss.** DMARC doesn't just need SPF or DKIM to *pass* —
it needs the passing domain to *match the From: header domain*. A vendor whose SPF passes
for `vendor-mailer.com` while sending as `<PRIMARY_DOMAIN>` **fails DMARC alignment**, even
though SPF technically passed. This is precisely how bulk senders break at enforcement, and
why the inventory matters more than the DNS syntax.

**DKIM is what makes forwarded mail survive.** SPF breaks on forwarding (the forwarding
server isn't in the SPF record); DKIM survives it. In a district — where staff forward to
each other constantly and parents forward to co-parents — **DKIM alignment is the one that
actually carries the load.**

---

## 2. Step 1 — Inventory (the gate)

**Complete [config/district-profile.md](../config/district-profile.md) → "Bulk senders"
before proceeding.** [ASSUMPTIONS.md](../ASSUMPTIONS.md) §A5 has the starting list.

### Finding senders you don't know about

You will not remember them all. Find them:

1. **DMARC `rua` reports at `p=none` (§5, Stage 1).** The authoritative method — every
   source sending as your domain shows up, including the ones nobody documented. **This is
   why Stage 1 runs for two full weeks minimum.**
2. **Email log search / BigQuery** ([docs/08](08-monitoring-response.md) §6) for outbound
   from non-Google IPs.
3. **Ask finance for the vendor list.** Anything that emails parents or staff is a sender.
   The AP ledger is a surprisingly good asset inventory.
4. **Walk the buildings.** Copiers, alarm panels, HVAC controllers, bell systems, marquee
   signs, gym scoreboards. Anything with an SMTP config is a sender, and none of it is in
   any inventory.
5. **Check the SMTP relay** service settings for who is authorized to use it.

### Per sender, record

| Field | Why |
| --- | --- |
| Envelope-From and Header-From domains | Alignment depends on Header-From |
| SPF mechanism needed | `include:`, `ip4:`, `a:` |
| **DKIM available?** | If no, the vendor is a DMARC blocker — escalate now, not in month three |
| Selector and key length | 2048 preferred |
| Business owner | Who calls the vendor |
| Criticality | Determines whether you delay enforcement or accept breakage |

**Vendors who cannot do DKIM are the critical path.** Identify them in week one. The
options are: get them to implement it, move them to a subdomain (§6), or replace them.
All three take months. Starting that conversation late is what makes DMARC projects stall
for a year.

---

## 3. Step 2 — SPF

**Path (Google's record):** `Admin console > Apps > Google Workspace > Gmail > Authenticate email`
([source](https://knowledge.workspace.google.com/admin/security/set-up-dkim))

### The 10-lookup limit

SPF permits a maximum of **10 DNS lookups** during evaluation
([RFC 7208 §4.6.4](https://datatracker.ietf.org/doc/html/rfc7208#section-4.6.4)). Exceeding
it produces `permerror`, which most receivers treat as **fail**. Every `include:`, `a`,
`mx`, `ptr`, and `exists` counts — and a vendor's `include:` can contain its own nested
includes that count against your budget.

**Districts blow this limit routinely**, because every vendor asks for one more `include:`
and nobody counts. Then SPF silently fails for everything, and because DKIM usually still
works, nobody notices until DMARC enforcement.

### Target record

```dns
<PRIMARY_DOMAIN>.  IN  TXT  "v=spf1 include:_spf.google.com include:_spf.<sis-vendor> include:<notification-vendor> ip4:<relay-ip> -all"
```

Rules:

- **Count your lookups before publishing.** Use an SPF flattening/validation checker.
- `-all` (hard fail), not `~all` (soft fail), **once you're confident the record is
  complete**. Start at `~all` during rollout.
- **One SPF record per domain.** Two TXT records both starting `v=spf1` is a `permerror` —
  a common and completely silent failure.
- Prefer `ip4:` for a fixed relay over an `include:` — costs zero lookups.
- **Every secondary domain needs its own record**, including parked ones. An unused domain
  with no SPF is a free spoofing asset.

### Consolidation when over 10

1. Remove vendors no longer in use — always the first win, usually 2–3 lookups.
2. Replace `include:` with `ip4:` where the vendor publishes stable IPs.
3. Move a vendor to a **subdomain** (§6) — that vendor's SPF then lives on the subdomain's
   record and costs nothing on the primary.
4. Use an SPF-flattening service **only as a last resort** — it introduces a dependency
   that silently breaks when a vendor changes IPs and you don't re-flatten.

**Rollback:** revert the DNS TXT record. Propagation per your TTL — **lower TTL to 300s
before any change**, raise it after you're confident.

---

## 4. Step 3 — DKIM

**Path:** `Admin console > Apps > Google Workspace > Gmail > Authenticate email` →
generate key → publish TXT → **Start authentication**
([source](https://knowledge.workspace.google.com/admin/security/set-up-dkim))

### Google's DKIM

| Item | Value |
| --- | --- |
| Key length | **2048-bit.** Google recommends 2048 where the DNS provider supports it; 1024 is the minimum for sending to personal Gmail ([source](https://knowledge.workspace.google.com/admin/security/set-up-dkim)) |
| Selector | Default `google`, or a custom one |
| **Every domain** | Generate and publish for **each** domain and alias domain separately |
| Verify | Confirm "Authenticating email" in the console after publishing |

**2048-bit keys exceed the 255-character limit of a single DNS string.** Most providers
split them automatically; some don't, and the record silently fails. If DKIM doesn't
validate after publishing a 2048-bit key, this is the cause about 80% of the time.

### Third-party sender DKIM — the actual work

**Every bulk sender in the §2 inventory needs its own DKIM**, typically a CNAME the vendor
provides pointing at their signing infrastructure.

| Sender | Typical method | Notes |
| --- | --- | --- |
| SIS | CNAME selectors | Usually supported |
| Mass notification | CNAME selectors | Usually supported; **verify alignment**, some sign as their own domain |
| Food service | Varies | **Frequent blocker** |
| Copiers via relay | Signed by the relay | Verify the relay signs as `<PRIMARY_DOMAIN>` |
| SMTP relay users | Signed by relay | Same |
| Small/legacy vendors | Often none | **The critical path** |

**Verify alignment, not just presence.** A vendor signing with `d=vendor.com` while sending
`From: notices@<PRIMARY_DOMAIN>` gives you a valid DKIM signature that **does not align** and
therefore does not satisfy DMARC. Check `d=` against the From: domain for every sender. This
is the single most common false "we're ready" in a DMARC project.

**Google requires DKIM and SPF to be authenticating for at least 48 hours before DMARC is
configured** ([source](https://knowledge.workspace.google.com/admin/security/set-up-dmarc)).

---

## 5. Step 4 — DMARC ramp (60–90 days)

**Path:** DNS TXT at `_dmarc.<PRIMARY_DOMAIN>`
([source](https://knowledge.workspace.google.com/admin/security/recommended-dmarc-rollout))

Google's guidance: start at `p=none`, monitor, then move to quarantine for a small
percentage, then increase, then reject
([source](https://knowledge.workspace.google.com/admin/security/set-up-dmarc)).

### The ramp

| Stage | Duration | Record | Exit criteria |
| --- | --- | --- | --- |
| **1. Monitor** | **14+ days** (don't shorten) | `v=DMARC1; p=none; rua=mailto:dmarc@<PRIMARY_DOMAIN>; ruf=mailto:dmarc@<PRIMARY_DOMAIN>; fo=1; adkim=r; aspf=r` | Every source in reports identified and classified |
| **2. Remediate** | 14–30 days | unchanged | **100% of legitimate sources aligned.** No exceptions, no "we'll fix it later" |
| **3. Quarantine 10%** | 7 days | `p=quarantine; pct=10` | No legitimate mail in spam; no complaints |
| **4. Quarantine 50%** | 7 days | `pct=50` | Same |
| **5. Quarantine 100%** | 14 days | `p=quarantine; pct=100` | Two clean weeks. **Include a payroll cycle and a mass-notification send** |
| **6. Reject 10%** | 7 days | `p=reject; pct=10` | Clean |
| **7. Reject 50%** | 7 days | `pct=50` | Clean |
| **8. Reject 100%** | permanent | `v=DMARC1; p=reject; rua=...; fo=1; adkim=s; aspf=s` | Steady state |

### Ramp rules

- **Never skip Stage 2.** Every failed DMARC project skipped Stage 2.
- **Do not advance during**: the first two weeks of school, state testing, grade reporting,
  open enrollment, or a payroll week. If something breaks, it breaks then.
- **Advance on Tuesdays**, never Fridays. You want two business days of daylight.
- **Stage 5 must include a full mass-notification send and a payroll cycle.** Those are the
  flows that break, and they're periodic — a "clean" two weeks that missed both proves nothing.
- Tighten `adkim`/`aspf` from relaxed (`r`) to strict (`s`) only at Stage 8, and only if
  no sender depends on subdomain relaxation.
- **`ruf` (forensic reports) may contain message content.** Some receivers include headers
  and subjects — potentially student or staff information. Send `ruf` to a district-controlled
  mailbox, **never to a third-party hosted analyzer**, and apply the same PII discipline as
  everywhere else in this repo. `rua` (aggregate) contains no message content and is safe to
  process externally.

### Secondary domains

**Every domain that exists needs a DMARC record**, including domains that never send mail:

```dns
_dmarc.<PARKED_DOMAIN>.  IN  TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@<PRIMARY_DOMAIN>;"
```

A non-sending domain can go straight to `p=reject` — there's no legitimate mail to break.
Pair with `v=spf1 -all` and a null MX. **Do this on day one for parked domains**; it's free
and it's the district's old domain from the last rebrand that gets used against it.

**Rollback at any stage:** lower `p=` or reduce `pct=`. Effective within DNS TTL — keep the
`_dmarc` TTL at **300 seconds** through the entire ramp. Raise it only at Stage 8.

---

## 6. Subdomain strategy for stubborn senders

When a vendor genuinely cannot do aligned DKIM, don't hold the whole ramp for them.

Move them to a subdomain — `notices.<PRIMARY_DOMAIN>` — with its own SPF, its own DKIM, and
its own DMARC policy that can lag the parent:

```dns
_dmarc.notices.<PRIMARY_DOMAIN>.  IN  TXT  "v=DMARC1; p=none; rua=mailto:dmarc@<PRIMARY_DOMAIN>;"
```

The parent domain reaches `p=reject` on schedule while the problem sender sits at `p=none`
on a subdomain with a visible deadline.

**Two things to get right:**

- The parent's policy applies to subdomains **unless** `sp=` is set. If you want the parent
  at reject and a subdomain at none, you need the subdomain's own `_dmarc` record — which is
  what the example above does.
- **This is a bridge, not a destination.** A subdomain at `p=none` is still spoofable and
  still carries the district's name. Set a hard deadline, and treat "the vendor still can't
  do DKIM" as a procurement finding for the next contract cycle.

---

## 7. DMARC report analysis

`rua` reports are gzipped XML from every major receiver. Reading them by hand is not viable
past week one.

### Self-hosted: parsedmarc

Assumes a Docker host ([ASSUMPTIONS.md](../ASSUMPTIONS.md) §A7).

```yaml
# compose.yaml — parsedmarc + OpenSearch + Dashboards
# Place beside a .env holding OPENSEARCH_INITIAL_ADMIN_PASSWORD and IMAP credentials.
# .env is gitignored. Do not commit credentials.
services:
  opensearch:
    image: opensearchproject/opensearch:2
    container_name: parsedmarc-opensearch
    environment:
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms1g -Xmx1g"
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_INITIAL_ADMIN_PASSWORD}
    ulimits:
      memlock: { soft: -1, hard: -1 }
      nofile:  { soft: 65536, hard: 65536 }
    volumes:
      - opensearch-data:/usr/share/opensearch/data
    restart: unless-stopped

  dashboards:
    image: opensearchproject/opensearch-dashboards:2
    container_name: parsedmarc-dashboards
    environment:
      - OPENSEARCH_HOSTS=["https://opensearch:9200"]
    ports:
      - "127.0.0.1:5601:5601"   # bind to loopback; front with Traefik + Tailscale
    depends_on: [opensearch]
    restart: unless-stopped

  parsedmarc:
    image: ghcr.io/domainaware/parsedmarc:latest
    container_name: parsedmarc
    volumes:
      - ./parsedmarc.ini:/etc/parsedmarc.ini:ro
    depends_on: [opensearch]
    restart: unless-stopped

volumes:
  opensearch-data:
```

```ini
; parsedmarc.ini
[general]
save_aggregate = True
save_forensic  = True

[imap]
host = imap.gmail.com
port = 993
ssl  = True
user = dmarc@<PRIMARY_DOMAIN>
; App password, or OAuth. Keep it out of this file in production - use env or a secret store.
password = ${IMAP_PASSWORD}

[mailbox]
watch = True
delete = False
archive_folder = Archive

[opensearch]
hosts = https://opensearch:9200
ssl = True
```

**Operational notes:**

- The `dmarc@` mailbox receives high volume — **exclude it from the §5 content compliance
  rules** in [docs/01](01-gmail.md), or reports get banner-injected and parsing gets noisy.
- **Do not expose Dashboards to the internet.** Bound to loopback above; front it with
  Traefik behind Tailscale.
- Retain 13 months to cover a full school year plus year-over-year comparison.
- If DKIM app passwords are used for IMAP, note that app-specific passwords are themselves
  audited in [audit/gam/05-app-passwords.sh](../audit/gam/05-app-passwords.sh) — document
  this one as a known, owned exception so it doesn't get revoked by a future audit sweep.

### Hosted alternatives

Viable if there's no Docker host: Dmarcian, Valimail, EasyDMARC, Postmark's free DMARC
digest, Cloudflare DMARC Management. **Send only `rua` to a hosted analyzer, never `ruf`**
(§5) — forensic reports can carry message content.

---

## 8. Inbound DMARC

Everything above is about **outbound** — stopping others from spoofing the district. Inbound
handling — what Gmail does with *others'* DMARC failures — is
[docs/01-gmail.md](01-gmail.md) §3, specifically **Protect against any unauthenticated
emails**.

Note the deliberate asymmetry: this document pushes the district to `p=reject`, while
doc 01 keeps *inbound* unauthenticated mail at **warning** for staff. Not inconsistent —
different risk calculus. Your own domain's alignment is under your control and worth
enforcing hard. Every small vendor's and PTA volunteer's alignment is not, and quarantining
all of it buries real detections.

**If a third-party gateway fronts Google** ([ASSUMPTIONS.md](../ASSUMPTIONS.md) §A4), inbound
DMARC is evaluated at the gateway and Gmail sees the gateway's IP. Configure Gmail's inbound
gateway settings so Google reads the **original** sender IP, or the doc 01 spoofing
protections operate on the wrong data and quietly stop working.

---

## 9. Verification checklist

- [ ] Every sending system inventoried — [config/district-profile.md](../config/district-profile.md)
- [ ] SPF record present, single record, **under 10 lookups**, verified with a checker
- [ ] SPF published for **every** domain including parked ones
- [ ] Google DKIM generated at 2048-bit and **authenticating** for every domain
- [ ] Third-party DKIM configured **and alignment verified** (`d=` matches From: domain)
- [ ] 48+ hours of SPF/DKIM authentication before publishing DMARC
- [ ] `_dmarc` TTL at 300s for the ramp
- [ ] `p=none` with `rua` published; reports flowing to a district-controlled mailbox
- [ ] `ruf` going only to a district-controlled mailbox, never a third party
- [ ] parsedmarc (or alternative) ingesting and dashboards readable
- [ ] **Every source in reports identified** — no unknowns
- [ ] **100% of legitimate sources aligned** before Stage 3
- [ ] Stage 5 spanned a full mass-notification send and a payroll cycle
- [ ] Parked/secondary domains at `p=reject` with `v=spf1 -all` and null MX
- [ ] Advancement dates avoid start-of-year, testing, grade reporting, payroll weeks
- [ ] Rollback procedure and TTL confirmed before each advancement

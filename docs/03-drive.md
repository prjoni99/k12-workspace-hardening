# 03 — Drive & Docs

Research date **2026-08-20**. All paths under
`Admin console > Apps > Google Workspace > Drive and Docs`.

Drive matters here for two distinct reasons: **share notifications are a phishing delivery
channel** (T7), and **over-broad sharing is how a single compromised account becomes a
student-data breach** (T11).

---

## 1. The constraint that shapes this whole document

Parents are external users. Staff must be able to share a permission slip, a progress
report, or a field-trip form with a guardian's personal Gmail address. **Any Drive policy
that blocks staff external sharing breaks the district.**

So: **students are restricted, staff are warned.** That asymmetry runs through every table
below and is not an oversight.

---

## 2. Sharing settings — the core table

**Path:** `Admin console > Apps > Google Workspace > Drive and Docs > Sharing settings > Sharing options`
([source](https://knowledge.workspace.google.com/admin/security/create-and-manage-trust-rules-for-drive-sharing),
[source](https://support.google.com/a/answer/60781))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Sharing outside of `<PRIMARY_DOMAIN>` | Drive and Docs > Sharing settings > Sharing options | **On** | **Off**, or **allowlisted domains only** | On | On | All | Students cannot share to personal Gmail / other districts. Staff↔guardian sharing preserved | [ref](https://support.google.com/a/answer/60781) |
| Warn when files are shared outside the organization | same | **On** | On (if sharing enabled) | On | On | All | Staff see a confirmation before external sharing. Cheap, effective, near-zero complaints | [ref](https://support.google.com/a/answer/60781) |
| Warn when sharing with allowlisted domains | same | On | On | On | On | All | Applies the same friction to allowlisted domains — the district isn't the only one who can be compromised | [ref](https://support.google.com/a/answer/60781) |
| Allow users to receive files from outside the organization | same | On | **Off** | On | On | All | Students can't be sent files by arbitrary external accounts. **This is a grooming/lure vector, not only a phishing one** | [ref](https://support.google.com/a/answer/60781) |
| Publish files to the web / "anyone with the link" visibility | same | **Off** | **Off** | Off | Off | All | Removes public-link publishing. Check for existing public files first — see §3 | [ref](https://support.google.com/a/answer/60781) |
| **Default link sharing for new items** | same > *When users create items, default link sharing is:* | **Restricted** | **Restricted** | Restricted | Restricted | All | New files are private by default. **Highest-value low-friction setting in this doc** | [ref](https://support.google.com/a/answer/60781) |
| Distributing content outside the domain (who can) | same | Staff only | **No one** | Staff only | Staff only | All | — | [ref](https://support.google.com/a/answer/60781) |

### Why "Restricted" default link sharing earns its place

The default governs what happens when a user clicks Share and does nothing else thoughtful.
With a permissive default, every new document silently becomes reachable by link — and
links leak: pasted into Chat, forwarded in email, screenshotted, embedded in a Classroom
post that later goes to a different section. Setting the default to `Restricted` means
broad access becomes a deliberate act. It changes nothing about existing files and
generates almost no tickets.

### ⚠ Blast radius: student external sharing

**Flag before Phase 4.** Turning off student external sharing breaks:

- Students sharing work with a **parent's personal address** — common for portfolios,
  senior projects, college applications
- **Dual-enrollment** students sharing with a community-college account on another domain
- **Scholarship and college application** submissions requiring a shared document
- **Competition and club** submissions (robotics, DECA, science fair, yearbook vendors)
- Students at a **different district domain** in a shared regional program

**Recommended instead of a hard Off for high school:** allowlisted domains — the community
college, the regional consortium, known scholarship platforms. Reserve hard `Off` for
elementary and middle. Document the decision per grade band in
[config/district-profile.md](../config/district-profile.md); the table above shows the
strict end of the range, and moving off it is a legitimate call, not a failure.

**Impact + comms:** Real for high school. Announce a term ahead with the exception process.

**Rollback:** Immediate per-OU. Existing shares are unaffected by the change in either
direction — turning sharing off does **not** revoke shares already granted.

---

## 3. Before you change anything: find what's already exposed

**Do this first.** The settings above govern *future* sharing. They do nothing about the
document from 2019 that's been "anyone with the link" ever since.

1. **Investigation tool** (`Admin console > Security > Security center > Investigation tool`)
   → data source **Drive log events** → filter `Visibility = Public` or
   `Shared externally`. **[Standard]/[Plus]**
2. Sort by document owner OU. Expect concentrations in: former-employee accounts,
   student-teacher shared folders, and anything created for a since-ended grant program.
3. **Look specifically for**: files with SSNs, IEP documents, free/reduced lunch data,
   discipline records, medical/504 documentation, and staff evaluation files.
4. Remediate in bulk from the investigation tool — it can change file permissions across a
   result set. Full procedure in [docs/08-monitoring-response.md](08-monitoring-response.md) §5.

**[Fundamentals] fallback:** no investigation tool. Use
[audit/gam/](../audit/gam/) to enumerate externally-shared files per OU. Slower, works.

> Do this **before** flipping "publish to the web" off, so you know what you're about to
> break. Some public files are intentional — the district calendar PDF, a public board
> packet. Find those first and move them somewhere designed for it.

---

## 4. Shared drives

**Path:** `Admin console > Apps > Google Workspace > Drive and Docs > Manage shared drives`
and `> Sharing settings > Shared drive creation`
([source](https://support.google.com/a/answer/7662202))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Allow users to create shared drives | Drive and Docs > Sharing settings > Shared drive creation | **Off** (IT-provisioned) | **Off** | Off | On | All | Prevents shadow shared drives with no owner and no lifecycle. Requires a request process — build it before flipping this | [ref](https://support.google.com/a/answer/7662202) |
| Allow members outside the organization to be added | same | **Off** | Off | Off | Off | All | External members on a shared drive is a standing, persistent grant — much higher risk than a per-file share | [ref](https://support.google.com/a/answer/7662202) |
| Allow people outside the org to access files | same | Off | Off | Off | Off | All | — | [ref](https://support.google.com/a/answer/7662202) |
| Allow non-members to access files | same | Off | Off | Off | Off | All | — | [ref](https://support.google.com/a/answer/7662202) |

**Why shared drives get stricter treatment than My Drive.** A shared drive survives its
creator. When a staff member leaves, their My Drive is handled by offboarding; a shared
drive they created with an external member attached just keeps existing, with that external
account still holding access. Districts routinely discover five-year-old shared drives with
a departed vendor still a member.

**Existing shared drives:** audit membership at least annually. Look for external members,
departed staff, and drives with **no active manager** — an unmanaged shared drive is
un-offboardable.

**Impact + comms:** Turning off creation is felt by power users. **Stand up the request
process first** — a form, a 2-business-day SLA, and a naming convention. Without it, staff
work around you by reverting to My Drive folders, which is worse.

**Rollback:** Immediate.

---

## 5. Trust rules **[Standard]/[Plus]**

**Path:** `Admin console > Apps > Google Workspace > Drive and Docs > Sharing settings > Manage trust rules`
([source](https://knowledge.workspace.google.com/admin/security/create-and-manage-trust-rules-for-drive-sharing))

Trust rules replace the blunt sharing-settings toggles with granular control over who can
share with whom, **inside and outside** the organization. Actions available on trigger:
**Allow**, **Allow with warning**, or **Block**
([source](https://knowledge.workspace.google.com/admin/security/create-and-manage-trust-rules-for-drive-sharing)).

> **Default trust rules are permissive** — they allow broad sharing both inside and outside
> the organization ([source](https://knowledge.workspace.google.com/admin/security/create-and-manage-trust-rules-for-drive-sharing)).
> Enabling trust rules without writing any is not a security improvement.

Recommended rule set, in evaluation order:

| # | Rule | Source | Target | Action |
| --- | --- | --- | --- | --- |
| 1 | Students → external | `/Students/*` | Any external | **Block** (elementary/middle) / **Allow with warning** to allowlisted domains (high school) |
| 2 | Students → staff | `/Students/*` | `/Staff` | Allow |
| 3 | Students → students | `/Students/*` | `/Students/*` | Allow |
| 4 | Finance-HR → external | `/Staff/Finance-HR` | Any external | **Allow with warning** |
| 5 | Staff → external | `/Staff` | Any external | Allow with warning |
| 6 | Anyone → known-bad domains | any | lookalike domains from [playbooks/07](../playbooks/07-lookalike-domain-response.md) | **Block** |

Rule 6 is the one people forget and it is genuinely useful: when a lookalike domain is
discovered, blocking Drive sharing to it is a same-day containment action alongside the
email-side response.

**[Fundamentals] fallback:** the §2 sharing-settings toggles plus allowlisted domains.
Coarser — you get per-OU on/off and an allowlist, not per-source-target rules — but the
student-external and staff-warned outcomes are both achievable.

**Impact + comms:** Depends entirely on the rules written. Test each rule against one OU
before applying broadly; a mis-scoped Block rule looks exactly like an outage to users.

**Rollback:** Disable individual rules. Rules evaluate in order — check the order after any
change, because inserting a rule can silently shadow a later one.

---

## 6. DLP for Drive **[Standard]/[Plus]**

**Path:** `Admin console > Security > Access and data control > Data protection`
([source](https://knowledge.workspace.google.com/admin/getting-started/editions/compare-education-editions))

Google provides predefined detectors for common sensitive data types, usable in both Drive
DLP and Gmail content compliance
([source](https://knowledge.workspace.google.com/admin/gmail/advanced/enhance-rules-for-advanced-email-content-filtering-with-predefined-detectors)).

Recommended starting rules — **all in audit-only mode for the first 30 days**:

| # | Rule | Detects | Scope | Action (after tuning) |
| --- | --- | --- | --- | --- |
| 1 | SSN external sharing | US SSN | All OUs, external share | **Block** + alert |
| 2 | Student ID bulk | Custom regex for district student ID format | All OUs, external share | Warn + alert |
| 3 | Financial account data | Bank account / routing numbers | `/Staff/Finance-HR` | Warn + alert |
| 4 | Credential-looking content | Predefined detector | All OUs | Alert only |
| 5 | Health/medical terms | Custom keyword list | All OUs, external share | Warn + alert |

**Run in audit mode first. This is not optional caution.** DLP rules in a K-12 tenant
generate large volumes of unexpected true-positives — a nurse's spreadsheet, an SRO
incident log, a special-education caseload file. You need to see the shape of the data
before you start blocking, or you will block a special-education coordinator's daily work
on day one and lose the political capital to run DLP at all.

**Edition note:** the Education comparison lists basic DLP for Gmail and Drive under
**Fundamentals**, with full DLP capability at Standard/Plus
([source](https://knowledge.workspace.google.com/admin/getting-started/editions/compare-education-editions)).
Confirm which detectors and actions your edition exposes before designing rules against
capabilities you may not have.

**Impact + comms:** In blocking mode, significant. Warn staff who handle student records
specifically — they are the population that will hit these rules legitimately and they need
to know what to do when they do.

**Rollback:** Set rule to audit-only, or disable. Immediate.

---

## 7. Third-party Drive app access

**Path:** `Admin console > Apps > Google Workspace > Drive and Docs > Features and Applications`

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Allow users to install Google Drive apps | Drive and Docs > Features and Applications | **Off** | **Off** | Off | Off | All | Third-party apps can no longer be attached to Drive ad hoc | [ref](https://knowledge.workspace.google.com/admin/apps/control-which-third-party-and-internal-apps-access-google-workspace-data) |
| Drive SDK / allow users to access Drive with the Drive SDK API | same | Off | Off | Off | Off | All | Blocks API-level third-party Drive access outside approved apps | [ref](https://knowledge.workspace.google.com/admin/apps/control-which-third-party-and-internal-apps-access-google-workspace-data) |

This overlaps deliberately with [docs/07-oauth-app-control.md](07-oauth-app-control.md).
The API controls in doc 07 are the authoritative layer — these Drive-specific toggles are
defense in depth. **Configure both**; an app blocked by API controls but allowed here is
blocked, since API controls override
([source](https://support.google.com/a/answer/6089179)).

---

## 8. Malicious files in Drive

Drive scans for malware, but the useful posture is response, not prevention:

1. **Alert center** surfaces malicious-file detections — route them ([docs/08](08-monitoring-response.md) §2).
2. **Investigation tool** locates every copy and every share of a given file — a malicious
   file shared into a shared drive may have been copied many times.
3. **Remediate in bulk**: remove access, transfer ownership, or delete across the result set.
4. **Then check the account** that introduced it — a malicious file in Drive is usually a
   symptom of [playbooks/01](../playbooks/01-compromised-staff-account.md), not a
   standalone event.

**Share-notification phishing (T7):** an attacker shares a document with a victim; Google
sends a legitimate share notification carrying the attacker's message. It authenticates
because it is genuinely from Google. `Allow users to receive files from outside the
organization` = **Off** for students removes this vector for them entirely. For staff it
cannot be removed without breaking guardian communication — accept it, and cover it with
link warnings ([docs/01-gmail.md](01-gmail.md) §4) and reporting culture
([docs/08](08-monitoring-response.md) §7).

---

## Rollback summary

| Section | Rollback | Speed | Residue |
| --- | --- | --- | --- |
| §2 Sharing settings | Reset per-OU toggles | Immediate | **Existing shares are never revoked by a settings change** |
| §4 Shared drives | Re-enable creation | Immediate | Drives created meanwhile persist |
| §5 Trust rules | Disable rule | Immediate | Check rule ordering after any change |
| §6 DLP | Set to audit-only | Immediate | Blocked actions are not retroactively allowed |
| §7 Third-party apps | Re-enable | Immediate | Previously-granted tokens survive — revoke separately ([docs/07](07-oauth-app-control.md)) |

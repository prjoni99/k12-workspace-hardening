# 05 — Chat, Meet, Classroom, Gemini, Takeout & Service Hygiene

Research date **2026-08-20**.

Two goals: close the non-Gmail communication channels students can be reached through, and
**shrink the number of Google services an attacker can abuse to send an authenticated lure**
(T7).

---

## 1. Age-based access — set this first

**Path:** `Admin console > Directory > Users` (age designation) and the age-based access
settings ([source](https://knowledge.workspace.google.com/admin/getting-started/editions/control-access-to-google-services-by-age))

Google applies different default protections to users designated **under 18**, and the
under-18 designation is what drives the third-party app restrictions in
[docs/07-oauth-app-control.md](07-oauth-app-control.md) §4.

**Verify before anything else in this doc:** that every student OU is correctly age-designated.
Districts commonly find high school students designated 18+ because of a bulk import
default, which silently removes protections from ~4,000 minors. This is a five-minute check
with large consequences.

---

## 2. Google Chat

**Path:** `Admin console > Apps > Google Workspace > Google Chat > External chat settings`
([source](https://knowledge.workspace.google.com/admin/chat/control-external-chat-and-spaces-chat-options))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| External chat | Chat > External chat settings | **Restricted to allowlisted domains** | **Off** | Restricted to allowlisted domains | Restricted to allowlisted domains | All | Students cannot be contacted by any external account via Chat | [ref](https://knowledge.workspace.google.com/admin/chat/control-external-chat-and-spaces-chat-options) |
| External spaces & group DMs | same | Off | **Off** | Off | Off | All | No external multi-party spaces | same |
| Chat history | Chat > Chat settings > History for spaces | On (default on) | **On, admin-controlled** | On | On | All | History must be retained for investigation and for student-safety review | [VERIFY exact path] |
| Chat apps / bots | Chat > Chat apps | Admin-approved only | **Off** | Admin-approved only | Admin-approved only | All | Chat bots are an under-reviewed third-party access path — treat as OAuth apps ([docs/07](07-oauth-app-control.md)) | [VERIFY exact path] |

**Why external Chat off for students is non-negotiable.** It is a direct, private,
real-time channel from an arbitrary external adult to a minor, inside a district-issued
account. That is a student-safety control before it is a phishing control. The phishing
benefit (removing a lure channel that bypasses every email control) is a bonus.

**Chat history on, admin-controlled, for students** matters for a reason that isn't
security: when a bullying or safety incident is investigated, history is the evidence. If
students can turn history off, that evidence doesn't exist.

**Impact + comms:** Low for students — most don't use Chat with external parties. Moderate
for staff if the district collaborates with external partners over Chat; the allowlist
handles known partners.

**Rollback:** Immediate per-OU.

---

## 3. Google Meet

**Path:** `Admin console > Apps > Google Workspace > Google Meet > Meet safety settings`

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Who can join meetings created by this OU | Meet > Meet safety settings > Joining | Anyone (guardians must join) | **Only users signed in to `<PRIMARY_DOMAIN>`** | Anyone | Anyone | All | External adults cannot join student-created meetings | [VERIFY exact path] |
| Which meetings users in this OU can join | same | Any | **Only `<PRIMARY_DOMAIN>` meetings** | Any | Any | All | Students cannot join arbitrary external meetings from a district account | [VERIFY] |
| Who can host / start meetings | same | All staff | **Off — students cannot create** | All staff | All staff | All | Removes student-hosted unmoderated meetings. **Check first** — some instructional models rely on student-led breakouts | [VERIFY] |
| Host management / knocking | same | On | On | On | On | All | Host approval required for external joiners | [VERIFY] |

> **`[VERIFY]`** — Meet safety settings have been reorganized more than once. The
> recommendations are stable; confirm the current sub-page names in your console.

**⚠ Blast radius: students cannot create meetings.** Breaks student-led breakout rooms,
peer tutoring, club meetings, and some project-based learning models. **Check with
instructional technology before applying** — this is exactly the kind of restriction the
"student-facing restrictions must not break instruction" rule exists to catch. If it
conflicts, keep student meeting creation but enforce domain-only joining, which retains
most of the benefit.

**Rollback:** Immediate per-OU.

---

## 4. Google Classroom

**Path:** `Admin console > Apps > Additional Google services > Google Classroom > Class settings`

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Who can join classes in your domain | Classroom > Class settings | **Only users in your domain** | Only users in your domain | — | — | All | External accounts cannot join district classes | [VERIFY exact path] |
| Which classes users in your domain can join | same | **Only classes in your domain** | Only classes in your domain | — | — | All | Students cannot join an external Classroom from a district account — closes a real lure ("join my class for free tutoring") | [VERIFY] |
| Who can create classes | same | **Verified teachers only** | Off | — | — | All | Students cannot create classes and impersonate a teacher. Requires the verified-teachers group to be maintained | [VERIFY] |
| Guardian email summaries | same | Per district policy | — | — | — | All | Legitimate guardian channel — keep, and verify guardian addresses through the SIS, not by self-service | [VERIFY] |

**Classroom-notification phishing is common and effective.** A fake "you've been invited to
a class" or "new assignment posted" email is highly credible to a student. Domain-restricted
class membership means the real notifications only ever come from inside the district, which
makes the fake ones distinguishable — but only if students are told that. Put it in the
student comms.

**"Verified teachers only" needs maintenance.** New hires can't create classes until they're
in the group. Wire this into onboarding or the first week of school produces a support
queue.

---

## 5. Gemini and generative AI

**Path:** `Admin console > Apps > Google Workspace > Gemini` /
`Generative AI` — service-level access is managed per OU or configuration group
([source](https://knowledge.workspace.google.com/admin/gemini/manage-access-to-gemini-features-in-workspace-services))

**Gemini in Classroom is ON by default for users of all ages**
([source](https://knowledge.workspace.google.com/admin/getting-started/editions/manage-access-to-gemini-in-classroom)) —
so this is another "default is permissive, doing nothing is a decision" case.

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini app | Gemini > Gemini app settings | On | **Per district AI policy** — Off if none exists | On | On | Varies | Don't enable district-wide generative AI for minors without a written policy and guardian communication | [ref](https://support.google.com/a/answer/14571493) |
| Gemini in Workspace services (Gmail, Docs, Drive) | Gemini > Manage access to Gemini features | On | Per policy | **Review — see below** | On | Varies | — | [ref](https://knowledge.workspace.google.com/admin/gemini/manage-access-to-gemini-features-in-workspace-services) |
| Gemini in Classroom | Gemini > Gemini in Classroom | Per policy | Per policy | — | — | Varies | **ON by default for all ages** — an affirmative decision either way | [ref](https://knowledge.workspace.google.com/admin/gemini/manage-access-to-gemini-in-classroom) |
| Ask Gemini in Meet | Meet > Ask Gemini | Per policy | Off | Per policy | Per policy | Varies | Meeting transcription/summarization has its own records and consent implications | [ref](https://knowledge.workspace.google.com/admin/meet/turn-ask-gemini-on-or-off-for-meet) |

### The prompt-injection angle

An AI assistant that reads email on a user's behalf will read **attacker-controlled text**,
because that is what inbound email is. Instructions embedded in a message body — including
in white-on-white text, tiny fonts, or an attachment — are input to the model, and a
summarize-my-inbox feature processes them the same as any other content.

Practical implications for a district:

- **Treat AI-generated summaries as untrusted for action.** A summary saying "the CFO needs
  a wire transfer approved" carries no more authority than the email it summarized. Say
  this explicitly in Finance-HR training — it is a new failure mode and staff will not
  intuit it.
- **Do not let convenience erode verification.** The out-of-band callback rule in
  [playbooks/04](../playbooks/04-payroll-diversion-attempt.md) and
  [playbooks/05](../playbooks/05-vendor-invoice-fraud.md) applies regardless of what any
  assistant reports.
- Google's June 2026 advisory documents attackers hiding malicious instructions in cloud
  documents to evade filtering — "invisible pages"
  ([Google](https://blog.google/innovation-and-ai/technology/safety-security/fraud-scams-advisory-june-2026/)).
  The same technique targets anything that reads documents on a user's behalf.

> **`[VERIFY]`** — I found no Google admin control specifically governing prompt-injection
> resistance or restricting what Gemini may act on within email as of 2026-08-20. This is
> currently a **training and process** control, not a configuration one. Do not tell
> leadership there's a setting for it.

**Edition note:** Gemini availability varies by edition and add-on and has changed
repeatedly. Confirm what your licensing actually includes before designing policy around it.

---

## 6. Google Takeout

**Path:** `Admin console > Apps > Additional Google services` → Takeout service, or
`Admin console > Account > Account settings > Takeout` — **`[VERIFY]` which applies in your
console**; Google has moved this control.

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Google Takeout for Workspace services | see path note | **On** (offboarding, records requests) | **Off** | On | On | All | Students cannot bulk-export their account data | [VERIFY] |

**Why off for students.** A compromised student account with Takeout enabled is a bulk data
exfiltration tool — one export, everything at once. Students also have no legitimate need to
mass-export a district-owned account; graduation data transfer, where the district offers
it, should be an administered process, not self-service.

**Consider the graduation exception explicitly.** Some districts allow seniors a Takeout
window before accounts are deprovisioned. If yours does, make it a time-boxed OU move
(`/Students/Graduating-Export`) for a defined window, not a standing permission.

---

## 7. Service hygiene — turn off what you don't use

**Path:** `Admin console > Apps > Additional Google services` (and `> Google Workspace` for
core services), per OU

**This is the T7 mitigation.** Every enabled Google service is a service an attacker can use
to generate an authentically-signed, perfectly-authenticated notification email to your
users. You cannot stop Google notifications from being trustworthy — you can reduce how
many kinds of them exist in your tenant.

### Sweep procedure

1. Enumerate every service, per OU:
   [audit/gam/08-ou-service-state.sh](../audit/gam/08-ou-service-state.sh)
2. For each **On** service, answer: *does an identified group of users use this for
   instruction or operations?* Not "might someone" — is there a known use.
3. If no → turn **Off** for all OUs.
4. If yes for some → turn Off for OUs that don't need it, starting with students.
5. Re-run quarterly. New Google services **arrive enabled by default** in many cases, so
   this sweep is a recurring task, not a one-time project.

### Common candidates

| Service | Typical district reality | Recommendation |
| --- | --- | --- |
| **AppSheet** | Almost never used | **Off** for all OUs unless a named owner exists. App-building + data access is meaningful surface |
| Google Ads / Merchant Center | Never | Off |
| Blogger | Legacy, rarely current | Off unless actively used |
| Google Groups (consumer, not Workspace Groups) | Rarely | Off — distinct from Groups for Business |
| Google+ / legacy social | Gone or vestigial | Off |
| Third-party / unlisted "Additional services" | Long tail nobody reviewed | Off by default; enable on request |
| Google Photos | Sometimes instructional | Off for students unless there's a use |
| YouTube | Instructional, needs restricted-mode config | Configure, don't disable |
| Google Sites | Sometimes instructional | Keep if used; note it's a documented ClickFix lure host |

> **On AppSheet specifically:** I did not find current reporting documenting AppSheet abuse
> in phishing chains, despite it being named in the source brief. Turning it off is
> justified as **attack-surface reduction for an unused service** — a defensible, honest
> rationale. Don't claim a campaign that isn't documented; the surface-reduction argument
> stands on its own.

**Impact + comms:** Usually zero, occasionally sharp. The failure mode is turning off a
service one teacher built a whole unit around. **Announce the sweep list two weeks ahead
with a "tell us if you use this" reply path.** That two-week window is the entire
difference between a clean sweep and an angry email from a department chair.

**Rollback:** Immediate per-service, per-OU. Data is retained while a service is off;
turning it back on restores access.

---

## 8. Quick reference — student OU target state

| Service | Student setting |
| --- | --- |
| Chat — external | Off |
| Chat — external spaces/DMs | Off |
| Chat — history | On, admin-controlled |
| Meet — join scope | Domain only, both directions |
| Classroom — membership | Domain only, both directions |
| Classroom — create classes | Off |
| Gemini | Per written AI policy; Off absent one |
| Takeout | Off |
| AppSheet | Off |
| Drive external sharing | Off / allowlisted ([docs/03](03-drive.md)) |
| POP/IMAP | Off ([docs/01](01-gmail.md)) |
| External forwarding | Off ([docs/01](01-gmail.md)) |
| Self-service password recovery | Off ([docs/06](06-accounts-mfa-admins.md)) |

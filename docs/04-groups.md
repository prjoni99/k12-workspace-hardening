# 04 — Groups

Research date **2026-08-20**. Paths under
`Admin console > Apps > Google Workspace > Groups for Business` and
`Admin console > Directory > Groups`.

**This is the single control that stops one spoofed email from hitting every employee in
the district.** It is also the most commonly neglected, because Groups are usually
configured once during migration and never revisited.

---

## 1. Why this is the highest-leverage doc in the repo per hour of effort

Every control in [docs/01-gmail.md](01-gmail.md) reduces the *probability* a phishing
message is delivered. This one reduces the *blast radius* when one is.

An open `all-staff@<PRIMARY_DOMAIN>` group means a single message — from anyone, anywhere
— reaches every employee simultaneously. That is the difference between an incident where
three people saw a phish and an incident where 1,200 people did, forty of them clicked, and
the help desk is on fire for two days. The attacker doesn't need to guess addresses; the
group name is on the district website.

**The default posture in most migrated tenants is far too open**, because Groups
permissions were set to "make it work" during migration and inherited forward ever since.

Maps to **T1** and **T9** in [docs/00-threat-landscape.md](00-threat-landscape.md).

---

## 2. Organization-wide Groups policy

**Path:** `Admin console > Apps > Google Workspace > Groups for Business > Sharing settings`
([source](https://support.google.com/a/answer/167097))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Who can create groups | Groups for Business > Sharing settings > Creating groups | **Admins only** | Admins only | Admins only | Admins only | All | Users can't self-serve groups. **Also structurally prevents external members and external posting** — see below | [ref](https://support.google.com/a/answer/167097) |
| Default for "Who can view conversations" | same > Default for permissions | **Group members** | Group members | Group members | Group members | All | Other defaults derive from this one, so setting it correctly cascades | [ref](https://support.google.com/a/answer/167097) |
| Group owners can allow external members | same | **Off** | Off | Off | Off | All | No external accounts in district groups | [ref](https://knowledge.workspace.google.com/admin/groups/options-for-limiting-group-access-and-activity) |
| Group owners can allow incoming email from outside the organization | same | **Off** | Off | Off | Off | All | **The core control.** External senders cannot post to district groups at all | [ref](https://knowledge.workspace.google.com/admin/groups/options-for-limiting-group-access-and-activity) |
| Group owners can hide groups from the directory | same | Off | Off | Off | Off | All | Keeps IT's inventory of groups complete | [ref](https://support.google.com/a/answer/167097) |

### The compounding effect of "Admins only"

Restricting group creation to admins does more than prevent group sprawl: **if users are
not allowed to create groups, group owners cannot add external members or allow external
users to send messages to their groups**
([source](https://support.google.com/a/answer/167097)).

One setting, three outcomes. This is the highest-value single toggle in the document.

### ⚠ Blast radius: turning off group creation

Flag before Phase 1. Check for legitimate self-service group use:

- Teachers creating groups for a club, team, or grade-level PLC
- Committees and school-improvement teams forming ad hoc
- Departments using groups as informal collaboration spaces
- **Automated provisioning** — if the SIS, a sync tool, or a script creates groups, it must
  run as an account with group-creation rights, or provisioning silently breaks

That last one is the real trap: SIS-driven group provisioning failing is invisible for
weeks, surfacing as "my class list is wrong" rather than "group creation is broken."

**Mitigation:** a group-request form with a 2-business-day SLA, plus verified exemption for
service accounts. Build it before flipping the setting.

**Impact + comms:** Moderate. Announce with the request process, not before it exists.

**Rollback:** Immediate.

---

## 3. Audit existing groups — do this before anything else

**Changing the org-wide default does not change existing groups.** Every group created
under the old policy keeps its old permissions. This audit is the actual work of this
document; §2 just stops the bleeding.

**Path:** `Admin console > Directory > Groups` → select group → **Access settings**
**Script:** [audit/gam/06-group-settings.sh](../audit/gam/06-group-settings.sh)

### Triage in this order

**Tier 1 — District-wide distribution lists.** `all-staff@`, `all-teachers@`,
`all-employees@`, `everyone@`. Highest blast radius in the domain.

| Setting | Required value |
| --- | --- |
| Who can post | **Only managers/owners** (or a named authorized-senders group) |
| Who can join | Only invited / admin-added |
| Allow external members | **Off** |
| Allow posting from outside the organization | **Off** |
| Message moderation | **Moderate all messages** from non-owners |
| Who can view members | Group members / managers |

**Tier 2 — School-wide lists.** `staff-<school>@`, `teachers-<school>@`. Same settings.
A single school's staff list is still hundreds of people.

**Tier 3 — Role and department lists.** `principals@`, `finance@`, `admins@`, `sped@`.
Internal-only posting; moderation optional. **`principals@` and `finance@` deserve Tier 1
treatment** — they are precisely the lists an attacker most wants.

**Tier 4 — Everything else.** Team, club, committee, project groups. Confirm no external
members, no external posting. Bulk-fixable via GAM.

### Findings to expect

Real audits routinely surface, in roughly this frequency order:

- Groups where **"Anyone on the web can post"** — set during migration, never revisited
- Groups with external members from a **long-finished** grant, pilot, or vendor engagement
- Groups owned by **departed staff** — orphaned, no one can change the settings
- Groups whose **address is published on the district website**, open to external posting
- **Nested groups** where a locked-down parent contains a wide-open child — the child's
  permissions govern what reaches the child's members, so a hardened `all-staff@` can still
  be fed by an open sub-group

Nested groups are the one that gets missed. Check membership *of* groups, not just members
*in* them.

---

## 4. Locking down all-staff — the authorized-senders pattern

The failure mode of "only owners can post" is that the list becomes unusable: HR needs to
send benefits notices, the superintendent's office sends board updates, transportation
sends weather closures at 5am. If posting is too hard, someone opens it back up.

**Pattern that survives contact with reality:**

1. Create `all-staff-senders@<PRIMARY_DOMAIN>` — a small group of accounts genuinely
   authorized to reach every employee. Typically: superintendent's office, HR director,
   communications, technology director, transportation/operations, safety.
2. On `all-staff@`, set **Who can post** to that group.
3. Set **message moderation** to moderate anything from outside that group, so a legitimate
   sender who isn't on the list gets a delay, not a bounce.
4. Name **two moderators**, not one, with explicit coverage for breaks.
5. Review the sender list each semester — people change roles.

**Emergency path matters.** Weather closures and safety notices cannot wait on moderation.
Either include those roles in the sender group directly, or use the mass-notification
system (which is the right tool for that traffic anyway) and reserve `all-staff@` for
non-urgent communication. Decide this explicitly rather than discovering it during a snow
event.

---

## 5. Directory visibility

**Path:** `Admin console > Directory > Directory settings > Sharing settings > Contact sharing`

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Contact sharing / directory visibility | Directory > Directory settings > Sharing settings | On (internal) | **Limited** — students should not browse a full staff+student directory | On (internal) | On (internal) | All | Reduces reconnaissance value and student-to-student targeting | [VERIFY path] |
| Group visibility in directory | Groups for Business > Sharing settings | Internal only | Internal only | Internal only | Internal only | All | Group addresses aren't externally enumerable | [ref](https://support.google.com/a/answer/167097) |

> **`[VERIFY]`** — I did not confirm the exact current navigation for contact-sharing and
> directory-visibility controls on 2026-08-20; Google has moved directory settings between
> `Directory > Directory settings` and the older `Apps > Google Workspace > Directory`
> location historically. Confirm in your console. The *recommendation* stands regardless of
> where the toggle now lives.

**A realistic note on directory restriction.** It has limited security value against T1 —
the superintendent's name and title are on the district website, and that's all the attacker
needs. Its real value is against **T9 (student-to-student)**, where browsing a full student
directory makes targeting trivial. Prioritize it for student OUs; treat it as low-priority
for staff.

---

## 6. Groups spoofing protection

Set in Gmail, not Groups: **Protect Groups from inbound emails spoofing your domain** →
`Quarantine`, scoped to **all groups** rather than private-only.

Full detail: [docs/01-gmail.md](01-gmail.md) §3.

**Why it needs saying twice.** The per-user spoofing protections do not cover mail
addressed to groups. A district can have employee-name spoofing perfectly configured and
still deliver a spoofed message to `all-staff@`, because that is a different code path and
a separate setting. It is genuinely easy to miss.

---

## 7. Ongoing cadence

| Task | Frequency |
| --- | --- |
| Tier 1 + Tier 2 group settings verified | **Monthly** |
| `all-staff-senders@` membership reviewed | Each semester |
| Full group audit — external members, external posting, orphans | **Quarterly** |
| Orphaned groups (departed owner) reassigned or deleted | Quarterly |
| Nested group membership reviewed | Quarterly |
| New groups reviewed against the tier model | At creation |

Script: [audit/gam/06-group-settings.sh](../audit/gam/06-group-settings.sh) — run it as
part of the quarterly audit and diff against the last run. The diff is more useful than the
report; it shows what someone changed.

---

## Rollback summary

| Section | Rollback | Speed | Residue |
| --- | --- | --- | --- |
| §2 Org-wide policy | Reset toggles | Immediate | **Existing groups keep their own settings either way** |
| §3 Per-group settings | Restore from audit output | Minutes | Keep pre-change GAM output — it *is* your restore point |
| §4 Authorized senders | Widen posting permission | Immediate | Moderated messages stay in the queue |
| §5 Directory visibility | Re-enable | Immediate | None |

> Before the quarterly bulk fix, run
> [audit/gam/06-group-settings.sh](../audit/gam/06-group-settings.sh) and **keep the
> output**. It is the only rollback you have for a bulk permission change.

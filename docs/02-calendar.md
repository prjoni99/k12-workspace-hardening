# 02 — Calendar

Research date **2026-08-20**. All paths under
`Admin console > Apps > Google Workspace > Calendar`.

Calendar is a phishing delivery channel that most districts have never configured,
because until six days ago the key control did not exist at the admin level.

---

## 1. Why Calendar is a delivery channel

A Calendar invitation carries attacker-controlled text and links, arrives with a
notification, and — historically — **appeared on the victim's calendar without any user
action**. It authenticates perfectly: SPF, DKIM, and DMARC all pass, because the message
genuinely originates from Google.

Check Point documented a campaign hitting **300 brands with 4,000+ emails in four weeks**
that passed all three authentication checks
([BleepingComputer](https://www.bleepingcomputer.com/news/security/ongoing-phishing-attack-abuses-google-calendar-to-bypass-spam-filters/)).
Google's own June 2026 fraud advisory lists fake renewal notices delivered directly as
Calendar invites among current AiTM tactics
([Google](https://blog.google/innovation-and-ai/technology/safety-security/fraud-scams-advisory-june-2026/)).

Two variants worth knowing:

- **Cancellation abuse.** The attacker cancels the event; the cancellation notice also
  carries attacker text. Users who "deleted the spam invite" can still receive follow-ups.
- **Chained lures.** Invite → Google Forms or Google Drawings → fake reCAPTCHA or support
  button → credential harvest. Every hop is on a Google domain
  ([Abnormal](https://abnormal.ai/attack-library/google-calendar-invite-phishing-google-drawings)).

Maps to **T6** in [docs/00-threat-landscape.md](00-threat-landscape.md).

---

## 2. The invitation control — new as of 2026-08-14

**This is the fix, it is brand new, and it does nothing until you change it.**

Google began rolling out admin-level control over Calendar invitation handling on
**2026-08-14**, to both Rapid and Scheduled release domains, gradual over up to 15 days,
**available to all Google Workspace customers**
([Workspace Updates, 2026-08-14](https://workspaceupdates.googleblog.com/2026/08/new-admin-controls-for-adding-invitations-to-Google-Calendar.html)).

**Path:** `Admin console > Apps > Google Workspace > Calendar > Advanced settings`
**Setting:** **`Add invitations to Calendar`**
([source](https://knowledge.workspace.google.com/admin/calendar/automatically-add-events-to-calendars))

The setting has **two independent values** — this is the part that's easy to get wrong:

| Sub-setting | What it does |
| --- | --- |
| **Least restrictive level available** | The floor. Users cannot choose anything *less* restrictive than this. **This is the enforcement control.** |
| **Default value** | What users get initially. Users may still move to any option at or above the floor. |

Both accept the same three values
([source](https://knowledge.workspace.google.com/admin/calendar/automatically-add-events-to-calendars)):

- `Invitations from everyone`
- `Invitations from known senders`
- `Invitations users have responded to via email`

**Default out of the box is "From everyone"** — the permissive, pre-2026 behavior
([Workspace Updates](https://workspaceupdates.googleblog.com/2026/08/new-admin-controls-for-adding-invitations-to-Google-Calendar.html)).
Doing nothing leaves the district exactly where it was.

### Recommended values

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Add invitations to Calendar — **Least restrictive level available** | Calendar > Advanced settings | `Invitations from known senders` | `Invitations users have responded to via email` | `Invitations from known senders` | `Invitations from known senders` | All | Users cannot opt back down to "from everyone" | [ref](https://knowledge.workspace.google.com/admin/calendar/automatically-add-events-to-calendars) |
| Add invitations to Calendar — **Default value** | same | `Invitations from known senders` | `Invitations users have responded to via email` | `Invitations from known senders` | `Invitations from known senders` | All | Applies without user action | same |

**Why students get the strictest tier.** Students have no legitimate need to receive
auto-added invitations from unknown external senders. Requiring an email response first
costs a student nothing — teachers and classmates are in-org and unaffected in practice —
while removing the vector entirely.

**Why staff get "known senders" rather than the strictest.** Staff receive genuine
external invitations from vendors, regional consortia, state agencies, and PD providers
where there has been prior email contact. "Known sender" covers contacts, in-org senders,
and **previously interacted-with** senders
([source](https://support.google.com/calendar/answer/13159188)), which captures nearly all
legitimate district use. The strictest tier would generate real friction for staff who
schedule externally, and friction produces workarounds.

### Behavior notes that will otherwise surprise you

- **Changes apply only to future invitations.** Existing spam already on calendars is not
  removed. Cleanup is §5.
- Propagation can take **up to 24 hours**, usually faster
  ([source](https://knowledge.workspace.google.com/admin/calendar/automatically-add-events-to-calendars)).
- Configuration groups override OUs, if you use them.
- **Roll out gradually.** If your tenant hasn't received the feature yet, the setting will
  not be present. That is expected as of 2026-08-20 — the 15-day window from 2026-08-14
  runs to roughly 2026-08-29. If absent, check back rather than concluding it doesn't exist.

**Impact + comms:** Low. Most users never notice. Staff who *do* schedule externally may
see an invitation arrive as email rather than a calendar entry. Comms template in
[comms/](../comms/).

**Rollback:** Immediate. Raise the least-restrictive level back to
`Invitations from everyone`. Note that user-level selections made under the stricter
policy persist — rolling back the policy does not reset individual choices.

---

## 3. External sharing of primary calendars

**Path:** `Admin console > Apps > Google Workspace > Calendar > Sharing settings`
→ **External sharing options for primary calendars**
([source](https://knowledge.workspace.google.com/admin/calendar/set-google-calendar-sharing-options))

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| External sharing options for primary calendars | Calendar > Sharing settings | **Only free/busy information (hide event details)** | **Only free/busy information** | Only free/busy information | Only free/busy information | All | External parties see busy/free blocks, never titles, attendees, locations, or descriptions | [ref](https://knowledge.workspace.google.com/admin/calendar/set-google-calendar-sharing-options) |
| Internal sharing options for primary calendars | Calendar > Sharing settings | Free/busy + event details (district norm) | **Only free/busy** | Free/busy + event details | Free/busy + event details | All | Staff scheduling keeps working; students don't broadcast schedules to each other | same |

**Why free/busy externally is the right call for a district.** Calendar event titles leak
a startling amount: `IEP meeting — [student]`, `Suspension hearing`, `Grievance — [staff]`,
`Interview — CFO candidate`. These are FERPA and personnel matters sitting in a field most
people never think of as a document. Free/busy removes the exposure entirely while leaving
external scheduling functional.

**Enforcement is real:** once external sharing is limited, users cannot exceed the limit on
individual events — a calendar shared out shows only "busy"
([source](https://knowledge.workspace.google.com/admin/calendar/set-google-calendar-sharing-options)).

**Impact + comms:** Moderate for the small number of staff who deliberately share full
calendars with external partners. Those cases should move to a **secondary shared calendar**
(secondary calendars are governed separately from primary), not to relaxing the primary
setting district-wide.

**Rollback:** Immediate per-OU.

---

## 4. External invitation warnings and related settings

| Setting | Path | Staff | Students | Finance-HR | Admins | Edition | Impact | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Allow external invitations / warn on external guests | Calendar > Sharing settings > External invitations | On, **with warning** | On, with warning | On, with warning | On, with warning | All | Users see a warning when an event includes guests outside `<PRIMARY_DOMAIN>`. Prevents accidental external exposure of internal meetings | [ref](https://knowledge.workspace.google.com/admin/calendar/allow-external-invitations-in-google-calendar-events) |

> **Do not turn external invitations off.** It would block guardian conferences, vendor
> meetings, and interagency coordination. Warning is the correct setting; blocking breaks
> the district.

---

## 5. Appointment schedule exposure review

Appointment schedules (booking pages) are a genuine and commonly-missed exposure. A public
booking page reveals a staff member's real availability pattern to anyone with the link,
and the booking form itself collects a name and email from whoever books.

**Review, per term:**

- [ ] Which staff have published appointment schedules? Counselors and administrators are
      the common cases.
- [ ] Are any booking pages linked from the public district website? A booking page for a
      counselor, publicly linked, is a scheduling channel an outside adult can use to reach
      a specific staff member — treat that as a student-safety review item, not just an IT one.
- [ ] Do booking forms collect more than name and email? Anything beyond that is data the
      district is now holding.
- [ ] **Students should not publish appointment schedules.** Confirm the Calendar service
      configuration for student OUs and disable if available.

> **`[VERIFY]`** — I could not confirm on 2026-08-20 whether a dedicated admin-console
> toggle exists to disable appointment schedule creation per OU, separate from turning off
> Calendar entirely. Check `Calendar > Sharing settings` and `Calendar > Advanced settings`
> in your console. If no such toggle exists, this is a policy-and-audit control, not a
> technical one — treat the term review above as the actual mitigation.

---

## 6. Cleaning up calendar spam already delivered

Policy changes apply only to **future** invitations. Anything already on calendars stays
there. Full procedure:
**[playbooks/06-mass-calendar-spam-cleanup.md](../playbooks/06-mass-calendar-spam-cleanup.md)**

Short version:

1. Change the §2 setting first — stop the inflow before cleaning.
2. Identify scope via the investigation tool / email log search on the Calendar
   notification mail.
3. Users delete via **"Report as spam"** in Calendar rather than plain delete — plain
   delete may notify the organizer that the address is live.
4. For widespread cases, GAM-based bulk deletion —
   [audit/gam/remediation/](../audit/gam/remediation/).
5. Confirm the §2 setting propagated; re-check after 24 hours.

---

## 7. End-user guidance

Staff can set their own preference at
**Calendar > Settings > Event settings > `Add invitations to my calendar`**, choosing
`Only if the sender is known`
([source](https://support.google.com/calendar/answer/13159188)).

**Tell them anyway, even though §2 enforces it.** Two reasons: the admin control is
rolling out gradually and may not have reached your tenant yet, and users who understand
*why* a setting exists report the invites that do get through. The user-facing explanation
of "known sender" — in your contacts, in your organization, or someone you've interacted
with before — is worth stating plainly, because users assume it means "someone I recognize",
which is not the same thing.

Comms template: [comms/](../comms/).

---

## Rollback summary

| Section | Rollback | Speed | Residue |
| --- | --- | --- | --- |
| §2 Invitation control | Raise least-restrictive level | Immediate (≤24h propagation) | User-level selections persist |
| §3 External sharing | Reset to previous level | Immediate | Previously-shared calendars re-expose details |
| §4 External invitations | Toggle warning off | Immediate | None |
| §6 Cleanup | Not reversible | — | Deleted events cannot be restored in bulk |

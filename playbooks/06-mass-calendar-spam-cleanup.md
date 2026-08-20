# Playbook 06 — Mass Calendar Spam Cleanup

**Trigger:** multiple users report unwanted events appearing on their calendars.

**Stop the inflow before cleaning, or you will clean the same calendars twice.**

---

## 1. Stop the inflow (0–15 min)

### 1.1 Set the invitation control
`Admin console > Apps > Google Workspace > Calendar > Advanced settings` →
**`Add invitations to Calendar`**

Set **Least restrictive level available** to `Invitations from known senders`
(students: `Invitations users have responded to via email`).

Full detail: [docs/02-calendar.md](../docs/02-calendar.md) §2

**Verify:** setting saved. **Propagation takes up to 24 hours**
([source](https://knowledge.workspace.google.com/admin/calendar/automatically-add-events-to-calendars)) —
plan the rest of this playbook accordingly.

> **If the setting is not present in your console:** the control began rolling out
> **2026-08-14** and rollout is gradual (up to 15 days)
> ([Workspace Updates](https://workspaceupdates.googleblog.com/2026/08/new-admin-controls-for-adding-invitations-to-Google-Calendar.html)).
> Proceed with §2 onward and set it as soon as it appears. In the interim, push the
> user-side setting via comms (§5).

### 1.2 Block the sender
Content compliance rule ([docs/01](../docs/01-gmail.md) §7) rejecting Calendar
notification mail from the offending sender domain. Narrow — envelope sender or domain
only — with an expiry date.

**Verify:** rule active; test with a subsequent message if one arrives.

---

## 2. Scope (15–30 min)

Calendar invitations arrive as email, so email tooling finds them.

`Security > Security center > Investigation tool` → **Gmail log events**

Search by: sender address, sender domain, subject fragment (typically `Invitation:`,
`Updated invitation:`, or `Cancelled event:`).

- [ ] Recipient count
- [ ] Date range — check whether this has been running quietly for weeks
- [ ] All sender variants identified — **campaigns rotate sender addresses**
- [ ] Event title(s) and any embedded URLs recorded

**Verify:** scope documented before any deletion.

---

## 3. Purge the notification mail (30–45 min)

Investigation tool → select → **Actions** → **Mark as phishing**

Prefer mark-as-phishing over delete: it feeds Google's classifier and preserves the sample.

Justification: `Calendar invitation phishing campaign — INC-<number>`

**Verify:** re-run the §2 search; messages show actioned.

> **This removes the email. It does not remove the calendar event.** Those are separate
> objects — §4.

---

## 4. Remove the events

### 4.1 Small scale — user self-service
Instruct users to use **"Report as spam"** in Google Calendar rather than plain **Delete**.

**Why this matters:** plain delete can send a response to the organizer, confirming the
mailbox is live and monitored. Report-as-spam does not, and it feeds Google's abuse signals.

**Verify:** spot-check with a few reporting users.

### 4.2 Large scale — bulk removal
For hundreds of affected calendars, per-user cleanup is not viable.

```bash
# Identify first - ALWAYS dry-run before deleting.
gam all users print events matchfield summary "<event title fragment>" \
  > audit/gam/out/calendar-spam-scope.csv

# Review the CSV. Confirm every row is spam. Then:
gam all users delete events matchfield summary "<event title fragment>" doit
```

**Rules:**
- **Always run the `print` form first and read the output.** Bulk-deleting calendar events
  is irreversible and there is no restore.
- Match on the most specific string available. A short or common fragment will match
  legitimate events.
- Test against a single user before running against `all users`.

**Verify:** re-run the `print` form — zero results. Spot-check three user calendars manually.

### 4.3 Watch for cancellation follow-ups
Attackers cancel events to deliver a second message, since cancellation notices also carry
attacker text ([BleepingComputer](https://www.bleepingcomputer.com/news/security/ongoing-phishing-attack-abuses-google-calendar-to-bypass-spam-filters/)).
Monitor for `Cancelled event:` notifications from the same sender for the next week.

---

## 5. Communicate

> Some of you have seen unexpected events appear on your Google Calendar. These are spam
> and in some cases phishing. **Do not click links inside them.**
>
> **To remove one:** open the event and choose **Report as spam** — not Delete. Delete can
> tell the sender your address is active.
>
> We have changed a district setting so invitations from unknown senders will no longer be
> added to your calendar automatically. You can also check this yourself:
> **Calendar > Settings > Event settings > "Add invitations to my calendar" >
> "Only if the sender is known."**

Template in [comms/](../comms/).

---

## 6. Verify and close

- [ ] Invitation control set and **propagated** (re-check after 24h)
- [ ] Sender blocked, with an expiry date on the rule
- [ ] Notification mail purged
- [ ] Events removed — verified by spot-check on at least three calendars
- [ ] No new events for 48 hours
- [ ] Anyone who clicked a link identified → [Playbook 01](01-compromised-staff-account.md)
- [ ] Cancellation follow-ups monitored for one week
- [ ] Calendar external sharing reviewed while you're in there —
      [docs/02](../docs/02-calendar.md) §3

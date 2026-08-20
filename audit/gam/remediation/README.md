# ⚠ REMEDIATION SCRIPTS — THESE MAKE CHANGES

**Everything in this directory modifies your tenant.** The scripts in the parent directory
are read-only; these are not.

---

## Rules

1. **Run the corresponding read-only audit first.** Know what you are changing before you
   change it.
2. **Every script defaults to dry-run.** You must pass `--commit` to make changes. This is
   deliberate, and do not remove it.
3. **Keep the audit output.** It is your only rollback for a bulk change. There is no undo
   button in GAM.
4. **Test against one account first.** Every script accepts a single-account argument.
5. **Not during**: the first two weeks of school, state testing, grade reporting, or a
   payroll week.
6. **Log what you ran, when, and why.** Scripts append to `out/remediation-log.txt`.

---

## Scripts

| Script | Does | Reversible? |
| --- | --- | --- |
| [revoke-tokens.sh](revoke-tokens.sh) | Revokes OAuth tokens and app passwords for an account | **No** — users must re-consent |
| [remove-forwarding.sh](remove-forwarding.sh) | Removes forwarding, forwarding addresses, and matching filters | **No** — record them first |
| [lockdown-group.sh](lockdown-group.sh) | Sets a group to internal-only, owner-post, moderated | Yes, if you saved prior settings |
| [bulk-reset-passwords.sh](bulk-reset-passwords.sh) | Resets passwords for a list of accounts | **No** |

---

## When each is appropriate

**revoke-tokens.sh** — during
[playbooks/01](../../../playbooks/01-compromised-staff-account.md) step 5, and at staff
offboarding. Suspending an account does not reliably revoke its OAuth grants; this does.

**remove-forwarding.sh** — during incident response, or as cleanup after
[docs/01](../../../docs/01-gmail.md) §5 turns the feature off. **The setting prevents new
rules; it does not remove existing ones.** Capture what you're removing first — some are
legitimate and users will ask.

**lockdown-group.sh** — bulk application of the
[docs/04](../../../docs/04-groups.md) §3 tier model. **Save
`06-group-settings.sh` output first**; it is the restore point.

**bulk-reset-passwords.sh** — mass student compromise,
[playbooks/02](../../../playbooks/02-compromised-student-account.md) §5. **Coordinate with
schools before running** — the front office absorbs the volume, and they need warning.

---

## Rollback

There is no general undo. Rollback is reconstruction from audit output:

| Change | Rollback |
| --- | --- |
| Tokens revoked | Users re-consent to legitimate apps individually |
| Forwarding removed | Re-create from the pre-change CSV — **which is why you keep it** |
| Group settings changed | Restore from `06-group-settings.sh` output |
| Passwords reset | Not reversible. Users get new credentials |

**If you did not keep the audit output, you do not have a rollback.** Say that out loud
before running anything here.

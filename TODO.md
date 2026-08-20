# TODO — K-12 Workspace Anti-Phishing Hardening Package

Working list. One commit per numbered deliverable, conventional commit messages.

## Phase A — Research (mandatory, before any doc)

- [x] Google Admin Help — verify every console path against current articles
      (**finding:** `support.google.com/a/answer/*` now 301-redirects to
      `knowledge.workspace.google.com` — cite the new canonical URLs)
- [x] Workspace Updates blog — last 12 months, Gmail/Calendar/Drive/Groups/admin
      (**finding:** Calendar invitation admin control shipped **2026-08-14**)
- [x] Education edition matrix — Fundamentals vs Standard vs Plus
- [x] CISA K-12 / MS-ISAC / K12 SIX / FBI IC3 — current district-targeted campaigns
- [x] Google-service-abuse phishing + AiTM kits (Tycoon 2FA)

## Phase B — Deliverables

- [x] 0. Repo scaffold, `TODO.md`, `ASSUMPTIONS.md`, `config/district-profile.md`
- [x] 1. `README.md` + `CLAUDE.md` — repo conventions
- [x] 2. `docs/00-threat-landscape.md`
- [x] 3. `docs/01-gmail.md`
- [x] 4. `docs/02-calendar.md`
- [x] 5. `docs/03-drive.md`
- [x] 6. `docs/04-groups.md`
- [x] 7. `docs/05-other-services.md`
- [x] 8. `docs/06-accounts-mfa-admins.md`
- [x] 9. `docs/07-oauth-app-control.md`
- [x] 10. `docs/08-monitoring-response.md`
- [x] 11. `docs/09-dmarc-spf-dkim.md`
- [x] 12. `playbooks/`
- [x] 13. `audit/gam/` + `audit/gam/remediation/`
- [x] 14. `checklists/rollout-phases.md` + `comms/`
- [x] 15. `docs/10-exec-summary.md`

## Phase C — Before this is executed in production

- [ ] District fills in `config/district-profile.md` (domains, OUs, bulk senders)
- [ ] Resolve every `[VERIFY]` tag against a live Admin console
- [ ] Bulk-sender inventory completed before any DMARC enforcement

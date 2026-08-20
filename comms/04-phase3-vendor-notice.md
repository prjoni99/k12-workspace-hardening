# Template 04 — Vendor Email Authentication Notice

**Send:** Phase 3 start · **To:** every vendor sending as `<PRIMARY_DOMAIN>`
**From:** Technology Director · **CC:** the district business owner for that vendor

---

**Subject: Action required — email authentication for <PRIMARY_DOMAIN> by [DATE]**

Hello,

`<DISTRICT_NAME>` is implementing DMARC enforcement on `<PRIMARY_DOMAIN>`. Your system sends
email using our domain, so this needs your attention.

**What's required**

Your platform must sign messages with **DKIM aligned to `<PRIMARY_DOMAIN>`** — meaning the
DKIM `d=` value must be `<PRIMARY_DOMAIN>` or a subdomain of it, not your own sending domain.

We will provide DNS records to publish; typically you provide CNAME values and we publish them.

**Timeline**

| Date | Stage |
| --- | --- |
| [DATE] | Monitoring begins — no impact |
| [DATE] | **Your alignment deadline** |
| [DATE] | Quarantine phase begins |
| [DATE] | **Reject — unaligned mail will not be delivered** |

**After the final date, mail from your platform using our domain will be rejected by
receiving mail servers if it is not aligned.** For a system that reaches parents, that means
those messages stop arriving. We would rather solve this now than have either of us find out
that way.

**Please confirm by [DATE]:**
1. Can your platform do DKIM signing aligned to our domain? (yes/no)
2. If yes — what DNS records do we publish, and what is your timeline?
3. If no — what alternatives do you support?

Technical contact: `<SECURITY_ALIAS>`

[Name]
Technology Director, `<DISTRICT_NAME>`

<div align="center">

[![Md. Sabbir Howlader — Full-Stack Engineer](/Images/banner.png)](https://realsabbir.dev)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&pause=1200&color=58A6FF&center=true&vCenter=true&width=640&height=42&lines=Identity+%26+device+trust;Immutable+Linux+workstations;Hand-written+Go+WebSocket+servers;Multi-tenant+SaaS+platforms">
  <source media="(prefers-color-scheme: light)" srcset="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&pause=1200&color=0969DA&center=true&vCenter=true&width=640&height=42&lines=Identity+%26+device+trust;Immutable+Linux+workstations;Hand-written+Go+WebSocket+servers;Multi-tenant+SaaS+platforms">
  <img alt="Identity &amp; device trust · Immutable Linux workstations · Hand-written Go WebSocket servers · Multi-tenant SaaS platforms" src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=20&pause=1200&color=58A6FF&center=true&vCenter=true&width=640&height=42&lines=Identity+%26+device+trust;Immutable+Linux+workstations;Hand-written+Go+WebSocket+servers;Multi-tenant+SaaS+platforms">
</picture>

<a href="https://realsabbir.dev"><img alt="realsabbir.dev" src="https://img.shields.io/badge/realsabbir.dev-58A6FF?style=for-the-badge&logo=googlechrome&logoColor=white&labelColor=0D1117"></a>
<a href="mailto:being.sabbirhowlader@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0D1117"></a>
<a href="https://linkedin.com/in/sabbiroffc"><img alt="LinkedIn" src="https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white&labelColor=0D1117"></a>
<a href="https://twitter.com/sabbir_offc"><img alt="X" src="https://img.shields.io/badge/X-1D9BF0?style=for-the-badge&logo=x&logoColor=white&labelColor=0D1117"></a>

</div>

## About

Full-stack engineer from Bangladesh. I build the internal platforms a company actually runs on — then
keep going past the browser into desktop clients, device identity and the operating system underneath.

- **Engineering at NeXbit LTD** — multi-tenant internal platforms: finance, lead, HR and POS systems
- **Day to day** — Next.js (App Router) + TypeScript, Tailwind v4, shadcn/ui, Prisma on Postgres
- **Backends in Go** — hand-written WebSocket servers, JWT auth, Web Push — and Node where it fits
- **Outside the browser** — Electron desktop clients, immutable Linux OS images, Python services
- **Currently deep in** — identity & device trust (device keypairs, OTP unlock, SSO) and on-device
  inference with `web-llm`
- **Reach me** — [being.sabbirhowlader@gmail.com](mailto:being.sabbirhowlader@gmail.com)

## Stack

<div align="center">

<sub><b>CORE</b></sub><br/>
<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=ts,js,nextjs,react,tailwind&theme=light">
  <img alt="TypeScript, JavaScript, Next.js, React, Tailwind" src="https://skillicons.dev/icons?i=ts,js,nextjs,react,tailwind&theme=dark">
</picture>

<sub><b>BACKEND &amp; DATA</b></sub><br/>
<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=go,nodejs,express,postgres,prisma,redis,mongodb&theme=light">
  <img alt="Go, Node.js, Express, Postgres, Prisma, Redis, MongoDB" src="https://skillicons.dev/icons?i=go,nodejs,express,postgres,prisma,redis,mongodb&theme=dark">
</picture>

<sub><b>PLATFORM &amp; TOOLING</b></sub><br/>
<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=electron,linux,python,docker,git,githubactions,vercel,figma,vscode&theme=light">
  <img alt="Electron, Linux, Python, Docker, Git, GitHub Actions, Vercel, Figma, VS Code" src="https://skillicons.dev/icons?i=electron,linux,python,docker,git,githubactions,vercel,figma,vscode&theme=dark">
</picture>

</div>

## Selected Work

### NeX OS
A hardened, centrally-managed, **immutable** workstation operating system. A normal daily-use machine
that happens to be encrypted, locked down and tamper-evident: `/usr` mounted read-only so nothing can
modify the OS at runtime, users are not administrators, and a whole fleet updates from one signed image.

`Linux` · `Immutable images` · `Fleet management` — *private*

### Enterprise Browser
An enterprise-first browser and identity platform. The Electron client stays locked at launch until
organizational OTP unlock; a device keypair is generated on first run and held in the OS keychain,
then registered for challenge/response login and SSO into internal apps. Paired with an identity
server and an HR/IT admin panel for devices, policies, approvals and audit.

`Electron` · `Next.js` · `Prisma` · `TypeScript` — *private* · [Signed installers →](https://github.com/sabbir-offc/enterprise-browser-releases)

### FinLedger v2
Multi-tenant financial ledger SaaS. Each organization gets isolated accounts, fund tracking with
auto-generated invoices, categorized expenses with line items and monthly budget limits, monthly
ledger carry-forward, multi-currency and reporting. Users belong to several organizations and switch
between them, with Owner / Admin / Accountant / Viewer roles granted per organization.

`Next.js 16` · `React 19` · `Prisma 7` · `Neon Postgres` · `Auth.js v5` — [Live →](https://financial-ledger-v2.vercel.app)

### TxnGuard
Transaction tracker for Bangladeshi mobile-banking agents (bKash / Nagad / Rocket / Upay). Shopkeepers
record who transacted with which ID, attach photo proof, flag suspicious entries and spot repeat
numbers at a glance — a practical guard against fraud and money bypass. Search, filters, per-filter
stats and one-click CSV export.

`Next.js 15` · `Prisma` · `Neon Postgres` · `Tailwind` — [Live →](https://txnguard.vercel.app)

### Chat
Real-time messaging with a Next.js client on a hand-written **Go** server: WebSockets, JWT auth,
Web Push notifications, and on-device inference through `web-llm`.

`Next.js` · `Go` · `Postgres (pgx)` · `shadcn/ui` — [Live →](https://chat-web-iota-eight.vercel.app)

### Domain Guard
Next.js admin panel for domain allowlisting. Review access requests by status, approve in one click
(allowlist + resolve + optional Slack ping), deny with a recorded reason, and keep an audit trail.

`Next.js` · `TypeScript` — [Repo →](https://github.com/sabbir-offc/domain-guard) · [Live →](https://domain-guard-iota.vercel.app)

### DevPulse
Issue-tracker API with JWT auth, contributor/maintainer roles and filtering by type and status.

`Node.js` · `Express` · `PostgreSQL` — [Repo →](https://github.com/sabbir-offc/l2-assignment-2-devpulse) · [API →](https://devpulse-gamma-nine.vercel.app)

## GitHub in Numbers

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=sabbir-offc&theme=github_dark">
  <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=sabbir-offc&theme=github">
  <img alt="Profile details" width="98%" src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=sabbir-offc&theme=github_dark">
</picture>

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.vercel.app?user=sabbir-offc&hide_border=true&background=0D1117&border=30363D&stroke=21262D&ring=58A6FF&fire=BF91F3&currStreakNum=E6EDF3&sideNums=8B949E&currStreakLabel=58A6FF&sideLabels=8B949E&dates=6E7681">
  <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.vercel.app?user=sabbir-offc&hide_border=true&background=FFFFFF&border=D0D7DE&stroke=D8DEE4&ring=0969DA&fire=8250DF&currStreakNum=1F2328&sideNums=57606A&currStreakLabel=0969DA&sideLabels=57606A&dates=6E7781">
  <img alt="Contribution streak" width="60%" src="https://streak-stats.vercel.app?user=sabbir-offc&hide_border=true&background=0D1117&border=30363D&stroke=21262D&ring=58A6FF&fire=BF91F3&currStreakNum=E6EDF3&sideNums=8B949E&currStreakLabel=58A6FF&sideLabels=8B949E&dates=6E7681">
</picture>

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=sabbir-offc&theme=github_dark">
  <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=sabbir-offc&theme=github">
  <img alt="Stats" width="49%" src="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=sabbir-offc&theme=github_dark">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=sabbir-offc&theme=github_dark">
  <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=sabbir-offc&theme=github">
  <img alt="Repos per language" width="49%" src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=sabbir-offc&theme=github_dark">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=sabbir-offc&theme=github_dark">
  <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=sabbir-offc&theme=github">
  <img alt="Most-committed languages" width="49%" src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=sabbir-offc&theme=github_dark">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=sabbir-offc&utcOffset=6&theme=github_dark">
  <source media="(prefers-color-scheme: light)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=sabbir-offc&utcOffset=6&theme=github">
  <img alt="Productive time" width="49%" src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=sabbir-offc&utcOffset=6&theme=github_dark">
</picture>

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=sabbir-offc&bg_color=0D1117&color=E6EDF3&line=58A6FF&point=BF91F3&area=true&area_color=58A6FF&hide_border=true&custom_title=Contribution%20Activity">
  <source media="(prefers-color-scheme: light)" srcset="https://github-readme-activity-graph.vercel.app/graph?username=sabbir-offc&bg_color=FFFFFF&color=1F2328&line=0969DA&point=8250DF&area=true&area_color=0969DA&hide_border=true&custom_title=Contribution%20Activity">
  <img alt="Contribution activity graph" width="98%" src="https://github-readme-activity-graph.vercel.app/graph?username=sabbir-offc&bg_color=0D1117&color=E6EDF3&line=58A6FF&point=BF91F3&area=true&area_color=58A6FF&hide_border=true&custom_title=Contribution%20Activity">
</picture>

<!--
  Self-hosted github-readme-stats. The public instance at github-readme-stats.vercel.app is
  permanently paused (503 DEPLOYMENT_PAUSED), so these two cards run from my own Vercel deploy of
  sabbir-offc/github-readme-stats. count_private + include_all_commits make them the only cards here
  that read private-repo commits directly. Uncomment and replace <DEPLOY-URL> once deployed.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://<DEPLOY-URL>/api?username=sabbir-offc&count_private=true&include_all_commits=true&show_icons=true&hide_border=true&bg_color=0D1117&title_color=58A6FF&icon_color=BF91F3&text_color=8B949E">
  <source media="(prefers-color-scheme: light)" srcset="https://<DEPLOY-URL>/api?username=sabbir-offc&count_private=true&include_all_commits=true&show_icons=true&hide_border=true&bg_color=FFFFFF&title_color=0969DA&icon_color=8250DF&text_color=57606A">
  <img alt="GitHub stats" width="49%" src="https://<DEPLOY-URL>/api?username=sabbir-offc&count_private=true&include_all_commits=true&show_icons=true&hide_border=true&bg_color=0D1117&title_color=58A6FF&icon_color=BF91F3&text_color=8B949E">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://<DEPLOY-URL>/api/top-langs/?username=sabbir-offc&count_private=true&layout=compact&langs_count=8&hide_border=true&bg_color=0D1117&title_color=58A6FF&text_color=8B949E">
  <source media="(prefers-color-scheme: light)" srcset="https://<DEPLOY-URL>/api/top-langs/?username=sabbir-offc&count_private=true&layout=compact&langs_count=8&hide_border=true&bg_color=FFFFFF&title_color=0969DA&text_color=57606A">
  <img alt="Top languages" width="49%" src="https://<DEPLOY-URL>/api/top-langs/?username=sabbir-offc&count_private=true&layout=compact&langs_count=8&hide_border=true&bg_color=0D1117&title_color=58A6FF&text_color=8B949E">
</picture>
-->

<sub>The streak and activity graph are built from the GitHub contribution calendar, so they include
private work — which is where most of my commits live.</sub>

</div>

<div align="right">
  <img alt="Profile views" src="https://komarev.com/ghpvc/?username=sabbir-offc&label=Profile%20views&color=58a6ff&style=flat-square">
</div>

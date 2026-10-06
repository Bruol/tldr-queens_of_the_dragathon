# TLDR; Lectures

Read-only lecture archive from the Viscon 2023 hackathon, hosted on Cloudflare Workers with static assets. The existing Django templates and SQLite database remain the content source. Django runs only when building the archive; the deployed site uses no Python server or database.

The archive preserves course pages, summary detail controls, lecture search, video links, and transcript downloads at their existing URLs. `/admin/` is not deployed. Only public lecture data is exported; Django users, sessions, and credentials are not uploaded.

## Build and deploy

Use Python 3.11 and Node.js 22 or later:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r TLDRserver/requirements.txt
npm ci
npm run build
npx wrangler login
npm run deploy
```

`cloudflare/build.py` exports the public views and CSS from `TLDRserver/db.sqlite3`. Search runs in the Worker against a generated topic index, using the same substring matching as SQLite. Download filenames use UTF-8 Content-Disposition encoding.

To update the archive, update the source database, rebuild, and deploy. Generated content is ignored by Git. GitHub Actions checks the export, Worker bundle, public pages, searches, download filenames, and missing routes on pushes and pull requests. Deployments are manual using the authenticated Wrangler CLI.

## Verify

```sh
npm run dev
# In another terminal with the Python virtual environment active:
python cloudflare/verify.py http://localhost:8787
# Or check the deployed site:
python cloudflare/verify.py https://tldr.bruol.me
```

## Fly.io rollback and retirement

The original Django application, Dockerfile, and Fly configuration remain available for rollback. Before migration, `tldr.bruol.me` resolved to Fly's IPv4 `66.241.124.34` and IPv6 `2a09:8280:1::67:1318:0`, and the Fly app was `tldrserver-proud-field-9619`.

For rollback, remove the Cloudflare Worker custom domain and restore those DNS records, then start the Fly machines if stopped. Keep Fly available until the Cloudflare custom domain passes verification. Retire the Fly app only after saving its machine configuration and checking whether it has volumes or other billable resources.

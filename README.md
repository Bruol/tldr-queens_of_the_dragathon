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

## Fly.io retirement

The production custom domain is `tldr.bruol.me`, served by the `tldr-lectures` Cloudflare Worker. The previous Fly.io app, `tldrserver-proud-field-9619`, was removed after the Cloudflare domain passed verification.

The Django source, SQLite content database, Dockerfile, and original Fly configuration remain in the repository. Restoring Fly would require creating a new app, updating `TLDRserver/fly.toml` and Django's allowed hosts, deploying from `TLDRserver/`, allocating IP addresses, and replacing the Cloudflare custom domain with the new Fly DNS records. The old Fly machines and IP addresses are no longer available.

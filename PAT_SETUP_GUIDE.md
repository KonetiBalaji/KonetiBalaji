# Personal Access Token (PAT) Setup Guide

Optional but recommended — a PAT raises API limits from 60 to 5,000 requests/hour.

---

## Step 1 — Create the Token

### Option A: Fine-Grained Token (Recommended)

1. **GitHub → Settings → Developer settings → Personal Access Tokens → Fine-grained tokens**
2. Click **"Generate new token"**
3. Fill in:
   - **Name:** `README Update Token`
   - **Expiration:** 1 year (or your preference)
   - **Repository access:** *Selected repositories* → pick `KonetiBalaji/KonetiBalaji`
4. **Permissions:**
   - Contents: **Read and Write**
   - Metadata: **Read**
5. Click **"Generate token"** and **copy it immediately** (it won't be shown again).

### Option B: Classic Token

1. **GitHub → Settings → Developer settings → Personal Access Tokens → Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Fill in:
   - **Note:** `README Update Token`
   - **Scopes:** check **`repo`**
4. Generate and copy.

---

## Step 2 — Add to Repository Secrets

1. Go to `https://github.com/KonetiBalaji/KonetiBalaji/settings/secrets/actions`
2. Click **"New repository secret"**
3. **Name:** `PAT_TOKEN`
4. **Value:** paste the token
5. Save.

---

## Step 3 — Verify

1. Go to **Actions** tab → **Update README with Latest Repos**
2. Click **"Run workflow"**
3. Confirm the run succeeds and the README updates.

---

## Security Tips

| Practice | Why |
|----------|-----|
| Use fine-grained tokens | Scoped to one repo, minimal permissions |
| Set an expiration | Limits blast radius if leaked |
| Never commit tokens | Always use repository secrets |
| Rotate annually | Good hygiene |

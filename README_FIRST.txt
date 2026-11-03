CAMBRIAN SUPABASE KEEP ALIVE — SETUP
====================================
1. Create a NEW GitHub repository named Cambrian-Keep-Alive (public if using GitHub Pages free hosting).
2. Upload the contents of this ZIP to the ROOT of that repository. Include the hidden .github folder and its workflows subfolder. GitHub's web uploader supports dragging the extracted folder contents.
3. In Supabase, open the CAMBRIAN ROTA project > SQL Editor. Paste keep_alive.sql and RUN it.
4. Repeat step 3 in the CAMBRIAN TSR project.
5. In the NEW GitHub repository, go to Settings > Secrets and variables > Actions > New repository secret. Add these FOUR secrets (one at a time):
   ROTA_SUPABASE_URL       = Supabase project URL for Rota
   ROTA_SERVICE_ROLE_KEY   = Supabase secret service_role key for Rota
   TSR_SUPABASE_URL        = Supabase project URL for TSR
   TSR_SERVICE_ROLE_KEY    = Supabase secret service_role key for TSR
   Find URL and keys in each Supabase project's Settings > API (or API Keys).
   Use a server-side service_role key, NOT an anon/publishable key. NEVER paste keys into HTML, commits, chat, or public files.
6. In repository Settings > Actions > General > Workflow permissions, enable Read and write permissions for GITHUB_TOKEN. Save.
7. Open repository Actions > Supabase Keep Alive > Run workflow > Run workflow. Wait for completion and check the log. It should report OK for both projects.
8. In Settings > Pages, select Deploy from a branch, branch main, folder /(root). Save. Wait for Pages to publish. Open your site's Pages URL shown by GitHub.
9. The scheduler will run twice a day at 05:17 and 17:17 UTC (UK winter time). In summer, those times are 06:17 and 18:17 BST. GitHub scheduled jobs may be delayed and may be disabled after 60 days of repository inactivity on public repositories; periodically check the Actions tab and re-enable if necessary.

NOTES
- The dashboard's REFRESH STATUS only reloads the latest result; RUN CHECK NOW opens GitHub Actions, where you must trigger the workflow.
- GitHub Pages publishes status.json publicly, but never publishes credentials.
- Each heartbeat updates only the new keep_alive table, not any existing app data.
- Supabase Free-tier pausing rules may change; heartbeat activity is NOT a guaranteed exemption.
- If a project is already paused, restore it in Supabase before checking.
- This starter monitors the two named projects only. Adding another requires a workflow/check.py update and new secrets.

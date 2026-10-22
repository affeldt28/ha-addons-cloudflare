# Contributing

`cloudflared/` contains the Home Assistant manifest, Dockerfile, startup script, translations and user documentation. The image copies the official cloudflared binary into Alpine and uses Docker init with an exec-based entrypoint.

Run local checks:

```sh
sh -n cloudflared/rootfs/usr/local/bin/run-cloudflared
python3 -m unittest discover -s tools -p 'test_*.py'
docker build -t ha-cloudflared:test cloudflared
docker run --rm --entrypoint cloudflared ha-cloudflared:test --version
```

CI checks configuration/startup behavior and builds both supported architectures. Before releasing, test installation, tunnel connection, proxy configuration, restart and shutdown on Home Assistant OS. Never commit real tunnel tokens.

For releases, bump `cloudflared/config.json`, the Dockerfile's default `BUILD_VERSION`, and the changelog. Update the pinned upstream cloudflared image separately. Home Assistant detects updates from the manifest version when the repository refreshes.

## Automatic dependency releases

The hosted Renovate GitHub app checks dependencies according to its service schedule, using `.github/renovate.json`. It updates cloudflared and the Alpine `BUILD_FROM` image, groups runtime updates into one PR, and bumps the patch version in both `cloudflared/config.json` and the Dockerfile's `BUILD_VERSION`. Cloudflared's calendar-version major updates are included, so a new year does not stop updates.

Renovate merges the PR itself on a subsequent run only after status checks pass. `platformAutomerge: false` keeps the decision with Renovate; do not disable status checks in the configuration. CI tests startup and builds/runs the image for amd64 and aarch64. A failed check leaves the PR open. No GitHub Release or prebuilt published image is needed: Supervisor builds the add-on from this repository.

### One-time GitHub setup

1. Install or configure the [Renovate GitHub app](https://github.com/apps/renovate) and grant it access to this repository. No personal access token, `RENOVATE_TOKEN` secret or scheduled Renovate workflow is needed.
2. Enable Actions and squash merging in repository settings. If branch protection/rulesets apply, allow this bot to merge subject to the required checks, and account for any required human reviews. Recommended required checks are `validate`, `build (amd64)` and `build (aarch64)`. Keep those names in sync if jobs change. GitHub's separate “Allow auto-merge” setting is not needed because Renovate performs the merge itself.
3. Push `.github/renovate.json` to the default branch. The existing configuration on that branch onboards the repository; wait for the hosted app to process it and open update PRs.

See the [hosted app installation guide](https://docs.renovatebot.com/getting-started/installing-onboarding/) and [Renovate automerge documentation](https://docs.renovatebot.com/key-concepts/automerge/).

Once merged, Home Assistant detects the new add-on version during its repository refresh. Users can press **Update** in the add-on page, or enable the add-on's **Auto update** setting to install it automatically. **Start on boot** only starts the add-on; it does not enable updates. Use the store's **Check for updates** action to refresh manually. Source changes become available only after they are pushed/merged to the branch installed by users.

Automated dependency release notes are recorded in the Renovate PR and git history. Keep the changelog updated for manual feature/fix releases.

## Formatting and workflow conventions

Use the shared `.editorconfig`: tabs with width 4 by default, spaces with width 2 for YAML/Terraform, LF endings, a final newline and an 80-column target. Markdown has no line-length limit and preserves trailing spaces. Keep workflow and step names emoji-prefixed, following the other repositories. Every workflow step must have a descriptive name.

GitHub Actions use full commit SHAs with exact release comments (`uses: owner/action@<sha> # vX.Y.Z`). Renovate's GitHub Actions manager and `helpers:pinGitHubActionDigests` preset maintain both the pin and its version comment. Action-only updates do not bump the Home Assistant add-on version; Docker runtime updates do.

## Repository labels

`.github/labels.yml` contains the shared emoji labels from `home-ops`. The **🔄 Sync labels** workflow runs when that file or its workflow changes on `main`, and can also be run manually. It uses `GITHUB_TOKEN` with `issues: write`; no additional secret is needed. Like the shared workflow, `clean-labels: true` removes labels absent from the configuration, and aliases migrate the default names.

Renovate applies `dependencies 📦` to its PRs, plus `docker 🐳` for runtime images or `github-actions :octocat:` for action updates.

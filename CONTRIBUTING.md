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

For releases, bump `cloudflared/config.json` and the Dockerfile's default `BUILD_VERSION`. Update the pinned upstream cloudflared image separately. Home Assistant detects updates from the manifest version when the repository refreshes.

## Automatic dependency releases

The hosted Renovate GitHub app checks dependencies according to its service schedule, using `.github/renovate.json`. It updates cloudflared and the Alpine `BUILD_FROM` image, groups runtime updates into one PR, and bumps the patch version in both `cloudflared/config.json` and the Dockerfile's `BUILD_VERSION`. Cloudflared's calendar-version major updates are included, so a new year does not stop updates. Other major dependency upgrades require review.

Renovate merges the PR itself on a subsequent run only after status checks pass. `platformAutomerge: false` keeps the decision with Renovate; do not disable status checks in the configuration. CI tests startup and builds/runs the image on native amd64 and aarch64 runners, without QEMU or a separate Buildx setup. A failed check leaves the PR open. No GitHub Release or prebuilt published image is needed: Supervisor builds the add-on from this repository.

### One-time GitHub setup

1. Install or configure the [Renovate GitHub app](https://github.com/apps/renovate) and grant it access to this repository. No personal access token, `RENOVATE_TOKEN` secret or scheduled Renovate workflow is needed.
2. Enable Actions and squash merging in repository settings. If branch protection/rulesets apply, allow this bot to merge subject to the required checks, and account for any required human reviews. The pipeline calls reusable validation; configure required checks using the emitted CI check names for `validate`, `build (amd64)` and `build (aarch64)`. Keep those names in sync if jobs change. GitHub's separate “Allow auto-merge” setting is not needed because Renovate performs the merge itself.
3. Push `.github/renovate.json` to the default branch. The existing configuration on that branch onboards the repository; wait for the hosted app to process it and open update PRs.

See the [hosted app installation guide](https://docs.renovatebot.com/getting-started/installing-onboarding/) and [Renovate automerge documentation](https://docs.renovatebot.com/key-concepts/automerge/).

Once merged, Home Assistant detects the new add-on version during its repository refresh. Users can press **Update** in the add-on page, or enable the add-on's **Auto update** setting to install it automatically. **Start on boot** only starts the add-on; it does not enable updates. Use the store's **Check for updates** action to refresh manually. Source changes become available only after they are pushed/merged to the branch installed by users.

## Release pipeline and add-on changelog

The **🐙 Pipeline** runs validation and both architecture builds on pull requests and pushes to `main`. After successful CI on `main`, it reads `cloudflared/config.json`, creates a matching `major.minor.patch` tag when absent, and calls **📋 Release**. There is no separate publish job: Home Assistant builds this add-on from source.

The release workflow publishes GitHub-generated release notes for the version tag. It does not push commits back to `main`. Maintain `cloudflared/CHANGELOG.md` alongside manual packaging changes; Home Assistant displays that file. GitHub Releases provide the generated notes for automated dependency releases.

To retry a failed release, rerun the pipeline or manually dispatch **🐙 Pipeline** on `main`. Validation must pass before tagging and publishing. An existing tag is reused, a missing release is created, and an existing release is left intact. There is no separate manual Release entry point that could bypass validation. Grant the Actions token permission to create tags and releases; no personal token is required.

## Formatting and workflow conventions

Use the shared `.editorconfig`: tabs with width 4 by default, spaces with width 2 for YAML/Terraform, LF endings, a final newline and an 80-column target. Markdown has no line-length limit and preserves trailing spaces. Keep workflow and step names emoji-prefixed, following the other repositories. Every workflow step must have a descriptive name.

GitHub Actions use full commit SHAs with exact release comments (`uses: owner/action@<sha> # vX.Y.Z`). Renovate's GitHub Actions manager and `helpers:pinGitHubActionDigests` preset maintain both the pin and its version comment. Action-only updates do not bump the Home Assistant add-on version; Docker runtime updates do.

## Repository labels

`.github/labels.yml` contains the shared emoji labels from `home-ops`. The **🔄 Sync labels** workflow runs when that file or its workflow changes on `main`, and can also be run manually. It uses `GITHUB_TOKEN` with `issues: write`; no additional secret is needed. Like the shared workflow, `clean-labels: true` removes labels absent from the configuration, and aliases migrate the default names.

Renovate applies `dependencies 📦` to its PRs, plus `docker 🐳` for runtime images or `github-actions :octocat:` for action updates.

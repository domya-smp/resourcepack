# DomSMP resource pack

Custom item models and textures for DomSMP. The supported resource pack format is
defined in `pack.mcmeta`.

## Download

[Download the latest domsmp.zip](https://github.com/domya-smp/resourcepack/releases/latest/download/domsmp.zip)

A manual release from `main` publishes a GitHub Release containing:

- `domsmp.zip` — ready to install, with `pack.mcmeta` at the archive root.
- `domsmp.zip.sha1` — the raw SHA-1 hash for Minecraft server configuration.
- `domsmp.zip.sha256` — a checksum file for `sha256sum --check`.

The latest download link becomes available after the first successful publication
and updates automatically. Each release also retains a permanent URL for its build.
GitHub documents this URL format in [Linking to releases](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases).
This repository is private: release downloads require GitHub authentication and
access to the repository.

For a client, place `domsmp.zip` in the Minecraft `resourcepacks` directory
and enable it in the resource pack settings.

For server delivery, upload `domsmp.zip` to a download host reachable by Minecraft
clients without GitHub authentication. Use that URL in `server.properties`:

```properties
resource-pack=https://your-download-host.example/domsmp.zip
resource-pack-sha1=<contents of domsmp.zip.sha1 from the same release>
```

Update the SHA-1 whenever the pack changes. Keep the hosted ZIP and its SHA-1 from
the same release.

## Local build

Requires Python 3.10 or newer; no additional packages are needed.

```sh
python3 scripts/build.py
cd dist
sha256sum --check domsmp.zip.sha256
```

The build checks JSON syntax, includes only `pack.mcmeta`, `pack.png` and `assets/`,
and produces a ZIP with stable ordering, timestamps and permissions. Build output
in `dist/` is ignored by Git.

## CI

GitHub Actions validates and packages pushes to `main`, pull requests targeting
`main`, and manual runs. Build artifacts are retained for 30 days.

Pushes and pull requests only build the `domsmp` artifact. Release publication is
manual:

1. Open **Actions → Build and release domsmp**.
2. Click **Run workflow**, select the `main` branch, and confirm **Run workflow**.
3. Wait for the build and publication jobs to finish.

Only manual runs on `main` publish a release. Each release is named
`domsmp build-<run number>-<attempt>` and has the corresponding
`build-<run number>-<attempt>` tag. Publication uses the built-in `GITHUB_TOKEN`
with `contents: write`; no extra secrets are needed. The release is assembled as a
draft and becomes the latest release after its files have been uploaded.

# DomSMP resource pack

Custom item models and textures for DomSMP. The supported resource pack format is
defined in `pack.mcmeta`.

## Download

[Download the latest resourcepack.zip](https://github.com/domya-smp/resourcepack/releases/latest/download/resourcepack.zip)

Every successful build of `main` publishes a GitHub Release containing:

- `resourcepack.zip` — ready to install, with `pack.mcmeta` at the archive root.
- `resourcepack.zip.sha1` — the raw SHA-1 hash for Minecraft server configuration.
- `resourcepack.zip.sha256` — a checksum file for `sha256sum --check`.

The latest download link becomes available after the first successful publication
and updates automatically. Each release also retains a permanent URL for its build.
GitHub documents this URL format in [Linking to releases](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases).
Direct downloads without authentication require a public repository.

For a client, place `resourcepack.zip` in the Minecraft `resourcepacks` directory
and enable it in the resource pack settings.

For a server, set these entries in `server.properties`:

```properties
resource-pack=https://github.com/domya-smp/resourcepack/releases/latest/download/resourcepack.zip
resource-pack-sha1=<contents of resourcepack.zip.sha1 from the same release>
```

Update the SHA-1 whenever the pack changes. To keep a deployed server on one build,
use that release's download URL instead of the `latest` URL.

## Local build

Requires Python 3.10 or newer; no additional packages are needed.

```sh
python3 scripts/build.py
cd dist
sha256sum --check resourcepack.zip.sha256
```

The build checks JSON syntax, includes only `pack.mcmeta`, `pack.png` and `assets/`,
and produces a ZIP with stable ordering, timestamps and permissions. Build output
in `dist/` is ignored by Git.

## CI

GitHub Actions validates and packages pushes to `main`, pull requests targeting
`main`, and manual runs. Build artifacts are retained for 30 days.

Pushes and manual runs on `main` also publish a release tagged
`build-<run number>-<attempt>`. Pull requests only build the artifact. Publication
uses the built-in `GITHUB_TOKEN` with `contents: write`; no extra secrets are needed.
The release is assembled as a draft and becomes the latest release after its files
have been uploaded.

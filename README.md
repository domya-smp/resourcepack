# DomSMP resource pack

[Download domsmp.zip](https://github.com/domya-smp/resourcepack/releases/latest/download/domsmp.zip)
— requires access to this private repository.

## Build

```sh
python3 scripts/build.py
```

Requires Python 3.10+. Output: `dist/domsmp.zip`.

## Release

**Actions → Build and release domsmp → Run workflow**, branch `main`.
Pushes and pull requests only build the `domsmp` artifact.

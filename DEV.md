# Development Notes

Notes for maintaining this repository.

## Repository Structure

```
umsi-si639-labs/
├── labs/                    # All lab content lives here
│   ├── README.md            # Index of all labs (links here)
│   ├── browser_save_as/     # Each lab gets its own folder
│   │   └── README.md        # Lab instructions (template format)
│   ├── wget/
│   ├── archive_it/
│   └── ...
├── scratch/                 # Working/scratch space (contents are git ignored)
├── README.md                # Student-facing setup instructions
└── pyproject.toml           # Python dependencies (uv)
```

## Lab Format

Each lab follows the template in `labs/browser_save_as/README.md`:

1. `# Lab: <Lab Name>`
2. `## Overview`
3. `## Instructions` (with numbered steps like `**1-**`, `**2-**`)
4. `### Reflection Prompts`

## GitHub Pages

This repo uses GitHub Pages to publish the labs as a website.

- **Published URL**: https://ghukill.github.io/umsi-si639-labs/
- **Source branch**: `main`
- **Root**: `/` (publishes entire repo)

GitHub Pages renders markdown files automatically. The `labs/README.md` serves as the main index at `/labs/`.

### How it works

- Push to `main` triggers GitHub Pages build
- Markdown files are rendered to HTML
- Relative links between markdown files work (e.g., `[Lab: Wget](wget)`)
- No Jekyll configuration needed for basic markdown rendering

## Local Preview

Use Docker with the GitHub Pages gem to mirror Pages rendering locally.

1- Start the preview server:
```shell
cd serve
docker compose up
```

2- Open the site:
```
http://localhost:4000
```

Notes:
- The first run downloads Ruby gems and may take a minute.
- Use `Ctrl+C` to stop, then `docker compose down` to clean up.
- Local config lives in `serve/`, including `serve/_config.yml` and `serve/Gemfile`.

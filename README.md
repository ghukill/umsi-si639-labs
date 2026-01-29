# umsi-si639-labs

Repository for University of Michigan, School of Information, SI639 - Web Archiving labs.

## Installation

1- [Install uv](https://docs.astral.sh/uv/getting-started/installation/) for python environment management.

Check that `uv` is installed correctly:
```shell
uv --version

# should see something like
# uv 0.9.18 (0cee76417 2025-12-16)
```

2- Clone this repository: https://github.com/ghukill/umsi-si639-labs

3- Create python virtual environment:
```shell
uv venv .venv --python 3.12
```

4- Install dependencies:
```shell
uv sync
```

## GitHub Codespaces

_NOTE: Experimental! Thar be dragons._

GitHub Codespaces provides a browser-based Linux environment that can be used to run the labs in this repository without installing software locally. This can be especially helpful if you are unable (or prefer not) to install tools like Python, Docker, or other dependencies on your own machine.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ghukill/umsi-si639-labs)

### Instructions

If the Codespace button above doesn't work, try this...

1. Log in to your own GitHub account.

2. Navigate to the course repository: [https://github.com/ghukill/umsi-si639-labs](https://github.com/ghukill/umsi-si639-labs)

3. Click **Fork** (top-right) to create a copy of this repository under your own GitHub account.

4. After the fork is created, navigate to **your fork**  
   (the URL should look like `https://github.com/<your-github-username>/umsi-si639-labs`).

5. Click the green **Code** button, then select the **Codespaces** tab.

6. Click **Create codespace on main**.

7. Wait while the Codespace initializes (this may take a few minutes the first time).  
   When it finishes, you will be dropped into a browser-based VS Code environment with a Linux terminal.

8. Open a terminal (if one is not already open) and follow the lab instructions as usual.

### Notes and Tips

- Your Codespace is **persistent**: files you create will still be there the next time you open it.
- Stopping a Codespace does **not** delete it. You can safely stop it when you are done for the day.
- Avoid creating multiple Codespaces for the same repository unless you know why you are doing so.
- You can download files from the Codespace or commit and push your work back to your fork on GitHub.

If something goes wrong, you can always delete the Codespace and create a fresh one from your fork.

## Labs

Labs can be found at [/labs](labs).
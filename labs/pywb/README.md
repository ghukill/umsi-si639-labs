# Lab: pywb (record + replay)

----------------------------------------------------------------------------------------------------------------------------------------------------------------

## TODO

### General
- create collection

```shell
wb-manager init gmail-test
```
- really just creates a directory structure!

### Recording
- simple record 

```shell

```

- when recording, you get Resources (HTTP captures) but there is no sense of a seed
  - therefore in RPW, no links in URL
- wayback record help

```text
usage: wayback [-h] [-V] [-p PORT] [-b BIND] [-t THREADS] [--debug] [--profile] [--live] [--record] [--proxy PROXY] [-pt PROXY_DEFAULT_TIMESTAMP] [--proxy-record] [--proxy-enable-wombat] [--enable-auto-fetch] [-a]
               [--auto-interval AUTO_INTERVAL] [--all-coll ALL_COLL] [-d DIRECTORY]

pywb Wayback Machine Server

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -p PORT, --port PORT  Port to listen on (default 8080)
  -b BIND, --bind BIND  Address to listen on (default 0.0.0.0)
  -t THREADS, --threads THREADS
                        Number of threads to use (default 4)
  --debug               Enable debug mode
  --profile             Enable profile mode
  --live                Add live-web handler at /live
  --record              Enable recording from the live web
  --proxy PROXY         Enable HTTP/S proxy on specified collection
  -pt PROXY_DEFAULT_TIMESTAMP, --proxy-default-timestamp PROXY_DEFAULT_TIMESTAMP
                        Default timestamp / ISO date to use for proxy requests
  --proxy-record        Enable proxy recording into specified collection
  --proxy-enable-wombat
                        Enable partial wombat JS overrides support in proxy mode
  --enable-auto-fetch   Enable auto-fetch worker to capture resources from stylesheets, <img srcset> when running in live/recording mode
  -a, --autoindex       Enable auto-indexing
  --auto-interval AUTO_INTERVAL
                        Auto-indexing interval (default 30 seconds)
  --all-coll ALL_COLL   Set "all" collection
  -d DIRECTORY, --directory DIRECTORY
                        Specify root archive dir (default is current working directory)
```

### create a WACZ file from a collection

```shell
wacz create --output collections/recorder-1/recorder-1.wacz collections/recorder-1/archive/*.*
```
- contains

### REPLAY
- all you need is `wayback` and it'll serve collections
- prefix searching requires full `https://minternet.exe.xyz`

### The big reveal.... all wrapped up in archiveweb.page
- 

----------------------------------------------------------------------------------------------------------------------------------------------------------------

## Overview

This lab looks at the python library `pywb` ([Github](https://github.com/webrecorder/pywb), [documentation](https://pywb.readthedocs.io/en/latest/)),

> **pywb** is a Python 3 web archiving toolkit for replaying web archives large and small as accurately as possible. The toolkit now also includes new features for creating high-fidelity web archives.
> 
> This toolset forms the foundation of Webrecorder project, but also provides a generic web archiving toolkit that is used by other web archives, including the traditional "Wayback Machine" functionality.

The `pywb` python library has kind of a complex past, and potentially future.  Until the [1.0 release of Browsertrix-Crawler](https://github.com/webrecorder/browsertrix-crawler/releases/tag/v1.0.0), `pywb` was used for recording network traffic to WARC files.  Since the 1.0 release, Browsertrix-Crawler uses the Chrome Debug Protocol (CDP) to capture network requests and write WARC files directly. 

But `pywb` has long been a multi-purpose tool, and remains highly relevant.  In addition to "recording" network traffic and writing WARC files, `pywb` can also provide a Wayback instance to replay WARC and WACZ web archives.  As with most things web archiving, the Wayback machine _itself_ relies on another component in the `pywb` library called `warcserver`.  `warcserver` is an API interface all WARC files and CDX indexes in a collection.  This is used to power a Wayback machine for replay, but can also be used to build custom web archiving interfaces.

That's a lot of evolution and interconnectedness from a single library, and we've still not touched on all aspects of `pywb`!

This lab will attempt to show some core architecture choices and core functionality of `pywb`.  With the caveat the approach we use here may not be fully optimized, or represent production grade approaches, they _do_ mirror the patterns in larger services like Archive-It, Webrecorder service, and pre-packed / convenience applications like [ArchiveWeb.page](https://archiveweb.page/) and [ReplayWab.page](https://replayweb.page/) (which we've used extensively!), both of which are also from the Webrecorder ecosystem.

The `pywb` python library includes the following command line interface (CLI) tools when installed:
1. `wayback` - The full Wayback Machine application
2. `warcserver` - Standalone server component
3. `cdx-indexer` - Creates CDX/CDXJ indexes from WARCs
4. `wb-manager` - Collection management utility
5. `live-rewrite-server` - Demo live rewriting server 

Our approach here will be the following:

1. Create a virtual environment and install `pywb`
2. Use `wb-manager` CLI to create a new web archiving collection
3. Use `wayback` CLI with a `--record` flag to perform user-based, transactional capture
4. Replay or web archive via a `wayback` CLI Wayback instance
5. ...
6. ...
7. ...

## Instructions

###  1. Create a virtual environment and install `pywb`

If you have not already, clone the Github repository [https://github.com/ghukill/umsi-si639-labs](https://github.com/ghukill/umsi-si639-labs):
```shell
git clone https://github.com/ghukill/umsi-si639-labs
```

Move into the repository:
```shell
cd umsi-si639-labs
```

Create a python virtual environment with `uv`:
```shell
uv venv .venv --python 3.12
```

Install all dependencies:
```shell
uv sync
```

Confirm that `pywb` is installed:
```shell
pywb --version
# pywb 2.9.1
```

### 2. Use `wb-manager` CLI to create a new web archiving collection

First, move into the scratch folder:
```shell
cd scratch
```

Let's create a directory for this lab and move into it:
```shell
mkdir pywb-lab
cd pywb-lab
```

Now that we've got a good place to work, let's scaffold a new collection using `wb-manager`:
```shell
wb-manager init minternet 
```

This should create a file structure like the following:
```text
.
├── collections
│   └── minternet
│       ├── archive
│       ├── indexes
│       ├── static
│       └── templates
├── static
└── templates

9 directories, 0 files
```

At this point, we've really only created a directory structure that `pywb` understands and expects.  Please note that you _can_ override the defaults locations of all these bits and pieces, but for the sake of this lab we'll just use the defaults.

### 3. Use `wayback` CLI with a `--record` flag to perform user-based, transactional capture

Next, we'll capture some content using a web browser on our own machine in a human-driven, transactional approach.  Unlike crawlers we've looked in previous labs, e.g. `wget` and browsertrix-crawler, this approach to capturing content is not a "crawler" in the traditional sense!  The only content captured will be from a browser that we, as humans, control and navigate.  Only the pages we see and interact with will be included in the web archive.  Only actions we perform, i.e. clicking on buttons, will be recorded.  This style of capture results in very high fidelity captures, but obviously is a lot of manual work.  

Run the following command to `pywb` start a recording session, using our newly created collection:
```shell
wayback --record --live -a --auto-interval 10
```

To begin recording, navigate to the following URL in your browser: [http://localhost:8080/minternet/record/https://minternet.exe.xyz](http://localhost:8080/minternet/record/https://minternet.exe.xyz).  You should see the following in your browser:

![pywb-record.png](pywb-record.png)

While the majority of the browser tab looks normal, our now very familiar Minternet home page -- probably getting sick of it by now! -- displayed, note the pywb header at the top complete with its own URL bar.  This is a visual indication that we are "recording" each page this tab sees in our web archive.

At this point, feel free to click around the Minternet.  Some suggestions for activity to perform so we can see if it replays later:
- click into recipes, look at one recipe but not the other
- click into blogs, click around the calendar and search
- use the forward and back arrows in your browser as you normally would
- click into the science subdomain, click "View details" for _some_ experiments, but not all
- in the science subdomain, click on some of the asset downloads near the bottom like "Experiments Catalog" and "Laboratory Safety Guide"

Once satisfied with clicking around, feel free to close this tab, then go back to the terminal and stop the recording process we started with `ctrl + c` (on Mac, `cmd + c`).

With that done, we can run `tree` again and see the effects of our recording in the collections file structure:

```text
.
├── collections
│   └── minternet
│       ├── archive
│       │   └── rec-20260202012608556474-Grahams-MacBook-Pro.local.warc.gz
│       ├── indexes
│       │   └── autoindex.cdxj
│       ├── static
│       └── templates
├── static
└── templates

9 directories, 2 files
```

Note the new WARC file under the `archive/` folder, and the new index file under `indexes/`.  Success!  We have successfully performed a high fidelity, boutique web crawl, using the `pywb` CLI tool `wayback`!

### 4. Replay or web archive via a `wayback` CLI Wayback instance

TODO............


### Reflection Prompts

Coming soon...

# Lab: Browsertrix

## Overview

Browsertrix-Crawler ([Github](https://github.com/webrecorder/browsertrix-crawler), [documentation](https://crawler.docs.browsertrix.com/)) is a, 

> standalone browser-based high-fidelity crawling system, designed to run a complex, customizable browser-based crawl in a single Docker container. Browsertrix Crawler uses [Puppeteer](https://github.com/puppeteer/puppeteer) to control one or more [Brave Browser](https://brave.com/) browser windows in parallel. Data is captured through the [Chrome Devtools Protocol (CDP)](https://chromedevtools.github.io/devtools-protocol/) in the browser.

Browsertrix is a core component of the [Webrecorder web archiving platform](https://webrecorder.net/), but can be run as a standalone CLI application to perform web crawls and save the results as WARC files and/or a WACZ archive.  For this lab, we'll look at Browsetrix in this context.

Browsertrix is run as a Docker container allowing for strong cross-platform compatability.

## Instructions

### Install Docker and pull Browsertrix-Crawler image

First, ensure that Docker is installed on your machine:

- [Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Mac installation](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Linux installation](https://docs.docker.com/engine/install/)

Our goal is the ability to invoke a `docker ...` command from a terminal shell, which is how we'll invoke Browsertrix.  Once you think you have Docker installed, run the following command to confirm it's working:

```shell
docker --version

# example output:
# Docker version 29.1.3, build f52814d
```

With Docker installed, we can now pull the Docker image we'll use for future invocations:

```shell
docker pull webrecorder/browsertrix-crawler
```

This may take a few minutes depending on internet connection.  Once complete, run the following to confirm that we can invoke the Browsertrix Docker image:

```shell
docker run -it webrecorder/browsertrix-crawler:latest crawl --version

# example output:
# 1.11.1
```

Great!  Now we're ready to perform some web crawls.  The following link could be helpful to open in a new tab, containing all CLI arguments available for running crawls: [https://crawler.docs.browsertrix.com/user-guide/cli-options/](https://crawler.docs.browsertrix.com/user-guide/cli-options/).

### Run a small sample crawl without saving output

Our first task will be a small, test crawl to ensure the crawler is functioning as expected.  For this first crawl, we won't worry about saving any of the output.

Let's perform a crawl for a single URL with all default configurations:

```shell
docker run -it \
webrecorder/browsertrix-crawler:latest \
crawl \
--verbose \
--url https://minternet.exe.xyz/
```

If all went well, you should see some output like the following:

```text
{"timestamp":"2026-01-26T00:21:25.255Z","logLevel":"info","context":"general","message":"Browsertrix-Crawler 1.11.1 (with warcio.js 2.4.7)","details":{}}
{"timestamp":"2026-01-26T00:21:25.255Z","logLevel":"info","context":"general","message":"Seeds","details":[{"url":"https://minternet.exe.xyz/","scopeType":"prefix","include":["/^https?:\\/\\/minternet\\.exe\\.xyz\\//"],"exclude":[],"allowHash":false,"depth":-1,"sitemap":null,"auth":null,"_authEncoded":null,"maxExtraHops":0,"maxDepth":1000000}]}
{"timestamp":"2026-01-26T00:21:25.256Z","logLevel":"info","context":"general","message":"Link Selectors","details":[{"selector":"a[href]","extract":"href","isAttribute":false}]}
{"timestamp":"2026-01-26T00:21:25.256Z","logLevel":"info","context":"general","message":"Behavior Options","details":{"message":"{\"autoplay\":true,\"autofetch\":true,\"autoscroll\":true,\"siteSpecific\":true,\"log\":\"__bx_log\",\"startEarly\":true,\"clickSelector\":\"a\"}"}}
{"timestamp":"2026-01-26T00:21:25.573Z","logLevel":"info","context":"worker","message":"Creating 1 workers","details":{}}
{"timestamp":"2026-01-26T00:21:25.573Z","logLevel":"info","context":"worker","message":"Worker starting","details":{"workerid":0}}
{"timestamp":"2026-01-26T00:21:25.643Z","logLevel":"info","context":"worker","message":"Starting page","details":{"workerid":0,"page":"https://minternet.exe.xyz/"}}
{"timestamp":"2026-01-26T00:21:25.644Z","logLevel":"info","context":"crawlStatus","message":"Crawl statistics","details":{"crawled":0,"total":1,"pending":1,"failed":0,"limit":{"max":0,"hit":false},"pendingPages":["{\"seedId\":0,\"started\":\"2026-01-26T00:21:25.574Z\",\"extraHops\":0,\"url\":\"https:\\/\\/minternet.exe.xyz\\/\",\"added\":\"2026-01-26T00:21:25.276Z\",\"depth\":0}"]}}
{"timestamp":"2026-01-26T00:21:25.908Z","logLevel":"info","context":"general","message":"Awaiting page load","details":{"page":"https://minternet.exe.xyz/","workerid":0}}
{"timestamp":"2026-01-26T00:21:29.229Z","logLevel":"info","context":"pageStatus","message":"Page Finished","details":{"loadState":4,"page":"https://minternet.exe.xyz/","workerid":0}}
{"timestamp":"2026-01-26T00:21:29.235Z","logLevel":"info","context":"worker","message":"Worker done, all tasks complete","details":{"workerid":0}}
{"timestamp":"2026-01-26T00:21:29.300Z","logLevel":"info","context":"crawlStatus","message":"Crawl statistics","details":{"crawled":1,"total":1,"pending":0,"failed":0,"limit":{"max":0,"hit":false},"pendingPages":[]}}
{"timestamp":"2026-01-26T00:21:29.301Z","logLevel":"info","context":"general","message":"Crawling done","details":{}}
{"timestamp":"2026-01-26T00:21:29.302Z","logLevel":"info","context":"general","message":"Exiting, Crawl status: done","details":{}}
```

Let's look at a few log lines in particular to see what's happening.  Each log line is conveniently formatted as valid JSON.

```text
{"timestamp":"2026-01-26T00:21:25.255Z","logLevel":"info","context":"general","message":"Seeds","details":[{"url":"https://minternet.exe.xyz/","scopeType":"prefix","include":["/^https?:\\/\\/minternet\\.
```

This suggests that by passing the `--url` argument, we effectively started a crawl with a single seed:
```json
{
  "url":"https://minternet.exe.xyz/",
  "scopeType":"prefix",
  "include":["/^https?:\\/\\/minternet\\.exe\\.xyz\\//"],
  "exclude":[],
  "allowHash":false,
  "depth":-1,
  "sitemap":null,
  "auth":null,
  "_authEncoded":null,
  "maxExtraHops":0,
  "maxDepth":1000000
}
```

Hopefully some of these default configurations are looking a bit familiar by now!  We can see that both `include` and `exclude` scoping rules are applied.  We can see that the "scope type" for this seed is `prefix`, with other [scope types documented here](https://crawler.docs.browsertrix.com/user-guide/crawl-scope/#configuring-pages-included-or-excluded-from-a-crawl).  There are some other defaults like `depth:-1` and `maxDepth:1000000` that set some _very_ expansive limits on the extent of the crawl.  If not careful, we could pull in a lot of content!  Thankfully our URL prefix of `https://minternet.exe.xyz/` only has a single URL online to crawl.

There is lots of helpful content in the Browsertrix logs, but lets just jump down to one of the last ones.  This `content: crawlStatus` type logging line is _very_ helpful for keeping an eye on during crawls:

```json
{
  "timestamp":"2026-01-26T00:21:29.300Z",
  "logLevel":"info",
  "context":"crawlStatus",
  "message":"Crawl statistics",
  "details":{
    "crawled":1,
    "total":1,
    "pending":0,
    "failed":0,
    "limit":{
      "max":0,
      "hit":false
    },
    "pendingPages":[]
  }
}
```

This tells us that 1 URL was crawled, that we have a total of 1 URLs so far in this crawl (queued + crawled), and that zero are pending.  The logs reveal that the crawl ends immediateley after this status update, confirming this information is accurate.  

It's a bit of an art, with lots of different techniques, but monitoring the logging output for crawlers like this a very good idea.  If a crawl encounters a crawler trap, or is otherwise not scoped well, the `total` and `pending` numbers will start to increase quickly.

Because we did not [mount](https://docs.docker.com/engine/storage/bind-mounts/) a folder from our computer (the "host" machine in Docker terms) into the container, despite the crwal completeing successfully we do not have any persisting outputs once the crawl is complete and the container closes.  Our next task will be to _save_ some of the output after the container exits.

### Run single URL crawl and save output

First, ensure that you are working in a directory that you are familiar with and can find again.  At the end of this task, we'll have some files to inspect once the container has closed.

One option is to clone the SI639 labs Github repository and move into the `scratch` directory:

```shell
git clone https://github.com/ghukill/umsi-si639-labs

cd umsi-si639-labs

cd scratch

pwd
# example output
# /Users/gshukill/dev/teaching/umsi-si639-labs/scratch
```

To have the crawler write outputs to our "host" machine, thus persisting after the container closes, we'll need to run the countain with a mount.  Additionally, we'll set some flags for crawler to indicate what kind of output we want.

Run the following to perform the same crawl, but this time saving the output locally.  We will mount to a known folder in the container `/crawls` and request a WACZ file is written.

```shell
docker run -it \
-v $(PWD):/crawls \
webrecorder/browsertrix-crawler:latest \
crawl \
--verbose \
--collection minternet-crawl-1 \
--url https://minternet.exe.xyz/ \
--generateWACZ
```

Once the crawl completes, you should see a new folder called `collections`.  For context: inside the Browsertrix container the folder `/crawls/collections` was created.  We mounted the `/crawls` folder locally to our machine in the current directory, and thus we see this `collections` folder even _after_ the crawl has completed.  The structure of this folder should look roughly like the following:

```text
collections
└── minternet-crawl-1
    ├── archive
    │   └── rec-bbd22d6d0bca-minternet-crawl-1-20260126004356641-0.warc.gz
    ├── minternet-crawl-1.wacz
    ├── downloads
    ├── indexes
    │   └── index.cdxj
    ├── logs
    │   └── 20260126003755193.log
    ├── pages
    │   ├── extraPages.jsonl
    │   └── pages.jsonl
    ├── profile
    │   └── ... <---------- truncated output from profile/ directory
    └── warc-cdx
        └── rec-bbd22d6d0bca-minternet-crawl-1-20260126004356641-0.warc.gz.cdx

92 directories, 259 files
```

Browsertrix's data model uses a "collection" to encapsulate crawls.  Technically, we could run multiple crawls under the same collection, but we'll likely create a new collection for each crawl to keep things simple.

We used the flag `--collection minternet-crawl-1`, which results in a folder `collections/minternet-crawl-1` that contains _all_ output from the crawl in one place.  We'll look at some of the artifacts from the crawl in more detail.

#### `archive/`

This folder contains all the WARC files generated during the crawl.  Generally speaking, you have as many WARC files as you have workers, and they will "roll over" into a new file each time one of the hits 1gb.  For our crawl, a single worker with tiny data, we get one file.  But it would not be uncommon to have dozens, even hundreds of WARC files here.

#### `minternet-crawl-1.wacz`

This is the WACZ file we requested!  It's a bit circular, but this archive file is basically a zip of _all_ the files we're looking at now, but ecnapsulated in a single file.  We'll use this later to replay our crawl.

#### `indexes/`

This folder contains CDXJ index files generated from the crawl.  [CDXJ](https://specs.webrecorder.net/cdxj/0.1.0/) is a file format created by Webrecorder that dovetails with other tooling in the Webrecorder ecosystem.  We might think of it as an _extension_ of the [CDX](https://www.loc.gov/preservation/digital/formats/fdd/fdd000590.shtml) file format created by the Internet Archive for similar purposes.

One of the big differences is that each line contains valid JSON that can be parsed.  More on indexes later.

#### `logs/`

Logs from the crawl.  These can be incredibly valuable for understanding details about a crawl for QA and/or scoping.

#### `pages/`

This is convention somewhat unique to the Browsertrix / Webrecorder ecosystem, but a very handy one.  The file `pages.jsonl` is roughly equivalent to the seeds used.  Looking at our file, we see only a couple lines, with our `--url` Seed as the second line:

```json
{"format":"json-pages-1.0","id":"pages","title":"Seed Pages","hasText":"false"}
{"id":"eddd95e0-9485-4400-b776-9d7f27a6c61c","url":"https://minternet.exe.xyz/","title":"The Minternet","loadState":4,"ts":"2026-01-26T00:43:56.391Z","mime":"text/html","status":200,"seed":true,"depth":0}
```

In `extraPages.jsonl` we see only the first metadata line and nothing else:

```json
{"format":"json-pages-1.0","id":"pages","title":"Non-Seed Pages","hasText":"false"}
```

We'll see plenty more in this file in later crawls.

#### `profile/`

Let's skip this for now.  This is fairly advanced usage of Browsertrix that allows for creating a Browser -- think Google profile as an example -- that you can run the crawl as.

#### `warc-cdx/`

This directory contains CDX files generated from the crawl, where we'll see one file per WARC file generated.  More on indexes later.

Zooming out a bit, these outputs provide most if not all of what's needed to archive the content captured during the crawl!

To close the loop on this first, small, single URL crawl, let's see if we can replay it in the [ReplayWeb.page](https://replayweb.page/).  This is identical to what we did in the Week 2 lab for `wget`.

First, let's try loading the only WARC file we generated.  The full path of the WARC file can be found at `collections/minternet-crawl-1/archive/rec-bbd22d6d0bca-minternet-crawl-1-20260126004356641-0.warc.gz` relative to where the crawl was performed from.  If you open replayweb.page, you can click "Choose file" and load this WARC file.  Once loaded, you should see something similar:

![rwp-load-warc.png](rwp-load-warc.png)

And clicking on the first link of `https://minternet.exe.xyz/` we see our page rendered from the crawl we performed!

![rwp-warc-link-1.png](rwp-warc-link-1.png)

This was a pure HTML page, with zero complexity, but still confirms things are working as we hoped.

## Reflection Prompts

Coming soon...

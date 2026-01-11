# Lab: Browsertrix

## Overview

From the [Browsertrix-crawler](https://github.com/webrecorder/browsertrix-crawler) github page,

> Browsertrix Crawler is a standalone browser-based high-fidelity crawling system, designed to run a complex, customizable browser-based crawl in a single Docker container. Browsertrix Crawler uses Puppeteer to control one or more Brave Browser browser windows in parallel. Data is captured through the Chrome Devtools Protocol (CDP) in the browser.

Documentation for the browsertrix-crawler can be found here: https://crawler.docs.browsertrix.com/.

This is not to be confused with [browsertrix](https://github.com/webrecorder/browsertrix) which is a more fully featured application that supports the [Webrecorder](https://webrecorder.net/) service.

_TODO: More context / explanation of this tool._

## Instructions

Move into the `scratch` folder:
```shell
cd scratch
```

Pull browsertrix docker image
```shell
docker pull webrecorder/browsertrix-crawler:latest
```

Trigger the CLI help output, indicating the docker container is working correctly and give us a feel for some CLI options and ergonomics:
```shell
docker run webrecorder/browsertrix-crawler:latest crawl --help
```

Next, let's run a _very_ small crawl to confirm that crawling itself seems to work.  Note that we have _not_ mounted a folder from our host machine inside the docker container, so any outputs of the crawl will be lost when the crawl completes.  We are also limiting ourselves to 5 total URLs crawled. 
```shell
docker run webrecorder/browsertrix-crawler:latest \
crawl \
--collection wp-seattle \
--url https://en.wikipedia.org/wiki/Seattle \
--workers 2 \
--limit 5
```

Next, let's try mounting a folder into the Docker container so we can view the results of the crawl.  We'll also add a couple of extra CLI flags to the crawler to get more outputs:
```shell
docker run \
-v $(PWD)/crawls:/crawls \
webrecorder/browsertrix-crawler:latest \
crawl \
--collection wp-seattle \
--url https://en.wikipedia.org/wiki/Seattle \
--workers 2 \
--limit 5 \
--generateWACZ \
--generateCDX \
--text
```

### Reflection Prompts

Coming soon...

# Lab: pywb (record + replay)

## Overview

Archive-It provides a handful of APIs to work with collections programatically:

![ait-apis.png](ait-apis.png)

Today, we'll look at four of these APIs (covered in more detail below):

1. Partner API
2. Opensearch API
3. CDX API
4. Web Archiving Systems API (WASAPI)

Our goal will be to explore each one a little bit, get a feel for what kind of data it provides, and see how we can stitch them together.

At the end of this lab, you should have a teeny, tiny, super hacky discovery and access layer for any of your Archive-It collections!

### Partner API

From the [documentation](https://support.archive-it.org/hc/en-us/articles/360032747311-Access-your-account-with-the-Archive-It-Partner-API),

> The Archive-It Partner API provides access to information about Archive-It partners, collections, and crawls outside of your Archive-It account or pages on archive-it.org. Credentialed Archive-It users can query this data from Archive-It's database in a web browser or from the command line.
> 
> Partners can retrieve this information to develop custom access layers, manage administrative or descriptive metadata externally, or run periodic account usage reports.

### Opensearch API

From the [documentation](https://support.archive-it.org/hc/en-us/articles/208002246-Access-your-web-archives-with-OpenSearch),

> OpenSearch is a loosely structured standard that defines formats for the exchange of search results between search engines. The full draft specification is available at https://www.opensearch.org/Specifications/OpenSearch/1.1. For the rest of this guide, we'll focus on how to use OpenSearch as implemented by Archive-It.  See some real examples from our partners who are using OpenSearch: https://support.archive-it.org/hc/en-us/articles/360001231286-Archive-It-Access-Integrations
> 
> What you can do with OpenSearch:> 
> - ✅ Perform search queries with an RSS reader or your web browser
> - ✅ Perform search queries with a script, CGI, or other software
> - ✅ Programmatically manipulate results (for example, you can format results to match your own UI)
> 
> What you can't do with OpenSearch:
> - 🚫 Add or remove documents from the search engine
> - 🚫 Modify the content or meta data of a document  

### CDX API

From the [documentation](https://support.archive-it.org/hc/en-us/articles/115001790023-Access-Archive-It-s-Wayback-index-with-the-CDX-C-API),

> Archive-It’s Wayback CDX is the index of all archived content that the Wayback browsing interface uses to lookup and serve the specific captures requested by an end-user, such as from the Wayback calendar page. The index format is known as 'CDX' and contains various fields that describe each record, sorted by URL and date. The index's server responds to GET queries and returns the plain text CDX data. The CDX server is deployed as part of the wayback.archive-it.org Wayback browsing interface and was derived from the CDX server deployed for the general archive at web.archive.org, as part of the open-source Wayback Machine software: https://github.com/internetarchive/wayback.

### WARC Server API

From the [documentation](https://support.archive-it.org/hc/en-us/articles/360015225051-How-to-find-and-download-your-WARC-files-with-WASAPI),

> Partners can use Archive-It's implementation of the Web Archiving Systems API (WASAPI) from a web browser or a command line terminal to find and download their WARC files and associated technical metadata. The API supports several advanced options for partners to find and download these files by collection, date and timespans, and other attributes described below.

## Instructions

### Prepare Workspace

As per usual, ensure that you have the SI639 labs GitHub repository cloned and updated:

```shell
git clone https://github.com/ghukill/umsi-si639-labs
cd umsi-si639-labs
git pull origin main
```

Run command to update dependencies:
```shell
uv sync
```

We're all set!  We'll run any code from the **root** of the project.

### Use Partner API via a Browser

First, login into the partner site at [https://partner.archive-it.org/](https://partner.archive-it.org/).

Once logged in, any API URL routes that we visit in our browser will show us the results for an authenticated user.

Let's navigate to the API root which shows us a list of API routes we can use: [https://partner.archive-it.org/api/](https://partner.archive-it.org/api/).

You should see something that looks like this:

![api-root.png](api-root.png)

This is an **HTML** representation of the API response, formatted nicely for our human eyes.  As we'll see later, _most_ of the time we make a request to the API and get back a JSON response.  So as we look at these responses in the browser, just keep in mind that from a programmatic context we'd be interacting with just JSON.

Conveniently, the links in this HTML API response are clickable.  Try clicking on the first link [https://partner.archive-it.org/api/account](https://partner.archive-it.org/api/account).  This brings back some information about our shared Archive-It account.  Neat!  One can imagine how this could be used to build a custom interface... but more on that later.

Next, and more aligned with goals of this lab, let's look at the `/collection` endpoint, [https://partner.archive-it.org/api/collection](https://partner.archive-it.org/api/collection).  At the time of this writing, the first page has 100 results, a second page 75 results, for a total of 175 collections.  It's pretty hacky, but try ctrl + f searching for a string you'd expect, like a collection you know exists.

For example, I looked for `gshukill` and found this collection on page 2:

```json
{
  "account": 421,
  "created_by": "gshukill",
  "created_date": "2026-01-17T00:23:39.656223Z",
  "custom_user_agent": null,
  "deleted": false,
  "id": 30935,
  "image": null,
  "last_crawl_date": "2026-01-22T05:34:51.071714Z",
  "last_updated_by": "gshukill",
  "last_updated_date": "2026-01-21T01:05:11.070555Z",
  "metadata": {
    "Identifier": [
      {
        "id": 17379727,
        "value": "gshukill-si639-collection-1"
      }
    ],
    "Date": [
      {
        "id": 17379728,
        "value": "2026-01-20"
      }
    ],
    "Creator": [
      {
        "id": 17379729,
        "value": "Graham Hukill"
      },
      {
        "id": 17379730,
        "value": "University of Michigan, School of Information, SI639"
      }
    ],
    "Title": [
      {
        "id": 17379731,
        "value": "Graham's SI639 Collection"
      }
    ],
    "minternet_domain": [
      {
        "id": 17379732,
        "value": "recipes"
      }
    ]
  },
  "name": "gshukill-si639-w26-week3-lab",
  "num_active_seeds": 1,
  "num_inactive_seeds": 0,
  "oai_exported": false,
  "private_access_token": "xxxxxxxxx",   <------- removed
  "publicly_visible": false,
  "state": "ACTIVE",
  "topics": null,
  "total_warc_bytes": 332017
}
```

In addition to metadata, one important thing from that response is the collection identifier `"id": 30935`.

Most of the AIT partner API routes can be filtered by keys that are in the response for that route.  Some filtering examples:

- a specific collection: [https://partner.archive-it.org/api/collection?id=30935](https://partner.archive-it.org/api/collection?id=30935)
- filter by creator: https://partner.archive-it.org/api/collection?created_by=gshukill

Let's use this collection and find seeds associated with it by using the `/seed` endpoint: [https://partner.archive-it.org/api/seed?collection=30935](https://partner.archive-it.org/api/seed?collection=30935)

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4602918,
      "created_by": "gshukill",
      "created_date": "2026-01-22T00:53:55.484540Z",
      "last_updated_by": "gshukill",
      "publicly_visible": false,
      "http_response_code": null,
      "last_checked_http_response_code": null,
      "active": true,
      "collection": 30935,
      "valid": null,
      "seed_type": "oneHopOff",
      "deleted": false,
      "last_updated_date": "2026-02-01T20:08:56.921002Z",
      "url": "https://minternet.exe.xyz/",
      "canonical_url": "https://minternet.exe.xyz/",
      "login_username": null,
      "login_password": null,
      "metadata": {
        "Title": [
          {
            "id": 17404882,
            "value": "The Minternet"
          }
        ],
        "Creator": [
          {
            "id": 17404883,
            "value": "Graham Hukill"
          }
        ],
        "Description": [
          {
            "id": 17404884,
            "value": "Root of web archiving test suites"
          }
        ]
      },
      "seed_groups": []
    }
  ]
}
```

We can also see all crawls for a given collection, [https://partner.archive-it.org/api/crawl_job?collection=30935](https://partner.archive-it.org/api/crawl_job?collection=30935):

```json
{
  "count": 7,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2654714,
      "type": "CRAWL_SELECTED_SEEDS",
      "brozzler": false,
      "original_start_date": "2026-01-17T14:15:23.469479Z",
      "end_date": "2026-01-17T14:16:08.436149Z",
      "test_crawl_save_date": null,
      "test_crawl_state": null,
      "elapsed_ms": 22607,
      "downloaded_count": 22,
      "total_data_in_kbs": 31,
      "novel_count": 15,
      "novel_bytes": 23414,
      "duplicate_count": 7,
      "duplicate_bytes": 8723,
      "warc_url_count": 20,
      "warc_content_bytes": 23416,
      "status": "FINISHED",
      "doc_rate": "0.97",
      "account": 421,
      "collection": 30935,
      "crawl_definition": 37325789982,
      "test_crawl_state_changed_by": null
    },
    {
      "id": 2656024,
      "type": "CRAWL_SELECTED_SEEDS",
      "brozzler": false,
      "original_start_date": "2026-01-21T00:51:19.561940Z",
      "end_date": "2026-01-21T00:55:13.935980Z",
      "test_crawl_save_date": null,
      "test_crawl_state": null,
      "elapsed_ms": 214733,
      "downloaded_count": 19,
      "total_data_in_kbs": 26,
      "novel_count": 7,
      "novel_bytes": 8006,
      "duplicate_count": 12,
      "duplicate_bytes": 18856,
      "warc_url_count": 17,
      "warc_content_bytes": 8008,
      "status": "FINISHED",
      "doc_rate": "0.09",
      "account": 421,
      "collection": 30935,
      "crawl_definition": 37325790587,
      "test_crawl_state_changed_by": null
    },
    {
      "id": 2656563,
      "type": "TEST_EXPIRED",
      "brozzler": false,
      "original_start_date": "2026-01-22T01:01:12.741230Z",
      "end_date": "2026-01-22T01:02:46.687552Z",
      "test_crawl_save_date": null,
      "test_crawl_state": "EXPIRED",
      "elapsed_ms": 77446,
      "downloaded_count": 48,
      "total_data_in_kbs": 475,
      "novel_count": 38,
      "novel_bytes": 482869,
      "duplicate_count": 10,
      "duplicate_bytes": 3738,
      "warc_url_count": 42,
      "warc_content_bytes": 482875,
      "status": "FINISHED",
      "doc_rate": "0.62",
      "account": 421,
      "collection": 30935,
      "crawl_definition": 37325790869,
      "test_crawl_state_changed_by": null
    },
    {
      "id": 2656566,
      "type": "TEST_EXPIRED",
      "brozzler": false,
      "original_start_date": "2026-01-22T01:17:18.852848Z",
      "end_date": "2026-01-22T01:19:45.554571Z",
      "test_crawl_save_date": null,
      "test_crawl_state": "EXPIRED",
      "elapsed_ms": 142400,
      "downloaded_count": 101,
      "total_data_in_kbs": 682,
      "novel_count": 88,
      "novel_bytes": 693648,
      "duplicate_count": 13,
      "duplicate_bytes": 4848,
      "warc_url_count": 95,
      "warc_content_bytes": 693654,
      "status": "FINISHED_DOCUMENT_LIMIT",
      "doc_rate": "0.71",
      "account": 421,
      "collection": 30935,
      "crawl_definition": 37325790870,
      "test_crawl_state_changed_by": null
    },
    {
      "id": 2656573,
      "type": "TEST_EXPIRED",
      "brozzler": false,
      "original_start_date": "2026-01-22T02:14:26.080621Z",
      "end_date": "2026-01-22T02:19:16.187737Z",
      "test_crawl_save_date": null,
      "test_crawl_state": "EXPIRED",
      "elapsed_ms": 267014,
      "downloaded_count": 308,
      "total_data_in_kbs": 1070,
      "novel_count": 295,
      "novel_bytes": 1090854,
      "duplicate_count": 13,
      "duplicate_bytes": 4848,
      "warc_url_count": 302,
      "warc_content_bytes": 1090860,
      "status": "FINISHED_ABORTED",
      "doc_rate": "1.15",
      "account": 421,
      "collection": 30935,
      "crawl_definition": 37325790871,
      "test_crawl_state_changed_by": null
    },
    {
      "id": 2656574,
      "type": "TEST_EXPIRED",
      "brozzler": false,
      "original_start_date": "2026-01-22T02:24:33.746895Z",
      "end_date": "2026-01-22T02:25:57.738364Z",
      "test_crawl_save_date": null,
      "test_crawl_state": "EXPIRED",
      "elapsed_ms": 66413,
      "downloaded_count": 83,
      "total_data_in_kbs": 579,
      "novel_count": 70,
      "novel_bytes": 588648,
      "duplicate_count": 13,
      "duplicate_bytes": 4848,
      "warc_url_count": 77,
      "warc_content_bytes": 588654,
      "status": "FINISHED",
      "doc_rate": "1.25",
      "account": 421,
      "collection": 30935,
      "crawl_definition": 37325790872,
      "test_crawl_state_changed_by": null
    },
    {
      "id": 2656578,
      "type": "CRAWL_SELECTED_SEEDS",
      "brozzler": false,
      "original_start_date": "2026-01-22T03:00:24.081819Z",
      "end_date": "2026-01-22T03:02:49.915230Z",
      "test_crawl_save_date": null,
      "test_crawl_state": null,
      "elapsed_ms": 127602,
      "downloaded_count": 83,
      "total_data_in_kbs": 579,
      "novel_count": 70,
      "novel_bytes": 588647,
      "duplicate_count": 13,
      "duplicate_bytes": 4848,
      "warc_url_count": 77,
      "warc_content_bytes": 588653,
      "status": "FINISHED",
      "doc_rate": "0.65",
      "account": 421,
      "collection": 30935,
      "crawl_definition": 37325790880,
      "test_crawl_state_changed_by": null
    }
  ]
}
```

Note that in each of these, the `id` field is the identifier of _that_ crawl.  We can use that to get more details about a specific crawl, [https://partner.archive-it.org/api/crawl_job_run?crawl_job=2654714](https://partner.archive-it.org/api/crawl_job_run?crawl_job=2654714):

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1948962,
      "start_date": "2026-01-17T14:15:27.918171Z",
      "end_date": "2026-01-17T14:16:08.436149Z",
      "processing_end_date": "2026-01-17T14:23:41.490287Z",
      "host": "wbgrp-crawl029",
      "crawl_stop_requested": "2026-01-17T14:15:48.123416Z",
      "downloaded_count": 22,
      "total_data_in_kbs": 31,
      "novel_count": 15,
      "novel_bytes": 23414,
      "duplicate_count": 7,
      "duplicate_bytes": 8723,
      "warc_url_count": 20,
      "warc_content_bytes": 23416,
      "status": "FINISHED",
      "port": 6440,
      "postcrawl_step": 100,
      "resumption_count": 0,
      "doc_rate": "0.97",
      "crawl_job": 2654714,
      "account": 421,
      "collection": 30935,
      "scheduled_crawl_event": 2861415,
      "crawl_queue": 3
    }
  ]
}
```

There is obviously _much_ more to the Partner API, but this is the general pattern:

- use routes and extract identifiers
- use other routes and apply those collection, crawl, etc., identifiers to further refine

With this API alone, you could do quite a bit!  Here is one more example showing a hosts report for a given crawl [https://partner.archive-it.org/api/reports/host/2654714](https://partner.archive-it.org/api/reports/host/2654714),

```json
[
  {
    "id": 2,
    "host": "minternet-recipes.exe.xyz",
    "all_count": 13,
    "all_size": 22884,
    "new_count": 7,
    "new_size": 14652,
    "warc_all_count": 13,
    "warc_new_count": 7,
    "warc_all_content_bytes": 15780,
    "warc_new_content_bytes": 14652,
    "blocked": 0,
    "queued": 0,
    "out_of_scope": 0
  },
  {
    "id": 3,
    "host": "whois:",
    "all_count": 5,
    "all_size": 7869,
    "new_count": 5,
    "new_size": 7869,
    "warc_all_count": 3,
    "warc_new_count": 3,
    "warc_all_content_bytes": 7871,
    "warc_new_content_bytes": 7871,
    "blocked": 0,
    "queued": 0,
    "out_of_scope": 0
  },
  {
    "id": 4,
    "host": "www.w3.org",
    "all_count": 2,
    "all_size": 1247,
    "new_count": 1,
    "new_size": 756,
    "warc_all_count": 2,
    "warc_new_count": 1,
    "warc_all_content_bytes": 1080,
    "warc_new_content_bytes": 756,
    "blocked": 0,
    "queued": 0,
    "out_of_scope": 0
  },
  {
    "id": 1,
    "host": "dns:",
    "all_count": 2,
    "all_size": 137,
    "new_count": 2,
    "new_size": 137,
    "warc_all_count": 2,
    "warc_new_count": 2,
    "warc_all_content_bytes": 137,
    "warc_new_content_bytes": 137,
    "blocked": 0,
    "queued": 0,
    "out_of_scope": 0
  }
]
```

Neat!  It's the raw data that the front-end uses to generate host report graphs and tables.  

Now, let's move into using python + HTTP requests to use this API in the way it was designed to be used.

### Use Partner API via python + HTTP requests

#### Starting Ipython shell with username + password environment variables

For the next few parts of the lab we'll be working from an Ipython shell and copy/pasting code to execute.

To make authenticated API requests we'll need to pass our username + password that we use to login into the partner site.  To do this from python, we'll set **environment variables** that we can then use from python.

Run the following to start an ipython shell, replacing `xxxx` and `yyyy` with your actual username + password:

```shell
AIT_USERNAME=xxxx AIT_PASSWORD=yyyy uv run ipython
```

**NOTE:** in a real production environment, you might create a `.env` file and store your credentials there, e.g.:

```shell
AIT_USERNAME=xxxx
AIT_PASSWORD=yyyy
```

And then start ipython and load that `.env` file:
```shell
uv run --env-file .env ipython
```

Both appraoches work!


Let's confirm our environment variables are set:

```python
import os

print(os.getenv("AIT_USERNAME"))
# gshukill
```

If that doesn't work, stop now!  All future work will assume these environment variables are set.

#### Make API requests with `requests` library

To demonstrate to ourselves how this works, let's do a simple API request with the `requests` library:

```python
import os
import requests

requests.get(
    "https://partner.archive-it.org/api/account",
    auth=(
        os.environ["AIT_USERNAME"],
        os.environ["AIT_PASSWORD"],
    )
).json()
```

Note that we are authenticating directly in the request.  A better approach would be to create a session, and then reuse that for all future requests:

```python
# create session
session = requests.Session()
session.auth = (
    os.environ["AIT_USERNAME"],
    os.environ["AIT_PASSWORD"],
)

# use session for requests
session.get("https://partner.archive-it.org/api/account").json()

# and another request using that same session
session.get("https://partner.archive-it.org/api/seed?collection=30935").json()
```

Noice!  So we've confirmed the Partner API works both in the browser and via python HTTP requests.  Let's move on to looking at the other APIs, and then we'll look at tying it all together.

### Use Opensearch API

The Opensearch API allows for full-text searching of our collections.

Let's first perform a request in the browser to get a quick feel for the response: [https://archive-it.org/search-master/opensearch?i=30935&q=alice](https://archive-it.org/search-master/opensearch?i=30935&q=alice).

Gasp, XML!  

Let's break down the URL pattern a bit:
- API base URL: `https://archive-it.org/search-master/opensearch?i=30935&q=alice](https://archive-it.org/search-master/opensearch`
- collection id: `?i=30935`
- search term "alice": `q=alice`

If we format that XML nicely, it looks like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>alice</title>
        <description>alice</description>
        <link/>
        <startIndex xmlns="http://a9.com/-/spec/opensearchrss/1.0/">0</startIndex>
        <itemsPerPage xmlns="http://a9.com/-/spec/opensearchrss/1.0/">1</itemsPerPage>
        <query xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">alice</query>
        <index xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">30935</index>
        <urlParams xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">
            <param name="i" value="30935"/>
            <param name="q" value="alice"/>
            <param name="n" value="10"/>
            <param name="p" value="0"/>
        </urlParams>
        <item>
            <title>Alice Chen - minternet-blogs.exe.xyz</title>
            <link>https://minternet-blogs.exe.xyz/author/alice</link>
            <docId xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">
                30935sha1:QH3IOM6XWXINOTGRTXTPV2RQ57IVOS46https://minternet-blogs.exe.xyz/author/alice
            </docId>
            <score xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">74.577446
            </score>
            <site xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">
                minternet-blogs.exe.xyz
            </site>
            <length xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">2740</length>
            <type xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">text/html
            </type>
            <boost xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">1.0</boost>
            <collection xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">30935
            </collection>
            <index xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">30935</index>
            <date>20260122030104</date>
            <description>&lt;b&gt;Alice&lt;/b&gt; Chen - minternet-blogs.exe.xyz Archive
                Blog Exploring web preservation, one trap at a time Home Calendar Search
                &lt;b&gt;Alice&lt;/b&gt; Bob Charlie &lt;b&gt;Alice&lt;/b&gt; Chen Digital
                preservation specialist with 10 years of experience
            </description>
        </item>
        <totalResults xmlns="http://a9.com/-/spec/opensearchrss/1.0/">1</totalResults>
        <responseTime xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">0.369
        </responseTime>
    </channel>
</rss>
```

We can see that each "result" is represented by a `<item>` element.  In this case, we only had one match.  

It's not obvious from this example with "alice" being in both the title and the URL, but this API _is_ searching the full-text of the crawled content!  This is the major advantage.  Let's try another result from a public collection, [https://archive-it.org/search-master/opensearch?i=2950&q=seattle](https://archive-it.org/search-master/opensearch?i=2950&q=seattle).

This is searching the public collection ["Occupy Movement 2011/2012"](https://archive-it.org/collections/2950).  Note that this works because the Opensearch endpoint does NOT require authentication for public collections.

That response contains quite a few more results -- it's a large collection! -- with a result like this showing that the search term "Seattle" brought back a record where it's not part of the title, URL, or explicit metadata:

```xml
<item>
    <title>West Coast Ports Shutdown « occupy california</title>
    <link>
        http://occupyca.wordpress.com/2011/12/12/west-coast-ports-shutdown/?like=1
    </link>
    <docId xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">
        2950sha1:22TZJ5NVOLWTXMAJ7QSEWGGMQIESNON2http://occupyca.wordpress.com/2011/12/12/west-coast-ports-shutdown/?like=1
    </docId>
    <score xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">56.488823
    </score>
    <site xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">
        occupyca.wordpress.com
    </site>
    <length xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">45819
    </length>
    <type xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">
        application/xhtml+xml
    </type>
    <boost xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">1.3698448
    </boost>
    <collection xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">2950
    </collection>
    <index xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">2950</index>
    <date>20120117014149</date>
    <description>&lt;b&gt;SEATTLE&lt;/b&gt; , Washington — Hundreds gathered in
        Westlake Park around 1:30pm. As of 2:30pm, they’ve begun to march to the
        Port of &lt;b&gt;Seattle&lt;/b&gt; . By around 3:15pm, a growing crowd has
        reached the port.
    </description>
</item>
```

The keen eye may notice that "Seattle" is in the `<description>` element.  Where does that come from?  My guess -- and this is somewhat unsubstantiated -- is that that field is derived automatically via full-text from the captured URL.  You'll notice that some `<description>` elements are wonky or look incomplete, reflecting a potentially poorly crawled website.

There are three super key elements from each `<item>` that we can use for other purposes:

- `<link>`: the actual URL crawled
- `<collection xmlns="http://web.archive.org/-/spec/opensearchrss/1.0/">`: the AIT collection identifier
- `<date>`: date of capture

What can we do with these?  Buckle up.... we can generate a URL that will produce a Wayback Machine instance already configured for _this_ website, from _this_ collection, crawled on _that_ date.

The pattern: `https://wayback.archive-it.org/{collection_id}/{date}/{link}`

Example: [https://wayback.archive-it.org/2950/20120117014149/http://occupyca.wordpress.com/2011/12/12/west-coast-ports-shutdown/?like=1](https://wayback.archive-it.org/2950/20120117014149/http://occupyca.wordpress.com/2011/12/12/west-coast-ports-shutdown/?like=1)

So what are our takeaways from this API at this point?

- supports full-text searching collections
- results contain enough information to drill in via the Partner API
- results contain enough information to render a Wayback Machine instance for that capture

Neat!

## Reflection Prompts

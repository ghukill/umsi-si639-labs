# Lab: bag-nabit

## Overview

`bag-nabit` is a tool built by the Harvard Library Innovation Laboratory ([website](https://lil.law.harvard.edu/), [GitHub](https://github.com/harvard-lil)).  A [blog post from inkdroid.org](https://inkdroid.org/2025/02/17/nabit/) sums up the functionality nicely,

> 1. downloads all the URLs to disk
> 2. writes the dataset metadata to disk 
> 3. packages up the data and metadata into a BagIt directory (RFC 8493) 
> 4. records provenance about who did the work and when they did it 

What does this mean exactly?  And why is it useful?

Let's imagine the following scenario.

You are interested in downloading a text file from the Internet, a `.txt` file of the 1910 book "A Nonsense Anthology" from the Project Gutenberg website.  Let's assume that we want to preserve this file in such a way that other, future researchers can be sure the file was retrieved directly from a given URL, on a specific date, and was not modified during or after retrieval.  

This may seem like a simple task:

1. download the file
2. prepare some kind of preservation package
3. include metadata about when we downloaded it, who did, how we did it, etc., etc.
4. include the text file we just downloaded

Seems simple, right?  But what is stopping us -- nefariously or accidentally -- from:

1. modifying the text file
2. claiming it came from URL `https://foo.com/book.txt` but it actually came from `https://bar.net/other-book.txt`
3. claiming it was `2020-01-01`, but was actually today `2026-03-17`
4. and so forth...

Not much!  Depending on how we package it, metadata and data file metadata like created and modified dates, there is virtually nothing in our handmade preservation package that tethers it to what actually occurred and how the package was made.

Enter `bag-nabit`!  As stated above, the purpose of this utility is to safeguard against the risks named above, and many more.  By using this tool to create a preservation object, we get the following:

1. confirmation that the file was retrieved directly from URL `https://foo.com/book.txt`
2. the data is checksummed during download and checksummed again when added to our preservation package
3. a WARC file is created that captures all network requests
4. optionally, signatures are added for who and when the operations took place that are very difficult to modify or forge
5. a self-contained preservation object in the form of a [BagIt](https://datatracker.ietf.org/doc/html/rfc8493) bag 
6. utilities for _verifying_ all these things after the fact

This is a bit of a niche tool, but one can imagine how important a role this could play in establishing the provenance of digital objects downloaded from the Internet.

Is this.... "web archiving"?  It depends on your definition!  The end goal is not a digital object that can support a replay experience of an internet browser -- what we often think of re: web archiving -- but we are certainly preserving data / information from the web, and encoding enough information about the network interactions to replay the _authenticity_ of the data retrieved.  

Let's take it for a spin and see what other similarities or differences emerge.

## Instructions

### Install Dependencies

If not using the `umsi-si639-labs` GitHub Codespace -- [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ghukill/umsi-si639-labs) -- make sure that `bag-nabit` is installed.  If you _are_ using GitHub Codespaces, you can skip to the "Create Workspace" section.

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

Lastly, make sure to activate your `uv` python virtual environment!
```shell
source .venv/bin/activate
```

### Create and Confirm Workspace

Ensure that `nabit` is installed:

```shell
nabit --help
# should see help output here...
```

Create a workspace folder and move into it:

```shell
mkdir -p scratch/bag-nabit
cd scratch/bag-nabit
```

We're all set!

### Creating our first bag

To get things started, we'll use `nabit` to create a single bag for two files located online.

Find two files you'd like to include in your bag, ideally simple, single files like a PDF or an image file.  If you're not feeling creative, feel free to use the following two URLs:

- A JPEG image from the 2000 AFSCME Convention: [https://wayne.contentdm.oclc.org/digital/download/collection/afscme/id/163/size/large](https://wayne.contentdm.oclc.org/digital/download/collection/afscme/id/163/size/large)
- A text file of the 1910 book "A Nonsense Anthology": [https://www.gutenberg.org/cache/epub/9380/pg9380.txt](https://www.gutenberg.org/cache/epub/9380/pg9380.txt)

Let's create the bag:

```shell
nabit archive \
test-bag-1 \
-u https://wayne.contentdm.oclc.org/digital/download/collection/afscme/id/163/size/large \
-u https://www.gutenberg.org/cache/epub/9380/pg9380.txt
```

NOTE: You may see a warning like the following: 
```text
..../.venv/lib/python3.12/site-packages/nabit/lib/sign.py:7: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
```

This can be ignored, but it's not a _great_ sign that the library is a bit behind in dependency management 😅.


You should see some output like the following:

```text
Creating package at test-bag-1 ...
Validating package at test-bag-1 ...
SUCCESS: headers.warc found
SUCCESS: bag format is valid
WARNING: No signatures found
WARNING: No timestamps found
Package is valid
Package created at test-bag-1
```

Which created the following directory structure:

```text
test-bag-1
├── bag-info.txt
├── bagit.txt
├── data
│   ├── files
│   │   ├── large.jpg
│   │   └── pg9380.txt
│   ├── headers.warc
│   └── signed-metadata.json
├── manifest-sha256.txt
└── tagmanifest-sha256.txt
```

Congratulations! 🎉  You have retrieved a couple of random files from the internet and packaged them up as a preservation-ready object!  So what are these files?  Let's look at them one by one.

```text
test-bag-1/
```

This directory is created and we might think of this as the bag itself.  It's the wrapper that holds the whole thing together.  It's worth noting -- and we'll touch on this later -- that you could zip up this directory and be confident you have all the files you need.


```text
├── data
│   ├── files
│   │   ├── large.jpg
│   │   └── pg9380.txt
```

These are the two files that were downloaded based on the URLs we provided.  It's worth noting that the filenames are fully dependent on the filename the URL resolves to.

```text
├── data
...
│   ├── headers.warc
```

A WARC file!  This is worth looking at in more detail:

```text
WARC/1.0
WARC-IP-Address: 132.174.3.1
WARC-Type: revisit
WARC-Record-ID: <urn:uuid:f3e4812d-eed5-4a5a-81d5-ed5a8b1663b1>
WARC-Target-URI: https://wayne.contentdm.oclc.org/digital/download/collection/afscme/id/163/size/large
WARC-Date: 2026-03-18T20:39:21Z
WARC-Payload-Digest: sha1:7AFLTDVQ7RVCOL4QYRSVQ2KAZ4DVVSVK
WARC-Profile: file-content; filename="files/large.jpg"
WARC-Block-Digest: sha1:USPSJJX3T3AYMFRQUOT7L2BDXJ3BONPA
Content-Type: application/http; msgtype=response
Content-Length: 785

HTTP/1.1 200 OK
Date: Wed, 18 Mar 2026 20:39:20 GMT
Server: Apache
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
X-OCLC-IIIF-Provider: cantaloupe
Vary: Accept-Encoding,Origin,Access-Control-Request-Method,Access-Control-Request-Headers
Content-Type: image/jpeg
Content-Disposition: attachment; filename="afscme_163_large.jpg"
Content-Description: File Transfer
Content-Transfer-Encoding: binary
Expires: 0
Cache-Control: must-revalidate, post-check=0, pre-check=0
Pragma: public
X-Content-Type-Options: nosniff
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN
Set-Cookie: JSESSIONID=Y2QzZGIxZmQtZWM0Mi00MTAwLThmZjEtMGJiOTRiMDU5Njlk; Path=/; HttpOnly; SameSite=Lax
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked



WARC/1.0
WARC-IP-Address: 132.174.3.1
WARC-Type: request
WARC-Record-ID: <urn:uuid:5bbb0234-e2f1-4e8a-a37b-618fad191f53>
WARC-Target-URI: https://wayne.contentdm.oclc.org/digital/download/collection/afscme/id/163/size/large
WARC-Date: 2026-03-18T20:39:21Z
WARC-Payload-Digest: sha1:3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ
WARC-Concurrent-To: <urn:uuid:f3e4812d-eed5-4a5a-81d5-ed5a8b1663b1>
WARC-Block-Digest: sha1:3CHYVHHRLDJVRT7PEROR6NLWZ6C6NHLQ
Content-Type: application/http; msgtype=request
Content-Length: 211

GET /digital/download/collection/afscme/id/163/size/large HTTP/1.1
Host: wayne.contentdm.oclc.org
User-Agent: python-requests/2.32.5
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive



WARC/1.0
WARC-IP-Address: 152.19.134.47
WARC-Type: revisit
WARC-Record-ID: <urn:uuid:dae9f5ad-1abc-49b3-970d-b3f022c58c54>
WARC-Target-URI: https://www.gutenberg.org/cache/epub/9380/pg9380.txt
WARC-Date: 2026-03-18T20:39:21Z
WARC-Payload-Digest: sha1:X2NPIDT4PJ4O5SJJUOJVHB4YQRGJ3SXB
WARC-Profile: file-content; filename="files/pg9380.txt"
WARC-Block-Digest: sha1:RDFZEPTLCVS6NMX5PSBPQ5SSKTH25EUT
Content-Type: application/http; msgtype=response
Content-Length: 227

HTTP/1.1 200 OK
date: Wed, 18 Mar 2026 20:39:21 GMT
server: Apache
last-modified: Wed, 04 Mar 2026 14:20:15 GMT
accept-ranges: bytes
content-length: 323548
x-backend: gutenweb5
content-type: text/plain; charset=utf-8



WARC/1.0
WARC-IP-Address: 152.19.134.47
WARC-Type: request
WARC-Record-ID: <urn:uuid:16976612-5110-41ec-876c-1a9336607110>
WARC-Target-URI: https://www.gutenberg.org/cache/epub/9380/pg9380.txt
WARC-Date: 2026-03-18T20:39:21Z
WARC-Payload-Digest: sha1:3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ
WARC-Concurrent-To: <urn:uuid:dae9f5ad-1abc-49b3-970d-b3f022c58c54>
WARC-Block-Digest: sha1:O3LLQN5O4Z7FSA736R22PZOJGAF33PNL
Content-Type: application/http; msgtype=request
Content-Length: 178

GET /cache/epub/9380/pg9380.txt HTTP/1.1
Host: www.gutenberg.org
User-Agent: python-requests/2.32.5
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
```

There is a single pattern, repeated twice (two URLs):
- a `WARC-Type: revisit` record
- a `WARC-Type: request` record

The name of the file gives us a clue about its purpose: `headers.warc`.  This WARC file is designed to record metadata about the network requests made, but not necessarily capture the data.

The `WARC-Type: request` record makes sense: we want to record the exact network request we made to the server for the file we eventually downloaded and stored in the bag.  

But what about the `WARC-Type: revisit` record?  This is a non-standard use of that WARC record type, but for a specific purpose.  This is `nabit` using the WARC file format to communicate something, "The payload for this response lives somewhere else, in _this_ bag, not here in this WARC file."

That `WARC-Profile` value is `nabit`'s custom profile, signaling that the actual response body was saved as a discrete file in the BagIt bag (`files/large.jpg` and `files/pg9380.txt`) rather than embedded in the WARC record itself. 

It's a clever trick, showing the flexibility of the WARC format!

The rest of the files are specific to the [BagIt](https://datatracker.ietf.org/doc/html/rfc8493) specification. 

A quick explanation of the BagIt format from the specification:

> "...a set of hierarchical file layout conventions for storage and transfer of arbitrary digital content.  A "bag" has just enough structure to enclose descriptive metadata "tags" and a file "payload" but does not require knowledge of the payload's internal semantics.  This BagIt format is suitable for reliable storage and transfer."

Let's look at the BagIt files individually.

```text
├── bagit.txt
```

This file contains technical information about the `bagit` software version used.  This file is required.

```text
├── bag-info.txt
```

This file contains metadata about the bag, like what software was used to create it and when.  This file is optional.

```text
├── manifest-sha256.txt
```

This is one of the most important files in a BagIt archive and is required.  It contains checksums of the files in the Bag (e.g. MD5, SHA256, etc.).  Here are the contents of this file, which _should_ be the same for anyone that runs this lab with the same URLs from above (assuming the files haven't changed):

```text
02bcb467b8d90ab051dda669fd3ead4f5de393c562768e5ab2be9ac3675ba81e  data/files/large.jpg
32da5aa1608526d8452f93cc1c24560de451c7f62937c4f0628bdcd6b2198cf5  data/files/pg9380.txt
e4277b33eeb5d43519129b6956e30dfe69124065660c7d2ae8ec8245d540b646  data/signed-metadata.json
ed6c2fdef881b39ba3befaf90fb4e33d8fd4c11632548ad3ca6937b41087ddb5  data/headers.warc
```

The two rows for the data files -- `data/files/large.jpg` and `data/files/pg9380.txt` -- are fairly straight-forward.  They are a checksum of the data files this bag is built around.  

The other two are a bit more subtle:

- `data/headers.warc`: this checksum confirms that our WARC file is also untouched / unchanged after it's been added to the bag
- `data/signed-metadata.json`: similarly, this checksum ensures the metadata about the files is unchanged

Big picture, if any bytes in any of those files are modified, this bag will fail validation when verified (we'll do this in a moment!).

```text
└── tagmanifest-sha256.txt
```

This file is optional in the BagIt specification, but `nabit` opts to create it.  It provides checksums for other files in the bag:

```text
542f6fd0691214b2b17295e356ccd41025e22f41e7ed8419fe92f3ff34b2871c  bag-info.txt
66c06401e14bbb0e67b4ee909702cb1b2528bb3abbdfe38a94879b6279f24c5c  manifest-sha256.txt
e91f941be5973ff71f1dccbdd1a32d598881893a7f21be516aca743da38b1689  bagit.txt
```

### Validate our test bag

Next, we'll use the `nabit` program to validate the bag we just created:

```shell
 nabit validate test-bag-1
```

The result should be success, looking like the following:

```text
Validating package at test-bag-1 ...
SUCCESS: headers.warc found
SUCCESS: bag format is valid
WARNING: No signatures found
WARNING: No timestamps found
Package is valid
```

We do get a couple of warnings that no signatures were found (more on this in a moment), but it's a "valid" bag in the sense it a) satisfies the BagIt specification, and b) the files all match their checksums.  

Let's do a test!  Try opening the text file at `data/files/pg9380.txt`, and changing just a couple of letters at the beginning.  For example I'm making this change in the first line:

Original:
```text
The Project Gutenberg eBook of A Nonsense Anthology
```

Changed:
```text
The Project Gutenberg eBook of A Nonsense Anthology - PICKLES!
```

Now, if we validate the bag a second time, we should see a failure:

```shell
nabit validate test-bag-1
```

```text
Validating package at test-bag-1 ...
SUCCESS: headers.warc found
data/files/pg9380.txt sha256 validation failed: expected="32da5aa1608526d8452f93cc1c24560de451c7f62937c4f0628bdcd6b2198cf5" found="6443c006996f53afc4f7330acc0a247dba0f83f0e60dae7757f3693b6e7f2ca7"
ERROR: bag format is invalid: Bag validation failed: data/files/pg9380.txt sha256 validation failed: expected="32da5aa1608526d8452f93cc1c24560de451c7f62937c4f0628bdcd6b2198cf5" found="6443c006996f53afc4f7330acc0a247dba0f83f0e60dae7757f3693b6e7f2ca7"
WARNING: No signatures found
WARNING: No timestamps found
Error: Errors found in package
```

Looks like the checksums work!

### Additional Features

Reading through `nabit`'s [Quickstart Documentation](https://github.com/harvard-lil/bag-nabit?tab=readme-ov-file#quick-start) you can see some additional functionality:

- ability to add metadata into the `bag-info.txt` file with `-i "<field>:<value>"`
- ability to "sign" the bag with an SSL `.pem` file ([more documentation](https://github.com/harvard-lil/bag-nabit?tab=readme-ov-file#key-management-create-and-sign-workflows))
- ability to update the bag with more files using the `--amend` flag

While the documentation states that `nabit` is not a "web crawler", there is a [documentation section](https://github.com/harvard-lil/bag-nabit?tab=readme-ov-file#collection-backends) that muses how it could be extended for other protocols (e.g. FTP) or even architectures (e.g. a web crawler).

## Reflection Prompts

**1-** What role does the file `headers.warc` play in a bag-nabit bag? 

**2-** What are some real world scenarios where this tool might be handy?  

**3-** (Bonus) Do you think that data from a "normal" WARC file, created during the course of a crawl, could be used to retroactively make a BagIt preservation object for one or many distinct files?
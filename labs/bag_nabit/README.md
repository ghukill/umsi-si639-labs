# Lab: bag-nabit

## Overview

`bag-nabit` is a tool built by the Harvard Library Innovation Laboratory ([website](https://lil.law.harvard.edu/), [Github](https://github.com/harvard-lil)).  A [blog post from inkdroid.org](https://inkdroid.org/2025/02/17/nabit/) sums up the functionality nicely,

> 1. downloads all the URLs to disk
> 2. writes the dataset metadata to disk 
> 3. packages up the data and metadata into a BagIt directory (RFC 8493) 
> 4. records provenance about who did the work and when they did it 

What does this mean exactly?  and why is it useful?

Let's imagine the following scenario.

You are interested in downloading a text file from the Internet, a `.txt` file of the 1910 book "A Nonsense Anthology" from the Project Gutenberb website.  Let's assume that we want to preserve this file in such a way that other, future researchers can be sure the file was retrieved directly from a given URL, on a specific date, and was not modified during or after retrieval.  

This may seem like a simple task:

1. download the file
2. prepare some kind of preservation package
3. include metadata about when we downloaded it, who did, how we did it, etc., etc.
4. include the text file we jsut downloaded

Seems simple, right?  But what is stopping us -- nefariously or accidentally -- from:

1. modifying the text file
2. claiming it came from URL `https://foo.com/book.txt` but it actually came from `https://bar.net/other-book.txt`
3. claiming it was `2020-01-01`, but was actually today `2026-03-17`
4. and so forth...

Not much!  Depending on how we package it, metadata and data file metadata like created and modified dates, there is virtually nothing in our handmade preservation package that tethers it what actually occurred and how the package was made.

Enter `bag-nabit`!  As stated above, the purpose of this utility is to safeguard against the risks named above, and many more.  By using this tool to creat a preservation object, we get the following:

1. confirmation that the file was retrieved directly from URL `https://foo.com/book.txt`
2. the data is checksummed during download and checksummed when added to our preservation package
3. a WARC file is created that captures all network requests
4. optionally, signatures are added for who and when the operations took place that are very difficult to modify or forge
5. utilities for _verifying_ all these things after the fact

This is a bit of a niche tool, but one can imagine how important a role this could play in establishing the provenance of digital objects downloaded from the Internet.

Is this.... "web archiving"?  It depends on your definition!  The end goal is not a digital object that can support a replay experience of an internet browser -- what we often think of re: web archiving -- but we certainly preserving data / information from the web, and encoding enough information about the network interactiosn to replay the _authenticity_ of the data retrieved.  

Let's take it for a spin and see what other similarities of differenes emerge.

## Instructions

### Install Dependencies

If not using the `umsi-si639-labs` GitHub CodeSpace -- [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ghukill/umsi-si639-labs) -- make sure that `bag-nabit` is installed.  If you _are_ using CodeSpace, you can skip to the "Create Workspace" section.

As per usual, ensure that you have the SI639 labs github repository cloned and updated:

```shell
git clone https://github.com/ghukill/umsi-si639-labs
cd umsi-si639-labs
git pull origin main
```

Run command to update dependencies:
```shell
uv sync
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

## Reflection Prompts

TODO...
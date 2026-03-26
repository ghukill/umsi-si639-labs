from flask import Flask, render_template

from clients import AITCollection, AITPartnerClient

app = Flask(__name__)


@app.route("/")
def index_route():
    partner_client = AITPartnerClient()
    collections = partner_client.get("collection")
    return render_template("index.html", collections=collections)


@app.route("/collection/<int:collection_id>")
def collection_route(collection_id):
    collection = AITCollection(collection_id)

    crawls = collection.crawls()

    return render_template(
        "collection.html",
        collection=collection,
        crawls=crawls,
    )


@app.route("/collection/<int:collection_id>/crawl/<int:crawl_id>")
def crawl_route(collection_id, crawl_id):
    collection = AITCollection(collection_id)

    crawl_documents = collection.partner_client.get(
        f"reports/crawled-detail/{crawl_id}",
        no_limit=False,
        format="json",
        status_code=200,
        mimetype="text/html",
    )

    # construct and add Wayback links
    # NOTE: this feels *very* hacky to pull the crawl timestamp from the WARC filename.
    #   Is there a better way?  Probably so.
    for doc in crawl_documents:
        timestamp = doc["warc_filename"].split("-")[-3]
        doc["wayback_url"] = (
            f"https://wayback.archive-it.org/{collection_id}/{timestamp}/{doc['url']}"
        )

    return render_template(
        "crawl.html",
        collection=collection,
        crawl_id=crawl_id,
        documents=crawl_documents,
    )


if __name__ == "__main__":
    app.run(debug=True)

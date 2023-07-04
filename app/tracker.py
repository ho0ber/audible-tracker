import audible
import itertools
import time
from datetime import datetime
from tabulate import tabulate
from prometheus_client import start_http_server, Gauge

BOOK_POSITION = Gauge("book_position", "the positions of books in ms", ["asin", "book"])

def batched(iterable, batch_size):
    """ Replace with itertools.batched in python3.12"""
    iterator = iter(iterable)
    while batch := list(itertools.islice(iterator, batch_size)):
        yield batch

def delay_duration(func, seconds=60):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        if duration < seconds:
            time.sleep(seconds - duration)
        return result
    return wrapper

@delay_duration
def update_positions():
    auth = audible.Authenticator.from_file("/tmp/audible-creds")
    with audible.Client(auth=auth) as client:
        library = client.get(
            "1.0/library",
            num_results=1000,
            response_groups="product_desc, product_attrs",
            sort_by="-PurchaseDate"
        )

        asin_to_title = {}
        for i in library["items"]:
            asin_to_title[i["asin"]] = i["title"]

        asins = [b["asin"] for b in library["items"]]

        positions_table = []
        for asin_batch in batched(asins,25):
            last = client.get("1.0/annotations/lastpositions", asins=",".join(asin_batch))
            for pos in last["asin_last_position_heard_annots"]:
                if pos["last_position_heard"].get("status") == "Exists" and \
                    pos["last_position_heard"].get("position_ms") > 0:
                        asin = pos["asin"]
                        position = pos["last_position_heard"].get("position_ms")
                        updated = pos["last_position_heard"].get("last_updated")
                        title = asin_to_title[asin]
                        updated_dt = datetime.fromisoformat(updated)
                        if updated_dt > datetime.now() - datetime.timedelta(days = 2):
                            positions_table.append((asin, title, position, updated))
                            BOOK_POSITION.labels(asin, title).set(position)
        positions_table.sort(key=lambda x: x[3], reverse=True)
        print(tabulate(positions_table, headers=("asin", "title", "position", "updated")))
        return 

def main():
    start_http_server(9999)
    while True:
        update_positions()

if __name__ == "__main__":
    main()
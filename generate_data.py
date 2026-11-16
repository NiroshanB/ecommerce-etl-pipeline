"""Generate raw e-commerce data for the ETL pipeline.

The data is SYNTHETIC: random orders and website events for a fictional
online store. It is deliberately a little dirty (duplicate rows, missing
values, negative quantities, bad dates) so the pipeline has real
cleaning work to do. The fixed seed makes it reproducible.
"""
import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_ORDERS = 1500
N_EVENTS = 4000

PRODUCTS = {
    "P001": ("Wireless Headphones", "Electronics", 89.99),
    "P002": ("Mechanical Keyboard", "Electronics", 129.99),
    "P003": ("Laptop Stand", "Electronics", 49.99),
    "P004": ("Running Shoes", "Apparel", 119.99),
    "P005": ("Denim Jacket", "Apparel", 79.99),
    "P006": ("Yoga Mat", "Sports", 34.99),
    "P007": ("Dumbbell Set", "Sports", 59.99),
    "P008": ("Coffee Maker", "Home", 69.99),
    "P009": ("Desk Lamp", "Home", 39.99),
    "P010": ("Blender", "Home", 99.99),
    "P011": ("Smartwatch", "Electronics", 199.99),
    "P012": ("Water Bottle", "Sports", 24.99),
}
REGIONS = ["BC", "ON", "AB", "QC", "MB"]


def main() -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    product_ids = list(PRODUCTS)
    weights = rng.dirichlet(np.ones(len(product_ids)) * 2)

    order_ids = np.arange(10001, 10001 + N_ORDERS)
    customer_ids = rng.integers(1000, 1500, N_ORDERS)
    product_choices = rng.choice(product_ids, N_ORDERS, p=weights)
    dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 365, N_ORDERS), unit="D")

    orders = pd.DataFrame({
        "order_id": order_ids,
        "customer_id": customer_ids,
        "order_date": dates.strftime("%Y-%m-%d"),
        "product_id": product_choices,
        "quantity": rng.integers(1, 5, N_ORDERS),
        "region": rng.choice(REGIONS, N_ORDERS),
    })
    orders["product_name"] = orders["product_id"].map(lambda p: PRODUCTS[p][0])
    orders["category"] = orders["product_id"].map(lambda p: PRODUCTS[p][1])
    orders["unit_price"] = orders["product_id"].map(lambda p: PRODUCTS[p][2])

    # Inject realistic dirt: duplicates, missing region, bad quantity, bad date.
    dupes = orders.sample(15, random_state=1)
    orders = pd.concat([orders, dupes], ignore_index=True)
    orders.loc[orders.sample(10, random_state=2).index, "region"] = None
    orders.loc[orders.sample(5, random_state=3).index, "quantity"] = -1
    orders.loc[orders.sample(5, random_state=4).index, "order_date"] = "not-a-date"
    orders = orders.sample(frac=1, random_state=5).reset_index(drop=True)
    orders.to_csv("data/raw_orders.csv", index=False)

    event_types = ["page_view", "add_to_cart", "purchase", "search"]
    events = pd.DataFrame({
        "event_id": np.arange(1, N_EVENTS + 1),
        "customer_id": rng.integers(1000, 1500, N_EVENTS),
        "event_type": rng.choice(event_types, N_EVENTS,
                                 p=[0.55, 0.2, 0.15, 0.1]),
        "event_date": (pd.to_datetime("2024-01-01") + pd.to_timedelta(
            rng.integers(0, 365, N_EVENTS), unit="D")).strftime("%Y-%m-%d"),
        "product_id": rng.choice(product_ids, N_EVENTS),
    })
    events.to_csv("data/raw_events.csv", index=False)

    print(f"Wrote {len(orders)} raw orders to data/raw_orders.csv")
    print(f"Wrote {len(events)} raw events to data/raw_events.csv")


if __name__ == "__main__":
    main()

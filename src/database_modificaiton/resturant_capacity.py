import random

class ResturantCapacityEstimator:

    @staticmethod
    def estimate_capacity(store_name):
        name = str(store_name or "").lower()

        # Coffee / cafes
        if any(k in name for k in ["coffee", "espresso", "cafe", "bakery", "tea"]):
            return random.randint(20, 50)

        # Ice cream / dessert
        if any(k in name for k in ["ice cream", "gelato", "dessert", "donut", "cookie"]):
            return random.randint(15, 40)

        # Fast food chains
        if any(k in name for k in ["mcdonald", "subway", "chipotle", "kfc", "taco bell", "domino"]):
            return random.randint(30, 80)

        # Bars / pubs
        if any(k in name for k in ["bar", "tavern", "lounge", "pub"]):
            return random.randint(60, 150)

        # Breweries / large
        if any(k in name for k in ["brew", "public house", "taproom"]):
            return random.randint(120, 300)

        # Default restaurant
        return random.randint(50, 120)
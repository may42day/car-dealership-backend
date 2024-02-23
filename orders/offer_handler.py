from cars.models import Car, CarStockItem
from common.models import Company
from dealers.models import Dealer, DealerStockItem
from marketing.models import (
    PASSING_WEIGHT,
    DealerDiscount,
    DealerMarketingCampaign,
    Discount,
    MarketingCampaign,
)
from orders.models import CustomerOffer, DealerOffer, Offer
from abc import ABC, abstractmethod

from suppliers.models import Supplier


class BaseOfferHandler(ABC):
    """
    Abstract class for handling offers.
    Contains main logic for seller selection.
    Picking up cars, selecting best stock item, analyzing discounts and marketing campaigns.

    Used for CustomersOfferHandler and DealerOfferHandler classes.

    Attributes
    ----------
    offer : Offer
        contains main info about buyer offer
    sellers : list[Company]
        queryset with all sellers on market

    purchase_car : Car
        suggested car for purchase
    purchase_seller : Company
        suggested seller with best price
    purchase_price : int
        price of suggested car
    purchase_marketing_campaign : MarketingCampaign
        marketing campaign in case suggested car have the best price with specific campaign
    purchase_discount : Discount
        discount in case suggested car have the best price with specific discunt
    purchase_stock_item : CarStockItem
        suggested dealer's stock item

    sellers_data : dict
        Dictionary to handle data in different stages step by step.
        Example:
            self.sellers_data = {
                seller.pk: {
                    "object": seller,                               # Stage 1 (sellers_with_suitable_car_on_stock)
                    "suitable_stock": [stock_item1, stock_item2],   # Stage 1 (sellers_with_suitable_car_on_stock)
                    "best_stock_item": stock_item1,                 # Stage 2 (seller_best_stock_item)
                    "best_marketing_campaign": marketing_campaign,  # Stage 3 (seller_suitable_discounts)
                    "best_discount": discount,                      # Stage 4 (seller_suitable_marketing_campaigns)
                },
            }
    """

    def __init__(self):
        self.offer: Offer = None
        self.sellers: list[Company] = [None]
        self.sellers_data = {}

        self.purchase_car: Car = None
        self.purchase_seller: Company = None
        self.purchase_price: int = None
        self.purchase_marketing_campaign: MarketingCampaign = None
        self.purchase_discount: Discount = None
        self.purchase_stock_item: CarStockItem = None

    @abstractmethod
    def process_offer(self):
        """
        Abstract function. Must consist of all steps of selecting a seller
        """
        pass

    def _sellers_with_suitable_car_on_stock(self):
        """
        Function to exclude dealers with no suitable cars.

        Iterating by sellers stock items and checking whether it equal with car in offer.
        Also checking whether stock item price fits with max price in offer.
        Adding collected data to self.sellers_data for future handling.
        """
        sellers = []
        for seller in self.sellers:
            stock_items = []
            for stock_item in seller.stock.all():
                if stock_item.amount and self.offer.car == stock_item.car:
                    stock_items.append(stock_item)

            if stock_items:
                self.sellers_data[seller.pk] = {
                    "object": seller,
                    "suitable_stock": stock_items,
                }
                sellers.append(seller)

        self.sellers = sellers

    def _sellers_suitable_stock_items_by_characteristics(self):
        """
        Function to exclude dealers with no suitable car characteristics.

        Iterating by sellers car characteristics and checking whether it  equal with characteristic in offer.
        """
        for seller in self.sellers:
            stock_items = []
            for stock_item in seller.stock.all():
                if stock_item.amount and stock_item.is_fit_characteristic(
                    self.offer.characteristic
                ):
                    stock_items.append(stock_item)

            if stock_items:
                self.sellers_data[seller.pk] = {
                    "object": seller,
                    "suitable_stock": stock_items,
                }

    def _seller_best_stock_item(self):
        """
        Function to select the best stock item suitable for offer based on price.
        Handles data in self.sellers_data.

        Iterating for every stock item of each seller and selects the best item for every seller by price.
        """
        for key, value in self.sellers_data.items():
            stock_items = value["suitable_stock"]
            best_price = None
            best_stock_item = None
            for item in stock_items:
                if best_price and item.price_per_one < best_price:
                    best_price = item.price_per_one
                    best_stock_item = item
                elif not best_price:
                    best_price = item.price_per_one
                    best_stock_item = item

            self.sellers_data[key]["best_stock_item"] = best_stock_item

    @abstractmethod
    def _seller_suitable_discounts(self):
        """
        Function to analyze and select the best sellers discounts.
        """

    @abstractmethod
    def _seller_suitable_marketing_campaigns(self):
        """
        Function to analyze and select the best sellers marketing campaigns.
        """

    def _select_best_offer(self):
        """
        Function to select the best sellers offer.
        Handles data in self.sellers_data.
        For every best stock item for each seller and select the best suggestion with its discounts
        or marketing campaigns if they exists. Or just add price of stock item if no events exists.
        """
        for dealer_data in self.sellers_data.values():
            stock_item = dealer_data["best_stock_item"]
            price = stock_item.price_per_one

            # Set best price for comparing with discounts price
            best_price = self.purchase_price if self.purchase_price else price

            best_marketing_campaign = dealer_data.get("best_marketing_campaign")
            best_discount = dealer_data.get("best_discount")

            # For existing campaigns calculating the price with discounts
            # and set it in offer if price is more profitable.
            if best_marketing_campaign:
                price_with_discount = best_marketing_campaign.count_price_with_discount(
                    price
                )
                if price_with_discount < best_price:
                    self._change_best_offer(
                        stock_item,
                        price_with_discount,
                        dealer_data["object"],
                        marketing_campaign=best_marketing_campaign,
                    )
                    best_price = price_with_discount

            # For existing discounts calculating the price with discounts
            # and set it in offer if price is more profitable.
            if best_discount:
                price_with_discount = best_discount.count_price_with_discount(price)
                if price_with_discount < best_price:
                    self._change_best_offer(
                        stock_item,
                        price_with_discount,
                        dealer_data["object"],
                        discount=best_discount,
                    )
                    best_price = price_with_discount

            # Change offer if we hadn't set best price before or
            # current stock itemprice more profitable than saved.
            if not self.purchase_price or (
                self.purchase_price and stock_item.price_per_one < self.purchase_price
            ):
                self._change_best_offer(
                    stock_item, stock_item.price_per_one, dealer_data["object"]
                )

    def _change_best_offer(
        self, stock_item, price, dealer, discount=None, marketing_campaign=None
    ):
        """
        Function to change all attributes related to purchase.
        """
        self.purchase_car = None if not stock_item else stock_item.car
        self.purchase_seller = dealer
        self.purchase_price = price
        self.purchase_marketing_campaign = marketing_campaign
        self.purchase_discount = discount
        self.purchase_stock_item = stock_item

    def _check_max_price(self):
        """
        Checks wether max price is less or equal than best offer.

        Clear best offer if price is greater than max_price.
        """
        if (
            self.offer.max_price
            and self.purchase_price
            and self.purchase_price > self.offer.max_price
        ):
            self._change_best_offer(None, None, None)


class CustomersOfferHandler(BaseOfferHandler):
    """
    An interface for handling customer offer.
    Inherits from class BaseOfferHandler.

    Widen with:
        - process_offer. Main logic for selecting the best seller.
        - sellers_with_suitable_characteristics. Function to pick up seller by car characteristic.
        - seller_suitable_discounts. Function to collect suitable distounts for each seller.
        - seller_suitable_marketing_campaigns. Function to collect suitable marketing campaigns for each seller.

    """

    def __init__(self, offer: CustomerOffer, dealers: list[Dealer]):
        self.offer: CustomerOffer = offer
        self.sellers: list[Dealer] = dealers

        self.sellers_data = {}

        self.purchase_car: Car = None
        self.purchase_seller: Supplier = None
        self.purchase_price: int = None
        self.purchase_marketing_campaign: DealerMarketingCampaign = None
        self.purchase_discount: DealerDiscount = None
        self.purchase_stock_item: DealerStockItem = None

    def process_offer(self):
        """
        Handle offer from start to the end
        Picking up cars suitable for offer
        Analyzing prices based on discounts and marketing campaigns
        """
        if self.offer.characteristic:
            self._sellers_with_suitable_characteristics()
            self._sellers_suitable_stock_items_by_characteristics()
        else:
            self._sellers_with_suitable_car_on_stock()

        if self.sellers:
            self._seller_best_stock_item()
            self._seller_suitable_marketing_campaigns()
            self._seller_suitable_discounts()
            self._select_best_offer()
            self._check_max_price()

    def _sellers_with_suitable_characteristics(self):
        """
        Function to exclude dealers with no suitable characteristics.
        Checking every dealer whether their car characteristics on sale fits to offer car characteristic.
        Updates seller list only with suitable dealers.
        """
        dealers = []
        for dealer in self.sellers:
            for characteristic in dealer.car_characteristics.all():
                if self.offer.characteristic.is_suitable(characteristic):
                    dealers.append(dealer)
                    break
        self.sellers = dealers

    def _seller_suitable_discounts(self):
        """
        Function to analyze and select the best sellers discounts.

        """
        # collect customer's total purchases for each dealer in dict
        # with dealer pk as a key
        customer_total_purchases_dict = {}
        for purchase in self.offer.customer.total_purchases.all():
            customer_total_purchases_dict[purchase.dealer.pk] = purchase.amount

        if customer_total_purchases_dict:
            # handles self.sellers_data. Add best discount for every seller.
            for dealer in self.sellers:
                total_purchases = customer_total_purchases_dict.get(dealer.pk, 0)

                if total_purchases:
                    # flags to define the best discount among every seller.
                    best_discount_percentage = None
                    best_discount = None

                    # calculate best percentage for every dealer's discounts
                    for discount in dealer.discounts.all():
                        percentage = discount.get_discount_percentage(
                            total_purchases=total_purchases
                        )
                        # saved new discount and its percentage if current percentage not 0 and
                        # we haven't collect best_discount before of current percentage bigger than saved
                        if percentage and (
                            not best_discount_percentage
                            or percentage > best_discount_percentage
                        ):
                            best_discount_percentage = percentage
                            best_discount = discount

                    if best_discount:
                        self.sellers_data[dealer.pk]["best_discount"] = best_discount
                        self.sellers_data[dealer.pk][
                            "best_discount_percentage"
                        ] = best_discount_percentage

    def _seller_suitable_marketing_campaigns(self):
        """
        Function to analyze and select the best sellers marketing campaigns.

        Checking cars in every marketing campaign for each seller
        and select collect campaigns if they fits with cars by cars of by cars characteristics.
        """
        for dealer in self.sellers:
            # set flags to define the best campaign among every seller
            best_marketing_campaign = None
            marketing_campaigns_percentage = None

            marketing_campaigns = dealer.marketing_campaigns.all()
            for campaign in marketing_campaigns:
                if campaign.percentage != 0:
                    cars = campaign.cars.all()

                    # if campaign have cars and it fits with our car in offer
                    if cars and self.offer.car and self.offer.car in cars:
                        if (
                            best_marketing_campaign
                            and campaign.percentage > marketing_campaigns_percentage
                        ):
                            best_marketing_campaign = campaign
                            marketing_campaigns_percentage = campaign.percentage
                        elif not best_marketing_campaign:
                            best_marketing_campaign = campaign
                            marketing_campaigns_percentage = campaign.percentage

                    # if campaign have cars and it fits with our car characteristics in offer
                    elif cars and self.offer.characteristic:
                        # cheching whether one of the car in campaigns fits with characteristic in offer
                        campaigng_fits_with_car = False
                        for car in cars:
                            if car.is_fit_characteristic(self.offer.characteristic):
                                campaigng_fits_with_car = True
                                break

                        if campaigng_fits_with_car:
                            if (
                                best_marketing_campaign
                                and campaign.percentage > marketing_campaigns_percentage
                            ):
                                best_marketing_campaign = campaign
                                marketing_campaigns_percentage = campaign.percentage
                            elif not best_marketing_campaign:
                                best_marketing_campaign = campaign
                                marketing_campaigns_percentage = campaign.percentage

            if best_marketing_campaign:
                self.sellers_data[dealer.pk][
                    "best_marketing_campaign"
                ] = best_marketing_campaign
                self.sellers_data[dealer.pk][
                    "marketing_campaign_percentage"
                ] = marketing_campaigns_percentage


class DealerOfferHandler(BaseOfferHandler):
    """
    An interface for handling dealer offer.
    Inherits from class BaseOfferHandler.

    In comparison with default offer it have new attribute - amount.
    The large logic added in DealerOfferHandler refer to this field.

    Widen with:
        - process_offer. Main logic for selecting the best seller.
        - seller_suitable_discounts. Widen with including both discount types.
        - seller_suitable_marketing_campaigns. Function to select best marketing campaign for each seller.
        - analyze_perspective_cooperation. Function to estimate perspectives of cooperation with suppliers.

    Attributes
    ----------
    forecast_cooperation_with_supplier : Supplier
        suggested supplier for cooperation to get best price in future
    forecast_weight: float(0 to 1)
        calculated weight for cooperation on current conditions
    """

    def __init__(self, offer: DealerOffer, suppliers: list[Supplier]):
        self.offer = offer
        self.sellers = suppliers
        self.sellers_data = {}

        self.purchase_car = None
        self.purchase_seller = None
        self.purchase_price = None
        self.purchase_marketing_campaign = None
        self.purchase_discount = None
        self.purchase_stock_item = None

        # new fields
        self.forecast_cooperation_with_supplier = None
        self.forecast_weight = None

    def process_offer(self):
        """
        Handle offer from start to the end
        Picking up cars suitable for offer
        Analyzing prices based on discounts and marketing campaigns
        """
        self._sellers_with_suitable_car_on_stock()
        if self.sellers:
            self._seller_best_stock_item()
            self._seller_suitable_discounts()
            self._seller_suitable_marketing_campaigns()
            self._select_best_offer()
            self._analyze_perspective_cooperation()
            self._check_max_price()

    def _seller_suitable_discounts(self):
        """
        Function to analyze and select the best sellers discounts.

        Includes both discount types:
            - cumulative discount
            - bulk discount

        """
        # collect dealer's total purchases for each supplier in dict
        # with supplier pk as a key
        buyer_total_purchases_dict = {}
        for purchase in self.offer.dealer.orders_history.all():
            buyer_total_purchases_dict[purchase.supplier.pk] = purchase.amount

        if buyer_total_purchases_dict:
            for seller in self.sellers:
                total_purchases = buyer_total_purchases_dict.get(seller.pk, 0)
                # flags to define the best discount among every supplier.
                best_discount_percentage = None
                best_discount = None

                for discount in seller.discounts.all():
                    # calculate percentage based on discount type
                    if discount.discount_type == "BD":
                        percentage = discount.get_discount_percentage(
                            current_purchase_amount=self.offer.amount
                        )
                    elif discount.discount_type == "CD" and total_purchases:
                        percentage = discount.get_discount_percentage(
                            total_purchases=total_purchases
                        )
                    else:
                        percentage = 0

                    if percentage and not best_discount_percentage:
                        best_discount_percentage = percentage
                        best_discount = discount
                    elif percentage and percentage > best_discount_percentage:
                        best_discount_percentage = percentage
                        best_discount = discount

                if best_discount:
                    self.sellers_data[seller.pk]["best_discount"] = best_discount
                    self.sellers_data[seller.pk][
                        "best_discount_percentage"
                    ] = best_discount_percentage

    def _seller_suitable_marketing_campaigns(self):
        """
        Function to analyze and select the best sellers marketing campaigns.

        Checking cars in every marketing campaign for each seller
        and select collect campaigns if they fits with cars.
        """
        for dealer in self.sellers:
            # set flags to define the best campaign among each seller
            best_marketing_campaign = None
            marketing_campaigns_percentage = None

            marketing_campaigns = dealer.marketing_campaigns.all()
            # compare car with car in campaign for every supplier's marketing campaigns
            # if cars participate in campaign and percentage isn't 0
            for campaign in marketing_campaigns:
                if campaign.percentage != 0:
                    cars = campaign.cars.all()
                    if cars and self.offer.car and self.offer.car in cars:
                        if (
                            best_marketing_campaign
                            and campaign.percentage > marketing_campaigns_percentage
                        ):
                            best_marketing_campaign = campaign
                            marketing_campaigns_percentage = campaign.percentage
                        elif not best_marketing_campaign:
                            best_marketing_campaign = campaign
                            marketing_campaigns_percentage = campaign.percentage

            if best_marketing_campaign:
                self.sellers_data[dealer.pk][
                    "best_marketing_campaign"
                ] = best_marketing_campaign
                self.sellers_data[dealer.pk][
                    "marketing_campaign_percentage"
                ] = marketing_campaigns_percentage

    def _analyze_perspective_cooperation(self):
        """
        Function to analyze perspective cooperation with supplier.
        Calculates forecast weights only for cumulative discounts.
        """
        # collect dealer's total purchases for each supplier in dict
        # with supplier pk as a key
        seller_total_purchases_dict = {}
        for purchase in self.offer.dealer.orders_history.all():
            seller_total_purchases_dict[purchase.supplier.pk] = purchase.amount

        if seller_total_purchases_dict:
            for seller in self.sellers:
                total_purchases = seller_total_purchases_dict.get(seller.pk, 0)
                if total_purchases:
                    # collect all cumulative discounts in list
                    cumulative_discounts = [
                        discount
                        for discount in seller.discounts.all()
                        if discount.discount_type == "CD"
                    ]
                    # sort disounts by its percentage
                    sorted_discounts = sorted(
                        cumulative_discounts, key=lambda d: d.percentage, reverse=True
                    )

                    dealer_best_price = self.sellers_data[seller.pk][
                        "best_stock_item"
                    ].price_per_one
                    # calculating weights for every discount and set as a suggested for cooperation
                    # in case weight is bigger than its defined border (PASSING_WEIGHT)
                    for discount in sorted_discounts:
                        weight = discount.estimate_foreceast_of_cooperation(
                            self.purchase_price, dealer_best_price, total_purchases
                        )
                        if weight >= PASSING_WEIGHT and (
                            (self.forecast_weight and weight > self.forecast_weight)
                            or not self.forecast_weight
                        ):
                            self.forecast_cooperation_with_supplier = seller
                            self.forecast_weight = weight
                            break

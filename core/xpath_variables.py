class ThingsXpath:
    # Product page parameters
    # Select country
    country_button_main = "//div[@class='m_chose_country']"

    # language options container
    language_options = "//div[@class='lang_part']/div[@class='bm_option']"

    # Select language options
    language_option_ru = "//div[@class='lang_part']/div[@class='bm_option']/div[@class='option_list']/a[@title='Русский']"
    language_option_en = "//div[@class='lang_part']/div[@class='bm_option']/div[@class='option_list']/a[@title='English']"

    # Countries container
    country_options = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='m_pullDown_country']"

    # Country options
    country_options_ru = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='m_pullDown_country openD']/div[@class='m_more_country']/ul/li[@class='RU']"
    country_options_en = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='m_pullDown_country openD']/div[@class='m_more_country']/ul/li[@class='US']"

    # Currency container
    currency = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='currency_part']//div[@class='result']"

    # Currency options
    currency_option_rub = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='currency_part']//div[@class='option_list']/a[@data-currency='RUB']"
    currency_option_en = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='currency_part']//div[@class='option_list']/a[@data-currency='USD']"

    # Save settings option
    button_save = "//div[@class='bm_dialog m_shipto_wrap_dialog hide dialog_show']//div[@class='m_shipto_wrap']//div[@class='btn_wrap']//div[@class='btn_save']/a"

    # Cookies
    site_cookies_button = "//input[@class='bm_btn_A minor']"

    # Product name
    product_title = "//div[@class='lineBlock showInformation']/h1/span"

    # Product subtitle
    product_subtitle = "//div[@class='lineBlock showInformation']/h2[@class='sub_title']"

    # Description
    product_description = "//section[@class='contentInside proInfWarp lbBox']//div[@id='description']"

    # Sale price
    product_sale_price_usd = "//div[@class='lineBlock showInformation']//p[@id='detailPrice']"
    product_sale_price_rub = "//div[@class='lineBlock showInformation']//div[@class='priceWarp']" \
                             "//div[@class='lineBlock currency']//ul[@id='currency']//li[7]"

    # Regular price
    product_regular_price = "//div[@class='lineBlock showInformation']//div[@class='saleWarp']//span[@id='d_origprice']"

    # Soled things count
    product_sold = "//div[@class='lineBlock showInformation']//div[@class='m_sales_promotion']//span[@class='pro_sell']"

    # Rating
    product_rating_value = "//div[@class='lineBlock showInformation']//div[@class='productReviews lineBlock']" \
                           "//span[@itemprop='ratingValue']"

    # Review count
    product_review_count = "//div[@class='lineBlock showInformation']//span[@itemprop='reviewCount']"

    # Product options
    product_options_container = "//div[@class='m_item_wrap color']"

    # Product option type name
    product_option_name = ".//p[@class='item_line proColor']//span"

    # Product options name
    product_available_options = ".//div[@class='item_box']/ul/li"

    # Delivery destination
    product_delivery_logistics = "//span[@class='logistics_b']"

    # Warehouses container
    product_shipping_from = "//div[@class='m_item_wrap shippingFrom']"  # single

    # Warehouses
    product_warehouses = "//div[@class='item_box']/ul/li[contains(@class,'lineBlock') and not(contains (@class,'invalids'))]"

    # Table shipping methods item
    product_shipping_methods = "//tr[contains(@class,'sel_b')]"

    # Exit shipping dialog button
    exit_shipping_dialog = "//div[@class='dialogs logistics_c dialogs_show']//span[@class='dialogs_c']//i[@class='close_dialogs']"

    # Name of option
    product_delivery_option_name = "./td[2]/a"

    # Estimated shipping time
    product_delivery_time = "./td[3]/a"

    # Tracking number
    product_delivery_tracking_number = "./td[4]"

    # Shipping cost
    product_delivery_shipping_cost = "./td[5]"

    # Main image
    product_title_image = "//li[contains(@class,'cpActive')]/a"

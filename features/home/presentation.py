from os.path import join, dirname, basename
from kivy.clock import triggered
from kivy.lang import Builder
from features.basescreen import BaseScreen

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class HomeScreen(BaseScreen):
    billing_client = None

    @triggered(2)
    def on_enter(self): pass

    def support(self, product_id, subscribe):
        print(product_id, subscribe)
        from sjbillingclient.jclass.billing import BillingResponseCode, ProductType
        from sjbillingclient.tools import BillingClient

        if self.billing_client:
            self.billing_client.end_connection()

        def on_acknowledge_purchase_response(billing_result):
            print(billing_result.getDebugMessage())
            if billing_result.getResponseCode() == BillingResponseCode.OK:
                self.toast("Thank you for subscribing to buy us a cup of coffee! monthly")

        def on_consume_response(billing_result):
            if billing_result.getResponseCode() == BillingResponseCode.OK:
                self.toast("Thank you for buying us a cup of coffee!")

        def on_purchases_updated(billing_result, null, purchases):
            if billing_result.getResponseCode() == BillingResponseCode.OK and not null:
                for purchase in purchases:
                    if subscribe:
                        self.billing_client.acknowledge_purchase(
                            purchase_token=purchase.getPurchaseToken(),
                            on_acknowledge_purchase_response=on_acknowledge_purchase_response
                        )
                    else:
                        self.billing_client.consume_async(purchase, on_consume_response)

        self.billing_client = BillingClient(on_purchases_updated=on_purchases_updated)

        def on_product_details_response(billing_result, product_details_list):
            for product_details in product_details_list:
                self.billing_client.get_product_details(
                    product_details,
                    ProductType.SUBS if subscribe else ProductType.INAPP)
            if billing_result.getResponseCode() == BillingResponseCode.OK:
                self.billing_client.launch_billing_flow(product_details=product_details_list)

        def on_billing_setup_finished(billing_result):
            if billing_result.getResponseCode() == BillingResponseCode.OK:
                self.billing_client.query_product_details_async(
                    product_type=ProductType.SUBS if subscribe else ProductType.INAPP,
                    products_ids=[product_id],
                    on_product_details_response=on_product_details_response,
                )

        self.billing_client.start_connection(
            on_billing_setup_finished=on_billing_setup_finished,
            on_billing_service_disconnected=lambda: print("disconnected")
        )

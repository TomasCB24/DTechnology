from django.contrib import admin

from .models import Product, OrderProduct, Order, Address


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['ref_id',
                    'ref_code',
                    'ordered',
                    'being_delivered',
                    'received',
                    'shipping_address',
                    'billing_address',
                    ]
    list_display_links = [
        'ref_code',
        'shipping_address',
        'billing_address',
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   ]
    search_fields = [
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'street_address',
        'apartment_address',
        'country',
    ]
    list_filter = ['country']
    search_fields = ['street_address', 'apartment_address']


admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)


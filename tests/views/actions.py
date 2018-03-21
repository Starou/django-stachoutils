def sell_cars(modeladmin, request, queryset):
    queryset.update(for_sale=True)
sell_cars.short_description = 'Sell the cars'

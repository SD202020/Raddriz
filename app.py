total = 0

for z in zones_data:

    # 1. БАЗА (сильная разница!)
    if z["size"] == "маленькая":
        price = 60
    elif z["size"] == "средняя":
        price = 120
    else:
        price = 220

    # 2. СЛОЖНОСТЬ
    price *= location_mult[z["location"]]
    price *= material_mult[z["material"]]
    price *= brand_mult.get(brand, 1.0)

    # 3. ВМЯТИНЫ (важно!)
    price *= (1 + (z["dents"] - 1) * 0.35)

    total += price

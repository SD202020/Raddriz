import streamlit as st

st.set_page_config(page_title="Raddriz MAP", layout="centered")

st.title("Raddriz MAP 🔧 PDR калькулятор")

mode = st.radio("Режим", ["Обычный", "Град (Hail)"])
vehicle_type = st.radio("Тип транспорта", ["Авто", "Мото"])

# ======================================================
# DATA
# ======================================================

base_price = {
    "маленькая": 50,
    "средняя": 110,
    "большая": 200
}

size_mult = {
    "маленькая": 1.0,
    "средняя": 1.4,
    "большая": 2.2
}

location_data = {
    "дверь (плоско)": 1.0,
    "дверь (ребро)": 1.25,
    "капот (плоско)": 1.0,
    "капот (ребро)": 1.25,
    "багажник (плоско)": 1.05,
    "багажник (ребро)": 1.3,
    "крыша (плоско)": 1.1,
    "крыша (ребро)": 1.35,
    "крыло переднее (плоско)": 1.1,
    "крыло переднее (ребро)": 1.35,
    "крыло заднее (плоско)": 1.2,
    "крыло заднее (ребро)": 1.45,
    "стойка": 1.5,
    "жесткое ребро": 1.6
}

hail_parts = {
    "капот": 1.0,
    "крыша": 1.2,
    "багажник": 1.0,
    "дверь передняя": 0.9,
    "дверь задняя": 0.9,
    "крыло переднее": 1.0,
    "крыло заднее": 1.1,
    "стойка": 1.3
}

material_mult = {
    "сталь": 1.0,
    "алюминий": 1.25
}

brand_mult = {
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.05,
    "bmw": 1.15,
    "audi": 1.15,
    "mercedes": 1.2
}

# ======================================================
# 🚗 AUTO
# ======================================================

if vehicle_type == "Авто":

    brand = st.text_input("Марка авто").lower()

    # ================= ОБЫЧНЫЙ =================
    if mode == "Обычный":

        zones_count = st.number_input("Сколько зон?", 1, 20, 1)

        zones = []

        for i in range(int(zones_count)):

            st.markdown(f"### Зона {i+1}")

            location = st.selectbox(
                "Место",
                list(location_data.keys()),
                key=f"loc_{i}"
            )

            material = st.selectbox(
                "Материал",
                list(material_mult.keys()),
                key=f"mat_{i}"
            )

            small = st.number_input("Маленькие", 0, 1000, 0, key=f"s_{i}")
            medium = st.number_input("Средние", 0, 1000, 0, key=f"m_{i}")
            large = st.number_input("Большие", 0, 1000, 0, key=f"l_{i}")

            zones.append({
                "location": location,
                "material": material,
                "small": small,
                "medium": medium,
                "large": large
            })

        if st.button("Рассчитать"):

            total = 0

            for z in zones:

                for size, count in [
                    ("маленькая", z["small"]),
                    ("средняя", z["medium"]),
                    ("большая", z["large"])
                ]:

                    if count == 0:
                        continue

                    price = base_price[size]
                    price *= location_data[z["location"]]
                    price *= material_mult[z["material"]]
                    price *= brand_mult.get(brand, 1.0)

                    if count > 50:
                        price *= (count * 9) * size_mult[size] * 0.7
                    else:
                        price *= (1 + 0.25 * (count - 1)) * (0.96 ** (count - 1))

                    total += price

            total = int(round(total / 10) * 10)

            st.subheader(f"💰 Итог: {total} €")

    # ================= ГРАД =================
    else:

        st.subheader("🌨️ Град")

        parts_count = st.number_input("Сколько деталей?", 1, 15, 1)

        parts = []

        for i in range(int(parts_count)):

            st.markdown(f"### Деталь {i+1}")

            part = st.selectbox(
                "Деталь",
                list(hail_parts.keys()),
                key=f"p_{i}"
            )

            material = st.selectbox(
                "Материал",
                list(material_mult.keys()),
                key=f"mat_h_{i}"
            )

            small = st.number_input("Маленькие", 0, 1000, 20, key=f"hs_{i}")
            medium = st.number_input("Средние", 0, 1000, 0, key=f"hm_{i}")
            large = st.number_input("Большие", 0, 1000, 0, key=f"hl_{i}")

            parts.append({
                "part": part,
                "material": material,
                "small": small,
                "medium": medium,
                "large": large
            })

        if st.button("Рассчитать град"):

            total = 0

            for p in parts:

                for size, count in [
                    ("маленькая", p["small"]),
                    ("средняя", p["medium"]),
                    ("большая", p["large"])
                ]:

                    if count == 0:
                        continue

                    base = 6  # дешевле чем обычка

                    price = count * base
                    price *= size_mult[size]
                    price *= hail_parts[p["part"]]
                    price *= material_mult[p["material"]]
                    price *= brand_mult.get(brand, 1.0)

                    total += price

            total *= 0.9  # объем

            total = int(round(total / 10) * 10)

            st.subheader(f"💰 Цена: {total} €")

# ======================================================
# 🏍️ МОТО
# ======================================================

else:

    st.subheader("🏍️ Мото")

    moto_type = st.selectbox("Тип", ["Harley", "Sport", "Other"])
    material = st.selectbox("Материал", ["сталь", "алюминий"])

    small = st.number_input("Маленькие", 0, 1000, 0)
    medium = st.number_input("Средние", 0, 1000, 0)
    large = st.number_input("Большие", 0, 1000, 0)

    moto_mult = {
        "Harley": 1.55,
        "Sport": 1.35,
        "Other": 1.15
    }

    total = 0

    for size, count in [
        ("маленькая", small),
        ("средняя", medium),
        ("большая", large)
    ]:

        if count == 0:
            continue

        price = base_price[size]
        price *= moto_mult[moto_type]
        price *= material_mult[material]
        price *= (1 + 0.30 * (count - 1)) * (0.95 ** (count - 1))

        total += price

    total = int(round(total / 10) * 10)

    st.subheader(f"💰 Цена: {total} €")

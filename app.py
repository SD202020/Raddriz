import streamlit as st

st.set_page_config(page_title="Raddriz MAP", layout="centered")

st.title("Raddriz MAP 🔧 PDR калькулятор")

# ---------------- MODE ----------------
mode = st.radio("Режим", ["Обычный", "Град (Hail)"])
vehicle_type = st.radio("Тип транспорта", ["Авто", "Мото"])

# ======================================================
# 🚗 AUTO DATA
# ======================================================

base_price = {
    "маленькая": 50,
    "средняя": 110,
    "большая": 200
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

    # =========================
    # 🔹 ОБЫЧНЫЙ РЕЖИМ
    # =========================
    if mode == "Обычный":

        zones_count = st.number_input("Сколько зон?", 1, 20, 1)

        zones = []

        for i in range(int(zones_count)):

            st.markdown(f"### Зона {i+1}")

            size = st.selectbox(
                "Размер",
                ["маленькая", "средняя", "большая"],
                key=f"size_{i}"
            )

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

            dents = st.number_input(
                "Вмятины",
                1, 1000, 1,
                key=f"dents_{i}"
            )

            zones.append({
                "size": size,
                "location": location,
                "material": material,
                "dents": dents
            })

        if st.button("Рассчитать"):

            total = 0

            for z in zones:

                price = base_price[z["size"]]
                price *= location_data[z["location"]]
                price *= material_mult[z["material"]]
                price *= brand_mult.get(brand, 1.0)

                d = z["dents"]

                # авто-град если много
                if d > 50:
                    price *= (d * 8) * 0.6   # оптовая логика
                else:
                    price *= (1 + 0.25 * (d - 1)) * (0.96 ** (d - 1))

                total += price

            total = int(round(total / 10) * 10)

            st.subheader(f"💰 Итог: {total} €")

    # =========================
    # 🌨️ ГРАД РЕЖИМ
    # =========================
    else:

        st.subheader("🌨️ Град — быстрый расчёт")

        parts_count = st.number_input("Сколько деталей?", 1, 15, 1)

        parts = []

        for i in range(int(parts_count)):

            st.markdown(f"### Деталь {i+1}")

            part = st.selectbox(
                "Деталь",
                list(hail_parts.keys()),
                key=f"hail_part_{i}"
            )

            dents = st.number_input(
                "Количество вмятин",
                1, 1000, 50,
                key=f"hail_dents_{i}"
            )

            material = st.selectbox(
                "Материал",
                list(material_mult.keys()),
                key=f"hail_mat_{i}"
            )

            parts.append({
                "part": part,
                "dents": dents,
                "material": material
            })

        if st.button("Рассчитать град"):

            total = 0

            for p in parts:

                base = 8  # цена за точку

                price = p["dents"] * base
                price *= hail_parts[p["part"]]
                price *= material_mult[p["material"]]
                price *= brand_mult.get(brand, 1.0)

                total += price

            total *= 0.85  # скидка за объем

            total = int(round(total / 10) * 10)

            st.subheader(f"💰 Цена за град: {total} €")

# ======================================================
# 🏍️ MOTORCYCLE
# ======================================================

else:

    st.subheader("🏍️ Мото расчёт")

    moto_type = st.selectbox("Тип мото", ["Harley", "Sport", "Other"])

    tank_size_cm = st.number_input("Вмятина бака (см)", 1, 50, 5)

    dents = st.number_input("Количество вмятин", 1, 1000, 1)

    material = st.selectbox("Материал", ["сталь", "алюминий"])

    base_moto = 75

    moto_mult = {
        "Harley": 1.55,
        "Sport": 1.35,
        "Other": 1.15
    }

    price = base_moto
    price *= (1 + tank_size_cm * 0.20)
    price *= (1 + 0.30 * (dents - 1)) * (0.95 ** (dents - 1))
    price *= moto_mult[moto_type]
    price *= material_mult[material]

    price = int(round(price / 10) * 10)

    st.subheader(f"💰 Цена: {price} €")

import streamlit as st

st.set_page_config(page_title="Raddriz MAP", layout="centered")

st.title("Raddriz MAP 🔧")

st.write("Выбор зоны ремонта (карта автомобиля)")

# ---------------- БАЗА ----------------
base_price = {
    "маленькая": 70,
    "средняя": 140,
    "большая": 260
}

# ---------------- КАРТА МАШИНЫ ----------------
# это и есть "карта" (упрощённая версия)
map_zones = {
    "дверь (плоско)": 1.0,
    "дверь (ребро/линия)": 1.35,

    "капот (плоско)": 1.0,
    "капот (ребро/линия)": 1.35,

    "багажник (плоско)": 1.05,
    "багажник (ребро/линия)": 1.4,

    "крыша (плоско)": 1.15,
    "крыша (ребро/линия)": 1.5,

    "стойка": 1.6
}

material_mult = {
    "сталь": 1.0,
    "алюминий": 1.35
}

brand_mult = {
    "": 1.0,
    "fiat": 1.0,
    "volvo": 1.1,
    "bmw": 1.3,
    "audi": 1.3,
    "mercedes": 1.4
}

# ---------------- INPUT ----------------
brand = st.text_input("Марка авто (bmw, audi, mercedes...)").lower()

zones_count = st.number_input("Сколько зон повреждений?", 1, 10, 1)

zones = []

for i in range(int(zones_count)):

    st.markdown(f"### Зона {i+1}")

    size = st.selectbox(
        "Размер вмятины",
        ["маленькая", "средняя", "большая"],
        key=f"size_{i}"
    )

    zone = st.selectbox(
        "КАРТА (где вмятина)",
        list(map_zones.keys()),
        key=f"zone_{i}"
    )

    material = st.selectbox(
        "Материал",
        list(material_mult.keys()),
        key=f"mat_{i}"
    )

    dents = st.number_input(
        "Количество вмятин",
        1, 10, 1,
        key=f"dents_{i}"
    )

    zones.append({
        "size": size,
        "zone": zone,
        "material": material,
        "dents": dents
    })

# ---------------- РАСЧЁТ ----------------
if st.button("Рассчитать цену"):

    total = 0

    for z in zones:

        price = base_price[z["size"]]

        # карта (самое важное)
        price *= map_zones[z["zone"]]

        price *= material_mult[z["material"]]
        price *= brand_mult.get(brand, 1.0)

        # вмятины
        price *= (1 + (z["dents"] - 1) * 0.45)

        total += price

    # ограничения рынка
    total = max(130, min(total, 900))

    fast = int(total * 0.85)
    normal = int(total)
    final = int(round(total / 10) * 10)

    st.subheader("💰 Результат")

    st.write(f"💨 Быстро: {fast} €")
    st.write(f"💼 Норм: {normal} €")
    st.write(f"✅ Итог: {final} €")

    st.text_area(
        "Сообщение клиенту",
        f"Цена ремонта без покраски (PDR): {final}€"
    )

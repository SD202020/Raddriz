import streamlit as st

st.title("PDR Calculator PRO+ 🔥")

lang = st.selectbox("Язык / Lingua", ["Русский", "Italiano"])

# --- БАЗА ---
base = {"small": 50, "medium": 75, "large": 110}
loc = {"door": 0, "hood": 0, "trunk": 10, "roof": 20, "pillar": 35, "edge": 40}
mat = {"steel": 0, "aluminum": 25}
brand_add = {"fiat": 0, "bmw": 25, "audi": 25, "mercedes": 25, "volvo": 15}

brand = st.text_input("Марка / Marca").lower()

# --- МУЛЬТИ ЗОНЫ ---
total = 0
num_blocks = st.number_input("Сколько зон?", min_value=1, max_value=10, value=1)

for i in range(num_blocks):
    st.markdown(f"### Зона {i+1}")

    size = st.selectbox(f"Размер {i+1}", ["small", "medium", "large"], key=f"s{i}")
    location = st.selectbox(f"Место {i+1}", ["door", "hood", "trunk", "roof", "pillar", "edge"], key=f"l{i}")
    material = st.selectbox(f"Материал {i+1}", ["steel", "aluminum"], key=f"m{i}")
    dents = st.number_input(f"Кол-во {i+1}", min_value=1, value=1, key=f"d{i}")

    price = base[size] + loc[location] + mat[material] + brand_add.get(brand, 10)
    price += (dents - 1) * 20

    total += price

# --- ЛОГИКА НЕАПОЛЯ ---
if total < 120:
    total = 120

if total > 450:
    total = 450

fast = int(total * 0.85)

# --- РЕЖИМ ПРОДАЖ ---
mode = st.selectbox("Режим", ["Обычный", "Закрыть клиента", "Свой клиент"])

if mode == "Закрыть клиента":
    final_price = int(fast * 0.95)   # ещё чуть ниже
elif mode == "Свой клиент":
    final_price = int(total * 0.9)   # небольшая скидка
else:
    final_price = total

# округление для психологии (например 287 → 290)
final_price = int(round(final_price / 10) * 10)

# --- ВЫВОД ---
st.subheader("💰 Цена")

st.write(f"💨 Быстро: {fast} €")
st.write(f"💼 Норм: {total} €")
st.write(f"✅ Итог для клиента: {final_price} €")

# --- ТЕКСТ КЛИЕНТУ ---
if lang == "Italiano":
    text = f"Prezzo per la riparazione: {final_price}€ senza verniciatura (PDR)"
else:
    text = f"Цена ремонта: {final_price}€ без покраски (PDR)"

st.text_area("Сообщение клиенту", text)

if st.button("📋 Скопировать"):
    st.success("Скопировано! Вставь в WhatsApp 👍")

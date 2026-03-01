# ========================= # IMPORTS # ========================= 
import streamlit as st

# ─── Page config must be FIRST Streamlit call ───────────────────────────────
st.set_page_config(
    page_title="Food Ordering",
    layout="centered",
)

# ─── Menu data ───────────────────────────────────────────────────────────────
MENU = {
    'starters': [
        {"id": "S1", "name": "gobi manchurian",    "price": 100},
        {"id": "S2", "name": "paneer manchurian",   "price": 200},
        {"id": "S3", "name": "mushroom manchurian", "price": 80},
    ],
    'deserts': [
        {"id": "DS1", "name": "chocolate fudge",          "price": 300},
        {"id": "DS2", "name": "death by chocolate",       "price": 200},
        {"id": "DS3", "name": "ferrero rocher ice cream", "price": 100},
    ]
}

# ─── Session state init ──────────────────────────────────────────────────────
if "cart" not in st.session_state:
    st.session_state.cart = []
if "order_history" not in st.session_state:
    st.session_state.order_history = []

# ─── Helper functions ────────────────────────────────────────────────────────
def browse_menu(category: str = "all") -> dict:
    if category == "all":
        return MENU
    return {category: MENU.get(category)}


def add_to_cart(item_id: str, quantity: int = 1) -> dict:
    for cat_items in MENU.values():
        for item in cat_items:
            if item['id'].upper() == item_id.upper():
                for ci in st.session_state.cart:
                    if ci['id'] == item['id']:
                        ci['qty'] += quantity
                        return {'status': 'updated'}
                st.session_state.cart.append({**item, "qty": quantity})
                return {'status': 'added new item'}
    return {'status': 'error', 'message': f'Item {item_id} not found'}


def place_order() -> dict:
    cart = st.session_state.cart
    if not cart:
        return {"status": "error", "message": "No items to order"}

    total = sum(item['price'] * item['qty'] for item in cart)
    order_id = f"ORD-{len(st.session_state.order_history) + 1}"

    st.session_state.order_history.append({
        "id": order_id,
        "items": cart.copy(),
        "total": round(total)
    })

    st.session_state.cart = []
    return {"status": "success", "message": "Order placed", "order_id": order_id}


# ─── UI ──────────────────────────────────────────────────────────────────────
st.title("🍽️ Food Ordering")

# --- Browse Menu ---
st.header("Menu")
category = st.selectbox("Category", ["all", "starters", "deserts"])
menu = browse_menu(category)
for cat, items in menu.items():
    st.subheader(cat.capitalize())
    for item in items:
        st.write(f"**{item['id']}** — {item['name']}  |  ₹{item['price']}")

st.divider()

# --- Add to Cart ---
st.header("Add to Cart")
col1, col2 = st.columns(2)
with col1:
    item_id = st.text_input("Item ID (e.g. S1, DS2)")
with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1)

if st.button("Add to Cart"):
    if item_id:
        result = add_to_cart(item_id.strip(), quantity)
        if result['status'] == 'error':
            st.error(result['message'])
        else:
            st.success(f"Cart {result['status']}!")
    else:
        st.warning("Please enter an item ID.")

st.divider()

# --- Cart ---
st.header("🛒 Your Cart")
if st.session_state.cart:
    for ci in st.session_state.cart:
        st.write(f"**{ci['name']}** x{ci['qty']}  —  ₹{ci['price'] * ci['qty']}")
    total = sum(ci['price'] * ci['qty'] for ci in st.session_state.cart)
    st.write(f"**Total: ₹{total}**")

    if st.button("Place Order"):
        result = place_order()
        if result['status'] == 'success':
            st.success(f"✅ {result['message']}! Order ID: {result['order_id']}")
        else:
            st.error(result['message'])
else:
    st.info("Your cart is empty.")

st.divider()

# --- Order History ---
st.header("📋 Order History")
if st.session_state.order_history:
    for order in reversed(st.session_state.order_history):
        with st.expander(f"Order {order['id']} — ₹{order['total']}"):
            for item in order['items']:
                st.write(f"- {item['name']} x{item['qty']}")
else:
    st.info("No orders yet.")
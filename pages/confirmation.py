import streamlit as st
from services.database_service import get_order_details

st.set_page_config(page_title="Order Status", page_icon="✅")

st.title("Order Confirmation")
st.caption("Track the live status of your order")

# Get the order ID saved by customer.py
order_id = st.session_state.get("last_order_id")

if not order_id:
    st.warning("No order found. Please place an order first.")
    if st.button("Go back to menu"):
        st.switch_page("pages/customer.py")
    st.stop()

# Fetch current order details from database
order = get_order_details(order_id)

if not order:
    st.error(f"Could not find order #{order_id}.")
    st.stop()

# Status tracker
STATUS_STEPS = ["pending", "preparing", "ready", "completed"]
current_status = order["order_status"]

st.subheader(f"Order #{order_id} — Table {st.session_state.get('last_order_table', '')}")

# Visual progress bar
if current_status in STATUS_STEPS:
    step = STATUS_STEPS.index(current_status)
    progress = (step + 1) / len(STATUS_STEPS)
    st.progress(progress)

# Status message
STATUS_MESSAGES = {
    "pending":   "Your order has been received and is waiting for the kitchen.",
    "preparing": "The kitchen is preparing your order right now.",
    "ready":     "Your order is ready for pickup!",
    "completed": "Your order has been completed. Enjoy your meal!",
    "cancelled": "This order has been cancelled.",
}

st.info(STATUS_MESSAGES.get(current_status, f"Status: {current_status}"))

# Order summary
st.subheader("What you ordered")
for item in order.get("items", []):
    st.write(f"• {item['quantity']} x {item['item_name']}")
    if item.get("special_instructions"):
        st.caption(f"  Note: {item['special_instructions']}")

st.write(f"**Total: ${order['order_total']:.2f}**")

st.divider()

# Refresh button
col1, col2 = st.columns(2)
with col1:
    if st.button("Refresh status"):
        st.rerun()
with col2:
    if st.button("Place a new order"):
        st.switch_page("pages/customer.py")
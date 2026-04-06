import streamlit as st
from services.database_service import get_orders, update_order_status

st.title("Staff Dashboard")
st.caption("View and manage all active orders")

NEXT_STATUS = {
    "pending":     "preparing",
    "preparing": "ready",
    "ready":       "completed",
}

BUTTON_LABELS = {
    "pending":     "Claim — start cooking",
    "preparing": "Mark as ready",
    "ready":       "Confirm pickup — complete",
}

orders = get_orders()

if not orders:
    st.info("No active orders right now.")
    st.stop()

st.subheader(f"Active orders ({len(orders)})")

for order in orders:
    order_id = order["order_id"]
    status   = order["order_status"]

    with st.expander(f"Order #{order_id} — Table {order['table_number']} — {status.upper()}"):
        st.write(f"**Status:** {status}")
        st.write(f"**Table:** {order['table_number']}")
        st.write(f"**Total:** ${order['order_total']}")
        st.write(f"**Placed at:** {order['created_at']}")

        if status in NEXT_STATUS:
            if st.button(BUTTON_LABELS[status], key=f"btn_{order_id}"):
                try:
                    update_order_status(order_id, NEXT_STATUS[status])
                    st.success(f"Order #{order_id} updated to {NEXT_STATUS[status]}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not update order: {e}")
        else:
            st.success("Order complete — no further action needed.")
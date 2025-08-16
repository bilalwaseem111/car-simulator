# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------- Page Config ----------------
st.set_page_config(page_title="Car Differential Simulation", layout="wide")

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #d4fc79, #96e6a1, #a1c4fd, #c2e9fb);
    color: #1a1a1a;
}

/* Animated Heading */
@keyframes glow {
  0% { text-shadow: 0 0 5px #00c6ff, 0 0 10px #0072ff; }
  50% { text-shadow: 0 0 20px #0072ff, 0 0 30px #00c6ff; }
  100% { text-shadow: 0 0 5px #00c6ff, 0 0 10px #0072ff; }
}
h1 {
  font-size: 64px !important;
  font-weight: bold;
  text-align: center;
  animation: glow 2s infinite alternate;
  margin-bottom: 20px;
}

/* Animated Buttons */
div.stButton > button {
    background: linear-gradient(45deg, #6a11cb, #2575fc);
    color: white;
    padding: 12px 30px;
    border-radius: 15px;
    border: none;
    font-size: 18px;
    transition: 0.3s;
}
div.stButton > button:hover {
    transform: scale(1.1);
    background: linear-gradient(45deg, #43cea2, #185a9d);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Heading ----------------
st.markdown("<h1> Car Differential Simulator</h1>", unsafe_allow_html=True)

# ---------------- Sidebar Controls ----------------
st.sidebar.header(" Simulation Controls")
speed = st.sidebar.slider("Engine Speed (RPM)", 500, 5000, 1500, 100)
turn_radius = st.sidebar.slider("Turn Radius (m)", 5, 50, 20, 1)
gear_ratio = st.sidebar.slider("Gear Ratio", 2.0, 6.0, 4.0, 0.1)
time = np.linspace(0, 5, 500)

# ---------------- Calculations ----------------
angular_velocity = (speed / 60) * 2 * np.pi
inner_wheel_speed = angular_velocity * (1 - 1/turn_radius) / gear_ratio
outer_wheel_speed = angular_velocity * (1 + 1/turn_radius) / gear_ratio
torque_inner = inner_wheel_speed * 50
torque_outer = outer_wheel_speed * 50
pressure = np.exp(-((time-2.5)**2)) * 100
stability = np.tanh(time - 2.5)

# ---------------- Results ----------------
st.subheader(" Simulation Results")
st.write(f"**Inner Wheel Speed:** {inner_wheel_speed:.2f} rad/s")
st.write(f"**Outer Wheel Speed:** {outer_wheel_speed:.2f} rad/s")
st.write(f"**Torque on Inner Wheel:** {torque_inner:.2f} Nm")
st.write(f"**Torque on Outer Wheel:** {torque_outer:.2f} Nm")

# ---------------- 2D Gear Visualization ----------------
st.subheader(" Differential Gear Visualization")
theta = np.linspace(0, 2*np.pi, 100)
gear1_x, gear1_y = np.cos(theta), np.sin(theta)
gear2_x, gear2_y = 2 + np.cos(-theta), np.sin(-theta)

fig, ax = plt.subplots(figsize=(6,6))
ax.plot(gear1_x, gear1_y, color="blue", linewidth=2, label="Input Gear")
ax.plot(gear2_x, gear2_y, color="green", linewidth=2, label="Output Gear")
ax.arrow(0, 0, 0.5, 0.5, head_width=0.2, color="blue")
ax.arrow(2, 0, 0.5, -0.5, head_width=0.2, color="green")
ax.set_aspect('equal')
ax.set_title("2D Differential Gear Motion", fontsize=14)
ax.legend()
st.pyplot(fig)

# ---------------- Graphs ----------------
st.subheader(" Real-Time Graphs & Explanations")
col1, col2 = st.columns(2)

# Graph 1 - Wheel Speeds
with col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(time, np.sin(time)*inner_wheel_speed, label="Inner Wheel", color="red")
    ax1.plot(time, np.sin(time)*outer_wheel_speed, label="Outer Wheel", color="blue")
    ax1.set_title("Wheel Speeds over Time")
    ax1.legend()
    st.pyplot(fig1)
    st.info("Inner wheel rotates slower than outer wheel during a turn.")

# Graph 2 - Torque Distribution
with col2:
    fig2, ax2 = plt.subplots()
    ax2.bar(["Inner Wheel", "Outer Wheel"], [torque_inner, torque_outer], color=["red", "blue"])
    ax2.set_title("Torque Distribution")
    st.pyplot(fig2)
    st.info("Torque split helps maintain stability when turning.")

col3, col4 = st.columns(2)
# Graph 3 - Pressure Distribution
with col3:
    fig3, ax3 = plt.subplots()
    ax3.plot(time, pressure, color="purple")
    ax3.set_title("Pressure on Gear Teeth")
    st.pyplot(fig3)
    st.info("Pressure peaks occur when gears engage each other.")

# Graph 4 - Vehicle Stability
with col4:
    fig4, ax4 = plt.subplots()
    ax4.plot(time, stability, color="green")
    ax4.set_title("Vehicle Stability Curve")
    st.pyplot(fig4)
    st.info("Shows how vehicle balance adjusts when wheel speeds differ.")

# ---------------- Button Example ----------------
if st.button(" Update Simulation"):
    st.success("Simulation refreshed with new parameters!")

# ---------------- Footer ----------------
st.markdown("<hr><h3 style='text-align:center;'>Made by Bilal Waseem</h3>", unsafe_allow_html=True)

import streamlit as st
import time
import numpy as np
import plotly.graph_objs as go


def gen_field_coords(theta, phi, ra):
    x = ra * np.sin(theta) * np.cos(phi)
    y = ra * np.sin(theta) * np.sin(phi)
    z = ra * np.cos(theta)
    return x, y, z


def electric_field_lines(ra):

    ch = 1e-12
    k = 8.99e9
    x = np.linspace(-(2*ra), (2*ra), 20)
    y = np.linspace(-(2*ra), (2*ra), 20)
    z = np.linspace(-(2*ra), (2*ra), 20)
    X, Y, Z = np.meshgrid(x, y, z)

    # Calculate the electric field at each point in the grid
    R = np.sqrt(X**2 + Y**2 + Z**2)
    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)
    Ez = np.zeros_like(Z)

    # Create a meshgrid for drawing the sphere outlines
    phi = np.linspace(0, 2 * np.pi, 100)
    theta = np.linspace(0, np.pi, 100)
    phi, theta = np.meshgrid(phi, theta)

    # Calculate spherical coordinates for the outlines of the spheres
    inner_sphere_x = ra * np.sin(theta) * np.cos(phi)
    inner_sphere_y = ra * np.sin(theta) * np.sin(phi)
    inner_sphere_z = ra * np.cos(theta)

    # Create a 3D scatter plot for the spheres producing the electric field
    inner_sphere_outline = go.Scatter3d(
        x=inner_sphere_x.flatten(),
        y=inner_sphere_y.flatten(),
        z=inner_sphere_z.flatten(),
        mode='lines',
        line=dict(width=1, color='white'),
        name=''
    )

    # Calculate electric field outside the central sphere
    outside_sphere = (R >= ra)
    Ex[outside_sphere] = k * ch * X[outside_sphere] / (R[outside_sphere]**3 + 1e-10)  # Added a small value to avoid division by zero
    Ey[outside_sphere] = k * ch * Y[outside_sphere] / (R[outside_sphere]**3 + 1e-10)
    Ez[outside_sphere] = k * ch * Z[outside_sphere] / (R[outside_sphere]**3 + 1e-10)

    # Create an interactive 3D plot
    fig = go.Figure(data=go.Cone(x=X.flatten(), y=Y.flatten(), z=Z.flatten(), u=Ex.flatten(), v=Ey.flatten(), w=Ez.flatten(), sizemode="absolute", colorbar=dict(title="Electric Field")))
    fig.update_layout(scene=dict(aspectmode="data"))
    fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=1)))

    # Set axis labels and title
    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
    fig.update_layout(title='Interactive Electric Field Vectors Outside a Uniform Spherical Charge Distribution')

    # Add the central charge outlines
    fig.add_trace(inner_sphere_outline)

    return fig



st.set_page_config(page_title="Plotting interference", page_icon="⚡️")

st.markdown("# Simple Interference on a sphere")
st.sidebar.header("Visualise on sphere")
st.write(
    """Channel 1 + Channel 2"""
)
s_to_p = st.number_input("Seconds", value=1)
rad = st.number_input("Radius of the model (m)", value=0.2)

## Coords pair 1
p1aph = st.number_input("Phi for P1A", value=1)
p1ath = st.number_input("Theta for P1A", value=1)
p1bph = st.number_input("Phi for P1B", value=1)
p1vph = st.number_input("Theta for P1B", value=1)

# Coords pair 2
p2aph = st.number_input("Phi for P2A", value=1)
p2ath = st.number_input("Theta for P2A", value=1)
p2bph = st.number_input("Phi for P2B", value=1)
p2bth = st.number_input("Theta for P2B", value=1)

fig = electric_field_lines(rad)

st.plotly_chart(fig)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
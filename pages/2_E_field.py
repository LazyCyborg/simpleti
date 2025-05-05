import streamlit as st
import time
import numpy as np
import plotly.graph_objects as go


def gen_field_coords(theta, phi, ra):
    x = ra * np.sin(theta) * np.cos(phi)
    y = ra * np.sin(theta) * np.sin(phi)
    z = ra * np.cos(theta)
    return x, y, z


def charge(theta, phi, charge):
    k = 8.99e9  ## Coulomb's constant I think? I stole it from some field modelling
    ra = 0.1  # Radius of sphere

    ## Charges
    q_p = charge * 1e-10

    ## Coordinates for electrode
    p_theta = theta
    p_phi = phi

    x_p = ra * np.sin(p_theta) * np.cos(p_phi)
    y_p = ra * np.sin(p_theta) * np.sin(p_phi)
    z_p = ra * np.cos(p_theta)

    x_grid = np.linspace(-0.5, 0.5, 20)
    y_grid = np.linspace(-0.5, 0.5, 20)
    z_grid = np.linspace(-0.5, 0.5, 20)

    X, Y, Z = np.meshgrid(x_grid, y_grid, z_grid)

    ## Displacement coordinates
    dx_p = X - x_p
    dy_p = Y - y_p
    dz_p = Z - z_p

    ## Displacement as a single coordinate
    r_p_sq = dx_p ** 2 + dy_p ** 2 + dz_p ** 2
    r_p = np.sqrt(r_p_sq)

    ## Unit direction vectors (scalars?)
    r_p_safe = r_p + 1e-10

    unit_dir_x_p = dx_p / r_p_safe
    unit_dir_y_p = dy_p / r_p_safe
    unit_dir_z_p = dz_p / r_p_safe

    ## Field contributions
    magnitude_p = k * q_p / (r_p_sq + 1e-10)

    Ex = magnitude_p * unit_dir_x_p
    Ey = magnitude_p * unit_dir_y_p
    Ez = magnitude_p * unit_dir_z_p

    return X, Y, Z, Ex, Ey, Ez, magnitude_p, x_p, y_p, z_p


def plot_charges(ta, pa, tb, pb, tc, pc, td, pd):

    ## I just chose a, b,c and d as:
    # a = + pair 1
    # b = - pair 1
    # c = + pair 2
    # d = - pair 2

    ## Convert from degrees to rads
    ta = np.deg2rad(ta)
    pa = np.deg2rad(pa)

    tb = np.deg2rad(tb)
    pb = np.deg2rad(pb)

    tc = np.deg2rad(tc)
    pc = np.deg2rad(pc)

    td = np.deg2rad(td)
    pd = np.deg2rad(pd)

    Xa, Ya, Za, Exa, Eya, Eza, magnitude_a, x_a, y_a, z_a = charge(theta=ta, phi=pa, charge=1)

    Xb, Yb, Zb, Exb, Eyb, Ezb, magnitude_b, x_b, y_b, z_b = charge(theta=tb, phi=pb, charge=-1)

    Xc, Yc, Zc, Exc, Eyc, Ezc, magnitude_c, x_c, y_c, z_c = charge(theta=tc, phi=pc, charge=1)

    Xd, Yd, Zd, Exd, Eyd, Ezd, magnitude_d, x_d, y_d, z_d = charge(theta=td, phi=pd, charge=-1)

    E_total_x = Exa + Exb + Exc + Exd
    E_total_y = Eya + Eyb + Eyc + Eyd
    E_total_z = Eza + Ezb + Ezc + Ezd

    E_magnitude = np.sqrt(E_total_x ** 2 + E_total_y ** 2 + E_total_z ** 2)

    print(f"E_magnitude: Min={np.min(E_magnitude):.2e}, Max={np.max(E_magnitude):.2e}, Mean={np.mean(E_magnitude):.2e}")

    x_grid = np.linspace(-0.5, 0.5, 20)
    y_grid = np.linspace(-0.5, 0.5, 20)
    z_grid = np.linspace(-0.5, 0.5, 20)

    X, Y, Z = np.meshgrid(x_grid, y_grid, z_grid)

    d = np.pi / 32

    theta, phi = np.mgrid[0:np.pi + d:d, 0:2 * np.pi:d]
    # Convert to Cartesian coordinates
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    ra = 0.1
    x = ra * x
    y = ra * y
    z = ra * z

    # print(x.shape, y.shape, z.shape)  # (33, 64) (33, 64) (33, 64)
    points = np.vstack([x.ravel(), y.ravel(), z.ravel()])
    # print(points.shape)  # (3, 2112)
    x, y, z = points
    # print(x.shape, y.shape, z.shape)  # (2112,) (2112,) (2112,)

    fig = go.Figure(data=[
        go.Mesh3d(x=x, y=y, z=z, color='lightblue', opacity=0.50, alphahull=0)
    ])
    # Add marker for positive charge
    fig.add_trace(go.Scatter3d(
        x=[x_a],
        y=[y_a],
        z=[z_a],
        mode='markers',
        marker=dict(size=10, color='red'),
        name='P1A (+)'
    ))

    # Add marker for negative charge
    fig.add_trace(go.Scatter3d(
        x=[x_b],
        y=[y_b],
        z=[z_b],
        mode='markers',
        marker=dict(size=10, color='red'),
        name='P1B (-)'
    ))

    # Add marker for negative charge
    fig.add_trace(go.Scatter3d(
        x=[x_c],
        y=[y_c],
        z=[z_c],
        mode='markers',
        marker=dict(size=10, color='blue'),
        name='P2A (+)'
    ))

    # Add marker for positive charge
    fig.add_trace(go.Scatter3d(
        x=[x_d],
        y=[y_d],
        z=[z_d],
        mode='markers',
        marker=dict(size=10, color='blue'),
        name='P2B (-)'
    ))

    # Add electric field vectors
    fig.add_trace(go.Cone(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        u=E_total_x.flatten(),
        v=E_total_y.flatten(),
        w=E_total_z.flatten(),
        sizemode="absolute",
        sizeref=500,
        anchor="tail",
        colorbar=dict(title='E Field Mag (V/m)'),
        name='E Field'
    ))

    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        scene=dict(
            aspectmode="cube",
            xaxis=dict(range=[-0.3, 0.3], title="X (m)"),
            yaxis=dict(range=[-0.3, 0.3], title="Y (m)"),
            zaxis=dict(range=[-0.3, 0.3], title="Z (m)"),
        ),
        title="Electric Field from Two Charges near a Sphere",
        margin=dict(l=30, r=30, b=30, t=40)
    )

    return fig


st.set_page_config(page_title="Plotting E fields", page_icon="⚡️")

st.markdown("# Simple E fields on a sphere")
st.sidebar.header("Visualise on sphere")
st.write(
    """Channel 1 + Channel 2"""
)
## Coords pair 1

col1, col2, = st.columns(2)

with col1:

    st.header("P1A and P1B coordinates")

    ta = st.slider("Theta for P1A", value=45, min_value=0, max_value=180)
    pa = st.slider("Phi for P1A", value=180, min_value=0, max_value=360)
    tb = st.slider("Theta for P1B", value=180, min_value=0, max_value=180)
    pb = st.slider("Phi for P1B", value=45, min_value=0, max_value=360)

with col2:

    st.header("P2A and P2B coordinates")
    # Coords pair 2
    tc = st.slider("Theta for P2A", value=90, min_value=0, max_value=180)
    pc = st.slider("Phi for P2A", value=-0, min_value=0, max_value=360)
    td = st.slider("Theta for P2B", value=0, min_value=0, max_value=180)
    pd = st.slider("Phi for P2B", value=90, min_value=0, max_value=360)


fig = plot_charges(ta, pa, tb, pb, tc, pc, td, pd)

st.plotly_chart(fig)

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")

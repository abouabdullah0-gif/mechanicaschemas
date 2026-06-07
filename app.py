import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(page_title="Mechanica Schema Analyzer", layout="wide")
st.title("Mechanica Schema Analyzer")

uploaded = st.file_uploader("Upload een afbeelding van je schema", type=["png", "jpg", "jpeg", "webp"])

st.markdown("### Algemene liggergegevens")
L = st.number_input("Lengte ligger L (m)", min_value=0.1, value=10.0, step=0.1)
n_point = st.number_input("Aantal puntlasten", min_value=0, value=1, step=1)
n_dist = st.number_input("Aantal verdeelde lasten", min_value=0, value=0, step=1)
n_axial = st.number_input("Aantal normaallasten", min_value=0, value=0, step=1)

col_img, col_info = st.columns([1.2, 1])

with col_img:
    if uploaded is not None:
        uploaded.seek(0)
        img = Image.open(uploaded)
        st.image(img, caption="Geüploade afbeelding", use_container_width=True)
    else:
        st.info("Upload een afbeelding om die hier te zien.")

with col_info:
    st.markdown("### Steunpunten")
    xA = st.number_input("Steunpunt A op x (m)", min_value=0.0, max_value=float(L), value=0.0, step=0.1)
    xB = st.number_input("Steunpunt B op x (m)", min_value=0.0, max_value=float(L), value=float(L), step=0.1)

    st.markdown("### Puntlasten")
    point_loads = []
    for i in range(int(n_point)):
        st.write(f"Puntlast {i+1}")
        x = st.number_input(f"x{i+1} (m)", min_value=0.0, max_value=float(L), value=float(L)/2, step=0.1, key=f"px_{i}")
        p = st.number_input(f"P{i+1} (kN, omlaag positief)", value=10.0, step=0.5, key=f"pp_{i}")
        point_loads.append((x, p))

    st.markdown("### Verdeelde lasten")
    dist_loads = []
    for i in range(int(n_dist)):
        st.write(f"Verdeelde last {i+1}")
        x1 = st.number_input(f"x1_{i+1} (m)", min_value=0.0, max_value=float(L), value=0.0, step=0.1, key=f"dx1_{i}")
        x2 = st.number_input(f"x2_{i+1} (m)", min_value=0.0, max_value=float(L), value=float(L), step=0.1, key=f"dx2_{i}")
        w = st.number_input(f"w{i+1} (kN/m, omlaag positief)", value=0.0, step=0.1, key=f"dw_{i}")
        dist_loads.append((min(x1, x2), max(x1, x2), w))

    st.markdown("### Normaallasten")
    axial_loads = []
    for i in range(int(n_axial)):
        st.write(f"Normaallast {i+1}")
        x = st.number_input(f"xa{i+1} (m)", min_value=0.0, max_value=float(L), value=float(L)/2, step=0.1, key=f"ax_{i}")
        n = st.number_input(f"N{i+1} (kN, trek positief)", value=0.0, step=0.5, key=f"an_{i}")
        axial_loads.append((x, n))

def reactions_simply_supported(L, point_loads, dist_loads):
    total_down = sum(p for _, p in point_loads) + sum(w * (x2 - x1) for x1, x2, w in dist_loads)
    moment_about_A = sum(p * x for x, p in point_loads) + sum((w * (x2 - x1)) * (x1 + (x2 - x1) / 2) for x1, x2, w in dist_loads)
    RB = moment_about_A / L if L != 0 else 0
    RA = total_down - RB
    return RA, RB

def axial_reactions_simple(xA, xB, axial_loads):
    NA = 0.0
    NB = 0.0
    if len(axial_loads) > 0:
        NA = -sum(n for _, n in axial_loads) / 2
        NB = -sum(n for _, n in axial_loads) / 2
    return NA, NB

def build_diagrams(L, point_loads, dist_loads, axial_loads, npts=600):
    x = np.linspace(0, L, npts)
    RA, RB = reactions_simply_supported(L, point_loads, dist_loads)
    NA, NB = axial_reactions_simple(xA, xB, axial_loads)

    V = np.zeros_like(x)
    M = np.zeros_like(x)
    N = np.zeros_like(x)

    for i, xi in enumerate(x):
        shear = RA
        moment = RA * xi
        axial = NA

        for xp, p in point_loads:
            if xi >= xp:
                shear -= p
                moment -= p * (xi - xp)

        for x1, x2, w in dist_loads:
            if xi > x1:
                xe = min(xi, x2)
                if xe > x1:
                    load = w * (xe - x1)
                    centroid = x1 + (xe - x1) / 2
                    shear -= load
                    moment -= load * (xi - centroid)

        for xa, n in axial_loads:
            if xi >= xa:
                axial += n

        V[i] = shear
        M[i] = moment
        N[i] = axial

    return x, N, V, M, RA, RB, NA, NB

if st.button("Bereken en toon lijnen"):
    x, N, V, M, RA, RB, NA, NB = build_diagrams(L, point_loads, dist_loads, axial_loads)

    st.success("Berekening klaar.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("RA (kN)", f"{RA:.2f}")
    c2.metric("RB (kN)", f"{RB:.2f}")
    c3.metric("NA (kN)", f"{NA:.2f}")
    c4.metric("NB (kN)", f"{NB:.2f}")

    figN = go.Figure()
    figN.add_trace(go.Scatter(x=x, y=N, mode="lines", name="Normaalkracht N(x)"))
    figN.add_hline(y=0, line_width=1, line_color="black")
    figN.update_layout(title="Normaalkrachtlijn", xaxis_title="x (m)", yaxis_title="N (kN)", height=350)

    figV = go.Figure()
    figV.add_trace(go.Scatter(x=x, y=V, mode="lines", name="Dwarskracht V(x)"))
    figV.add_hline(y=0, line_width=1, line_color="black")
    figV.update_layout(title="Dwarskrachtenlijn", xaxis_title="x (m)", yaxis_title="V (kN)", height=350)

    figM = go.Figure()
    figM.add_trace(go.Scatter(x=x, y=M, mode="lines", name="Moment M(x)"))
    figM.add_hline(y=0, line_width=1, line_color="black")
    figM.update_layout(title="Momente­nlijn", xaxis_title="x (m)", yaxis_title="M (kNm)", height=350)

    st.plotly_chart(figN, use_container_width=True)
    st.plotly_chart(figV, use_container_width=True)
    st.plotly_chart(figM, use_container_width=True)


import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.title("Visualisasi Algoritma Kruskal")

st.markdown("""
Aplikasi ini memvisualisasikan cara kerja *Algoritma Kruskal* dalam mencari Minimum Spanning Tree (MST) dari graf berbobot.
""")

# Input jumlah simpul dan sisi
num_nodes = st.number_input("Jumlah simpul", min_value=2, value=5)
num_edges = st.number_input("Jumlah sisi", min_value=1, value=7)

# Input daftar sisi
st.subheader("Input Sisi dan Bobot")
edges = []
for i in range(int(num_edges)):
    col1, col2, col3 = st.columns(3)
    with col1:
        u = st.text_input(f"Node awal sisi {i+1}", value=f"{i%num_nodes}")
    with col2:
        v = st.text_input(f"Node akhir sisi {i+1}", value=f"{(i+1)%num_nodes}")
    with col3:
        w = st.number_input(f"Bobot sisi {i+1}", value=1, key=f"w_{i}")
    edges.append((u, v, w))

# Buat graf dari input
G = nx.Graph()
G.add_weighted_edges_from(edges)

# Tampilkan graf awal
st.subheader("Graf Awal")
fig, ax = plt.subplots()
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, ax=ax)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
st.pyplot(fig)

# Kruskal Algorithm
def kruskal_mst(edges):
    sorted_edges = sorted(edges, key=lambda x: x[2])
    parent = {}
    mst = []

    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(u, v):
        parent[find(u)] = find(v)

    nodes = set([u for u, v, _ in edges] + [v for u, v, _ in edges])
    for node in nodes:
        parent[node] = node

    steps = []
    for u, v, w in sorted_edges:
        if find(u) != find(v):
            mst.append((u, v, w))
            union(u, v)
            steps.append(list(mst))  # copy of current MST

    return mst, steps

if st.button("Jalankan Kruskal"):
    # Jalankan Kruskal dan ambil hasilnya
    sorted_edges = sorted(edges, key=lambda x: x[2])
    mst_result, step_list = kruskal_mst(edges)

    # Tampilkan tabel pengurutan bobot
    st.subheader("Tabel Pengurutan Bobot Edge")
    df_edges = pd.DataFrame(sorted_edges, columns=["Node Awal", "Node Akhir", "Bobot"])
    st.table(df_edges)


    st.subheader("Langkah-langkah Pemilihan Edge")
    for i, step in enumerate(step_list):
        st.markdown(f"*Langkah {i+1}*: Tambahkan edge {step[-1]}")
        fig, ax = plt.subplots()
        temp_G = nx.Graph()
        temp_G.add_weighted_edges_from(step)
        nx.draw(G, pos, with_labels=True, node_color="lightgray", ax=ax)
        nx.draw_networkx_edges(temp_G, pos, edge_color='red', width=2, ax=ax)
        nx.draw_networkx_edge_labels(temp_G, pos, edge_labels={(u, v): w for u, v, w in step}, ax=ax)
        st.pyplot(fig)

    st.success("Minimum Spanning Tree (MST) selesai dibentuk!")
    total_weight = sum(w for _, _, w in mst_result)
    st.write(f"*Total Bobot MST: {total_weight}*")
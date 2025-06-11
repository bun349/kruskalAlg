import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# Judul aplikasi
st.title("Visualisasi Algoritma Kruskal")

# Deskripsi singkat algoritma
st.markdown("""
Aplikasi ini memvisualisasikan cara kerja *Algoritma Kruskal* dalam mencari Minimum Spanning Tree (MST) dari graf berbobot.
""")

# Input jumlah simpul dan sisi
num_nodes = st.number_input("Jumlah simpul", min_value=2, value=5)
num_edges = st.number_input("Jumlah sisi", min_value=1, value=7)

# Input daftar sisi (edge) oleh pengguna
st.subheader("Input Sisi dan Bobot")
edges = []
for i in range(int(num_edges)):
    # Bagi input ke dalam 3 kolom: node awal, node akhir, dan bobot
    col1, col2, col3 = st.columns(3)
    with col1:
        u = st.text_input(f"Node awal sisi {i+1}", value=f"{i%num_nodes}")
    with col2:
        v = st.text_input(f"Node akhir sisi {i+1}", value=f"{(i+1)%num_nodes}")
    with col3:
        w = st.number_input(f"Bobot sisi {i+1}", value=1, key=f"w_{i}")
    edges.append((u, v, w))  # Simpan edge dalam list

# Buat graf dari input (hanya untuk visualisasi)
G = nx.Graph()
G.add_weighted_edges_from(edges)

# Visualisasi graf awal
st.subheader("Graf Awal")
fig, ax = plt.subplots()
pos = nx.spring_layout(G, seed=42)  # Layout posisi simpul
nx.draw(G, pos, with_labels=True, ax=ax)  # Gambar simpul dan sisi
edge_labels = nx.get_edge_attributes(G, 'weight')  # Ambil label bobot
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)  # Tampilkan label bobot
st.pyplot(fig)

# -------------------------------
# Algoritma Kruskal manual (tanpa library eksternal untuk logika)
# -------------------------------
def kruskal_manual(edges):
    # Urutkan sisi berdasarkan bobot secara ascending
    sorted_edges = sorted(edges, key=lambda x: x[2])

    # Inisialisasi struktur union-find
    parent = {}

    # Fungsi untuk mencari root dari sebuah node (find)
    def find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]  # Path compression
            node = parent[node]
        return node

    # Fungsi untuk menyatukan dua set (union)
    def union(u, v):
        parent[find(u)] = find(v)

    # Buat himpunan semua node unik
    nodes = set()
    for u, v, _ in edges:
        nodes.add(u)
        nodes.add(v)

    # Setiap node jadi parent dirinya sendiri (init)
    for node in nodes:
        parent[node] = node

    mst = []      # Menyimpan hasil MST
    steps = []    # Menyimpan langkah-langkah pembentukan MST

    # Proses Kruskal
    for u, v, w in sorted_edges:
        # Jika node tidak membentuk siklus, tambahkan ke MST
        if find(u) != find(v):
            mst.append((u, v, w))
            union(u, v)
            steps.append(list(mst))  # Salin snapshot MST saat ini

    return mst, steps, sorted_edges  # Return hasil akhir MST dan langkah-langkah

# -------------------------------
# Jalankan saat tombol diklik
# -------------------------------
if st.button("Jalankan Kruskal"):
    mst_result, step_list, sorted_edges = kruskal_manual(edges)

    # Tampilkan tabel hasil pengurutan sisi
    st.subheader("Tabel Pengurutan Bobot Edge")
    df_edges = pd.DataFrame(sorted_edges, columns=["Node Awal", "Node Akhir", "Bobot"])
    st.table(df_edges)  # Lebih ringkas daripada st.dataframe

    # Visualisasi langkah-langkah pembentukan MST
    st.subheader("Langkah-langkah Pemilihan Edge")
    for i, step in enumerate(step_list):
        st.markdown(f"*Langkah {i+1}*: Tambahkan edge {step[-1]}")
        fig, ax = plt.subplots()

        # Buat graf dari edge-edge saat ini
        temp_G = nx.Graph()
        temp_G.add_weighted_edges_from(step)

        # Gambar graf dasar (berwarna abu)
        nx.draw(G, pos, with_labels=True, node_color="lightgray", ax=ax)

        # Gambar edge yang sudah dipilih berwarna merah
        nx.draw_networkx_edges(temp_G, pos, edge_color='red', width=2, ax=ax)

        # Label bobot pada MST saat ini
        nx.draw_networkx_edge_labels(temp_G, pos, edge_labels={(u, v): w for u, v, w in step}, ax=ax)

        st.pyplot(fig)

    # Tampilkan hasil akhir MST
    st.success("Minimum Spanning Tree (MST) selesai dibentuk!")
    total_weight = sum(w for _, _, w in mst_result)
    st.write(f"*Total Bobot MST: {total_weight}*")

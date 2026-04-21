import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import streamlit as st

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Brazil Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
/* Sidebar hijau Brazil */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14532d 0%, #15803d 50%, #16a34a 100%);
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Navigasi style seperti menu item - tanpa radio button */
[data-testid="stSidebar"] .stRadio > div {
    gap: 4px;
}
[data-testid="stSidebar"] .stRadio label {
    background-color: rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 10px 16px;
    transition: background 0.2s;
    cursor: pointer;
    display: flex !important;
    align-items: center;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background-color: rgba(255,255,255,0.25);
}
/* Sembunyikan radio button bulat */
[data-testid="stSidebar"] .stRadio label > div:first-child {
    display: none !important;
}
/* Navigasi yang dipilih lebih terang */
[data-testid="stSidebar"] .stRadio [data-checked="true"] label {
    background-color: rgba(255,255,255,0.3) !important;
    font-weight: bold;
}

/* Slider warna kuning */
[data-testid="stSlider"] .st-emotion-cache-1gv3huu {
    background: #EAB308 !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #EAB308 !important;
    border-color: #EAB308 !important;
}
div[data-baseweb="slider"] > div > div > div {
    background: #EAB308 !important;
}
div[data-baseweb="slider"] [role="slider"] {
    background-color: #EAB308 !important;
    border-color: #CA8A04 !important;
}
div[data-testid="stSlider"] div[data-baseweb="slider"] div {
    background: #EAB308 !important;
}

/* Tabel header hijau muda */
thead tr th {
    background-color: #dcfce7 !important;
    color: #14532d !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard/main_data.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df_main = load_data()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding:20px 0 10px 0;'>
    <div style='font-size:60px;'>🛍️</div>
    <h2 style='color:white; margin:4px 0; font-size:18px;'>E-Commerce Brazil</h2>
    <p style='color:rgba(255,255,255,0.8); font-size:12px; margin:0;'>Meilani Bulandari Hasibuan</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigasi",
    ["🏠 Overview", "💳 Metode Pembayaran", "🗺️ Pendapatan per Wilayah", "📦 Clustering Seller"]
)

st.sidebar.markdown("---")
year_filter = st.sidebar.multiselect(
    "Filter Tahun",
    options=[2017, 2018],
    default=[2017, 2018]
)

df_filtered = df_main[df_main['order_purchase_timestamp'].dt.year.isin(year_filter)]

# Warna hijau Brazil
colors_green = ['#14532d', '#15803d', '#22c55e', '#86efac']

# ══════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    # Banner hijau di paling atas seperti referensi
    total_pendapatan = df_filtered['payment_value'].sum() / 1e6
    total_orders     = df_filtered['order_id'].nunique()
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #14532d, #22c55e);
                padding: 28px 32px; border-radius: 16px; margin-bottom: 24px;
                display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <p style='color:rgba(255,255,255,0.8); margin:0; font-size:14px;'>Selamat datang di</p>
            <h1 style='color:white; margin:6px 0; font-size:26px;'>🛍️ E-Commerce Brazil Dashboard</h1>
            <p style='color:rgba(255,255,255,0.85); margin:0; font-size:13px;'>
                Analisis transaksi Olist Dataset — Periode 2017–2018
            </p>
        </div>
        <div style='text-align:right;'>
            <p style='color:rgba(255,255,255,0.75); margin:0; font-size:13px;'>Total Pendapatan</p>
            <h2 style='color:white; margin:4px 0; font-size:34px; font-weight:bold;'>
                R${total_pendapatan:.2f}M
            </h2>
            <p style='color:rgba(255,255,255,0.75); margin:0; font-size:12px;'>
                dari {total_orders:,} orders
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🧾 Total Orders", f"{df_filtered['order_id'].nunique():,}")
    with col2:
        st.metric("💰 Total Pendapatan", f"R${df_filtered['payment_value'].sum()/1e6:.2f}M")
    with col3:
        st.metric("🏪 Jumlah Seller", f"{df_filtered['seller_id'].nunique():,}")
    with col4:
        st.metric("💳 Metode Pembayaran", f"{df_filtered['payment_type'].nunique()}")

    st.markdown("---")
    st.markdown("### 📊 Tren Transaksi Bulanan")

    monthly = df_filtered.copy()
    monthly['month'] = monthly['order_purchase_timestamp'].dt.to_period('M').astype(str)
    monthly_agg = monthly.groupby('month')['payment_value'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 4), facecolor='#F8F9FA')
    ax.set_facecolor('#FFFFFF')
    ax.plot(monthly_agg['month'], monthly_agg['payment_value'] / 1e3,
            color='#15803d', linewidth=2.5, marker='o', markersize=5)
    ax.fill_between(monthly_agg['month'], monthly_agg['payment_value'] / 1e3,
                    alpha=0.15, color='#22c55e')
    ax.set_title('Total Nilai Transaksi per Bulan', fontsize=12, fontweight='bold', color='#1a1a2e')
    ax.set_ylabel('Total Transaksi (Ribu R$)', fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R${x:.0f}K'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

# ══════════════════════════════════════════════════════════════
# PAGE: METODE PEMBAYARAN
# ══════════════════════════════════════════════════════════════
elif page == "💳 Metode Pembayaran":
    st.title("💳 Analisis Metode Pembayaran")
    st.markdown("**Pertanyaan:** Bagaimana perbandingan total nilai transaksi dan rata-rata cicilan antar metode pembayaran pada periode 2017-2018?")
    st.markdown("---")

    payment_stats = df_filtered.groupby('payment_type').agg(
        total_transaksi=('order_id', 'nunique'),
        total_nilai=('payment_value', 'sum'),
        rata_nilai=('payment_value', 'mean'),
        rata_cicilan=('payment_installments', 'mean')
    ).reset_index().sort_values('total_nilai', ascending=False).round(2)

    labels_map = {'credit_card': 'Credit Card', 'boleto': 'Boleto',
                  'voucher': 'Voucher', 'debit_card': 'Debit Card'}
    payment_stats['label'] = payment_stats['payment_type'].map(labels_map)

    col1, col2, col3, col4 = st.columns(4)
    for i, row in enumerate(payment_stats.itertuples()):
        cols = [col1, col2, col3, col4]
        with cols[i]:
            st.metric(row.label, f"R${row.total_nilai/1e6:.2f}M",
                      delta=f"avg cicilan {row.rata_cicilan:.1f}x")

    st.markdown("---")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor='#F8F9FA')
    fig.suptitle('Perbandingan Metode Pembayaran (2017-2018)',
                 fontsize=13, fontweight='bold', color='#1a1a2e')

    ax1 = axes[0]
    bars1 = ax1.bar(payment_stats['label'], payment_stats['total_nilai'] / 1e6,
                    color=colors_green, edgecolor='white', linewidth=1.5, zorder=3)
    ax1.set_title('Total Nilai Transaksi', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Total Transaksi (Juta R$)', fontsize=10)
    ax1.set_xlabel('Metode Pembayaran', fontsize=10)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R${x:.1f}M'))
    ax1.set_facecolor('#FFFFFF')
    ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax1.spines[['top', 'right']].set_visible(False)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.1,
                 f'R${h:.1f}M', ha='center', va='bottom', fontsize=9,
                 fontweight='bold', color='#1a1a2e')

    ax2 = axes[1]
    bars2 = ax2.bar(payment_stats['label'], payment_stats['rata_cicilan'],
                    color=colors_green, edgecolor='white', linewidth=1.5, zorder=3)
    ax2.set_title('Rata-rata Jumlah Cicilan', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Rata-rata Cicilan', fontsize=10)
    ax2.set_xlabel('Metode Pembayaran', fontsize=10)
    ax2.set_facecolor('#FFFFFF')
    ax2.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax2.spines[['top', 'right']].set_visible(False)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 0.05,
                 f'{h:.1f}x', ha='center', va='bottom', fontsize=9,
                 fontweight='bold', color='#1a1a2e')

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("### 📋 Tabel Detail")
    payment_stats_display = payment_stats[['label', 'total_transaksi', 'total_nilai', 'rata_nilai', 'rata_cicilan']].copy()
    payment_stats_display.columns = ['Metode Pembayaran', 'Jumlah Transaksi', 'Total Nilai (R$)', 'Rata-rata Nilai (R$)', 'Rata-rata Cicilan']
    payment_stats_display = payment_stats_display.set_index('Metode Pembayaran')
    st.dataframe(payment_stats_display.style.format({
        'Total Nilai (R$)': 'R${:,.2f}',
        'Rata-rata Nilai (R$)': 'R${:,.2f}',
        'Rata-rata Cicilan': '{:.2f}x'
    }).set_table_styles([{
        'selector': 'thead th',
        'props': [('background-color', '#dcfce7'), ('color', '#14532d'), ('font-weight', 'bold')]
    }]), use_container_width=True)

    st.success("**Insight:** Credit Card mendominasi total nilai transaksi (R$12.5M, ~79%) dengan rata-rata cicilan 3.5x. Platform disarankan memperkuat kemitraan dengan penyedia credit card dan menawarkan promo cicilan 0%.")

# ══════════════════════════════════════════════════════════════
# PAGE: PENDAPATAN PER WILAYAH
# ══════════════════════════════════════════════════════════════
elif page == "🗺️ Pendapatan per Wilayah":
    st.title("🗺️ Distribusi Pendapatan Seller per Negara Bagian")
    st.markdown("**Pertanyaan:** Bagaimana distribusi total pendapatan seller berdasarkan negara bagian pada periode 2017-2018?")
    st.markdown("---")

    state_stats = df_filtered.groupby('seller_state').agg(
        jumlah_seller=('seller_id', 'nunique'),
        total_pendapatan=('payment_value', 'sum'),
        rata_pendapatan=('payment_value', 'mean')
    ).reset_index().sort_values('total_pendapatan', ascending=False).round(2)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Negara Bagian Tertinggi", state_stats.iloc[0]['seller_state'],
                  delta=f"R${state_stats.iloc[0]['total_pendapatan']/1e6:.1f}M")
    with col2:
        st.metric("Total Negara Bagian", f"{len(state_stats)}")
    with col3:
        st.metric("Rata-rata per State", f"R${state_stats['total_pendapatan'].mean()/1e3:.1f}K")

    st.markdown("---")

    top_n = st.slider("Tampilkan Top N Negara Bagian", min_value=5, max_value=len(state_stats), value=15)
    p2 = state_stats.head(top_n).sort_values('total_pendapatan', ascending=True)
    colors_p2 = plt.cm.Greens(np.linspace(0.3, 0.9, len(p2)))

    fig, ax = plt.subplots(figsize=(11, max(5, top_n * 0.4)), facecolor='#F8F9FA')
    ax.set_facecolor('#FFFFFF')
    bars = ax.barh(p2['seller_state'], p2['total_pendapatan'] / 1e6,
                   color=colors_p2, edgecolor='white', linewidth=0.8, zorder=3)
    ax.set_title(f'Top {top_n} Negara Bagian berdasarkan Total Pendapatan Seller',
                 fontsize=12, fontweight='bold', color='#1a1a2e', pad=12)
    ax.set_xlabel('Total Pendapatan (Juta R$)', fontsize=10)
    ax.set_ylabel('Negara Bagian', fontsize=10)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R${x:.1f}M'))
    ax.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    ax.spines[['top', 'right']].set_visible(False)
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.05, bar.get_y() + bar.get_height()/2,
                f'R${w:.1f}M', va='center', fontsize=8, color='#1a1a2e')
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("### 📋 Tabel Detail")
    state_display = state_stats.copy()
    state_display.columns = ['Negara Bagian', 'Jumlah Seller', 'Total Pendapatan (R$)', 'Rata-rata Pendapatan (R$)']
    state_display = state_display.set_index('Negara Bagian')
    st.dataframe(state_display.style.format({
        'Total Pendapatan (R$)': 'R${:,.2f}',
        'Rata-rata Pendapatan (R$)': 'R${:,.2f}'
    }).set_table_styles([{
        'selector': 'thead th',
        'props': [('background-color', '#dcfce7'), ('color', '#14532d'), ('font-weight', 'bold')]
    }]), use_container_width=True)

    st.success("**Insight:** São Paulo (SP) mendominasi dengan R$13.3M (~65% total). Terdapat kesenjangan besar antara SP dengan negara bagian lain, menunjukkan peluang ekspansi bisnis yang besar.")

# ══════════════════════════════════════════════════════════════
# PAGE: CLUSTERING SELLER
# ══════════════════════════════════════════════════════════════
elif page == "📦 Clustering Seller":
    st.title("📦 Clustering Seller Berdasarkan Performa")
    st.markdown("Pengelompokan seller ke dalam kategori **Low**, **Medium**, dan **High Performer** menggunakan teknik Binning berdasarkan total pendapatan.")
    st.markdown("---")

    seller_perf = df_filtered.groupby('seller_id').agg(
        total_revenue=('payment_value', 'sum'),
        total_orders=('order_id', 'nunique'),
        total_items=('order_item_id', 'count'),
        avg_order_value=('payment_value', 'mean')
    ).reset_index()

    q33 = seller_perf['total_revenue'].quantile(0.33)
    q66 = seller_perf['total_revenue'].quantile(0.66)

    def categorize(rev):
        if rev <= q33:
            return 'Low Performer'
        elif rev <= q66:
            return 'Medium Performer'
        else:
            return 'High Performer'

    seller_perf['category'] = seller_perf['total_revenue'].apply(categorize)

    col1, col2, col3 = st.columns(3)
    with col1:
        n_low = (seller_perf['category'] == 'Low Performer').sum()
        st.metric("🔵 Low Performer", f"{n_low:,} seller", delta=f"<= R${q33:,.0f}")
    with col2:
        n_med = (seller_perf['category'] == 'Medium Performer').sum()
        st.metric("🔷 Medium Performer", f"{n_med:,} seller", delta=f"R${q33:,.0f} – R${q66:,.0f}")
    with col3:
        n_high = (seller_perf['category'] == 'High Performer').sum()
        st.metric("🏆 High Performer", f"{n_high:,} seller", delta=f"> R${q66:,.0f}")

    st.markdown("---")

    category_order  = ['Low Performer', 'Medium Performer', 'High Performer']
    colors_cluster  = ['#86efac', '#22c55e', '#15803d']
    count_data      = seller_perf['category'].value_counts().reindex(category_order)
    avg_rev_data    = seller_perf.groupby('category')['total_revenue'].mean().reindex(category_order)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor='#F8F9FA')
    fig.suptitle('Clustering Seller Berdasarkan Performa Pendapatan (2017-2018)',
                 fontsize=12, fontweight='bold', color='#1a1a2e')

    ax1 = axes[0]
    bars1 = ax1.bar(category_order, count_data.values, color=colors_cluster,
                    edgecolor='white', linewidth=1.5, zorder=3)
    ax1.set_title('Jumlah Seller per Kategori', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Jumlah Seller', fontsize=10)
    ax1.set_facecolor('#FFFFFF')
    ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax1.spines[['top', 'right']].set_visible(False)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 5,
                 f'{int(h):,}', ha='center', va='bottom', fontsize=10,
                 fontweight='bold', color='#1a1a2e')

    ax2 = axes[1]
    bars2 = ax2.bar(category_order, avg_rev_data.values / 1e3, color=colors_cluster,
                    edgecolor='white', linewidth=1.5, zorder=3)
    ax2.set_title('Rata-rata Pendapatan per Kategori', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Rata-rata Pendapatan (Ribu R$)', fontsize=10)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R${x:.1f}K'))
    ax2.set_facecolor('#FFFFFF')
    ax2.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax2.spines[['top', 'right']].set_visible(False)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 0.2,
                 f'R${h:.1f}K', ha='center', va='bottom', fontsize=9,
                 fontweight='bold', color='#1a1a2e')

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    st.markdown("### 📋 Detail Statistik per Kategori")
    cluster_summary = seller_perf.groupby('category').agg(
        jumlah_seller=('seller_id', 'count'),
        avg_revenue=('total_revenue', 'mean'),
        avg_orders=('total_orders', 'mean'),
        avg_items=('total_items', 'mean')
    ).reindex(category_order)
    cluster_summary.index.name = 'Kategori'
    cluster_summary.columns = ['Jumlah Seller', 'Avg Revenue (R$)', 'Avg Orders', 'Avg Items']
    st.dataframe(cluster_summary.style.format({
        'Avg Revenue (R$)': 'R${:,.2f}',
        'Avg Orders': '{:.1f}',
        'Avg Items': '{:.1f}'
    }).set_table_styles([{
        'selector': 'thead th',
        'props': [('background-color', '#dcfce7'), ('color', '#14532d'), ('font-weight', 'bold')]
    }]), use_container_width=True)

    st.success("**Insight:** Distribusi seller relatif merata di ketiga kategori. Gap pendapatan antara High Performer dengan Low/Medium sangat signifikan. Platform dapat merancang program insentif berbeda untuk setiap kategori.")

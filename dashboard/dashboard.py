import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import streamlit as st

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Brazil Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a5c38 0%, #2d8653 50%, #3aab69 100%);
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Hilangkan bullet (titik radio) */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
    display: none;
}

/* Biar item sejajar horizontal */
[data-testid="stSidebar"] .stRadio label {
    display: flex;
    align-items: center;
    gap: 10px; /* jarak icon dan teks */
    padding: 6px 10px;
    margin: 4px 0;
    background: transparent;
    border-radius: 8px;
}

/* Hover */
[data-testid="stSidebar"] .stRadio label:hover {
    background-color: rgba(255,255,255,0.15);
}

/* Selected */
[data-testid="stSidebar"] .stRadio input:checked + div {
    background-color: rgba(255,255,255,0.25);
    border-radius: 8px;
    padding: 6px 10px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border-left: 4px solid #16a34a;
    border-radius: 10px;
    padding: 12px 16px;
}

/* Dataframe header */
[data-testid="stDataFrame"] th {
    background-color: #16a34a !important;
    color: white !important;
}

/* Success box */
.stSuccess {
    background-color: #f0fdf4;
    border-left: 4px solid #16a34a;
}

/* Banner */
.green-banner {
    background: linear-gradient(135deg, #15803d, #22c55e);
    padding: 24px 32px;
    border-radius: 16px;
    margin-bottom: 24px;
    color: white;
}

/* Divider */
hr {
    border-color: #bbf7d0;
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
st.sidebar.image("https://www.flaticon.com/free-icon/commerce_14667832?term=shopping+bucket&page=1&position=13&origin=search&related_id=14667832", width=120)
st.sidebar.title("E-Commerce Brazil")
st.sidebar.markdown("**👩‍💻 Meilani Bulandari Hasibuan**")

st.sidebar.markdown("---")
year_filter = st.sidebar.multiselect(
    "Filter Tahun",
    options=[2017, 2018],
    default=[2017, 2018]
)

df_filtered = df_main[df_main['order_purchase_timestamp'].dt.year.isin(year_filter)]

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigasi",
    ["🏠 Overview", "💳 Metode Pembayaran", "🗺️ Pendapatan per Wilayah", "📦 Clustering Seller"]
)

# Warna hijau Brazil
GREEN_DARK   = '#15803d'
GREEN_MID    = '#22c55e'
GREEN_LIGHT  = '#86efac'
GREEN_PALE   = '#dcfce7'
colors_green = [GREEN_DARK, '#16a34a', GREEN_MID, GREEN_LIGHT]

# ══════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "🏠 Overview":

    # Banner hijau di atas
    st.markdown(f"""
    <div class='green-banner'>
        <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div>
                <h1 style='color:white; margin:0; font-size:28px;'>🛍️ E-Commerce Brazil</h1>
                <p style='color:rgba(255,255,255,0.9); margin:6px 0 0 0; font-size:15px;'>
                    Dashboard Analisis Transaksi Olist Dataset — Periode 2017–2018
                </p>
            </div>
            <div style='text-align:right;'>
                <p style='color:rgba(255,255,255,0.8); margin:0; font-size:13px;'>Total Pendapatan</p>
                <h2 style='color:white; margin:0; font-size:32px;'>
                    R${df_filtered['payment_value'].sum()/1e6:.2f}M
                </h2>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metric cards
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

    fig, ax = plt.subplots(figsize=(12, 4), facecolor='#f0fdf4')
    ax.set_facecolor('#FFFFFF')
    ax.plot(monthly_agg['month'], monthly_agg['payment_value'] / 1e3,
            color=GREEN_DARK, linewidth=2.5, marker='o', markersize=5)
    ax.fill_between(monthly_agg['month'], monthly_agg['payment_value'] / 1e3,
                    alpha=0.15, color=GREEN_MID)
    ax.set_title('Total Nilai Transaksi per Bulan', fontsize=12, fontweight='bold', color='#1a1a2e')
    ax.set_ylabel('Total Transaksi (Ribu R$)', fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R${x:.0f}K'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.4, color=GREEN_LIGHT)
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)

# ══════════════════════════════════════════════════════════════
# PAGE: METODE PEMBAYARAN
# ══════════════════════════════════════════════════════════════
elif page == "💳 Metode Pembayaran":
    st.markdown(f"""
    <div class='green-banner'>
        <h1 style='color:white; margin:0; font-size:24px;'>💳 Analisis Metode Pembayaran</h1>
        <p style='color:rgba(255,255,255,0.85); margin:6px 0 0 0; font-size:13px;'>
        Bagaimana perbandingan total nilai transaksi dan rata-rata cicilan antar metode pembayaran pada periode 2017-2018?
        </p>
    </div>
    """, unsafe_allow_html=True)

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

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor='#f0fdf4')
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
    ax1.grid(axis='y', linestyle='--', alpha=0.5, color=GREEN_PALE, zorder=0)
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
    ax2.grid(axis='y', linestyle='--', alpha=0.5, color=GREEN_PALE, zorder=0)
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
    }).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#15803d'), ('color', 'white'), ('font-weight', 'bold')]}
    ]), use_container_width=True)

    st.success("**Insight:** Credit Card mendominasi total nilai transaksi (R$12.5M, ~79%) dengan rata-rata cicilan 3.5x. Platform disarankan memperkuat kemitraan dengan penyedia credit card dan menawarkan promo cicilan 0%.")

# ══════════════════════════════════════════════════════════════
# PAGE: PENDAPATAN PER WILAYAH
# ══════════════════════════════════════════════════════════════
elif page == "🗺️ Pendapatan per Wilayah":
    st.markdown(f"""
    <div class='green-banner'>
        <h1 style='color:white; margin:0; font-size:24px;'>🗺️ Distribusi Pendapatan Seller per Negara Bagian</h1>
        <p style='color:rgba(255,255,255,0.85); margin:6px 0 0 0; font-size:13px;'>
        Bagaimana distribusi total pendapatan seller berdasarkan negara bagian pada periode 2017-2018?
        </p>
    </div>
    """, unsafe_allow_html=True)

    state_stats = df_filtered.groupby('seller_state').agg(
        jumlah_seller=('seller_id', 'nunique'),
        total_pendapatan=('payment_value', 'sum'),
        rata_pendapatan=('payment_value', 'mean')
    ).reset_index().sort_values('total_pendapatan', ascending=False).round(2)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏆 Negara Bagian Tertinggi", state_stats.iloc[0]['seller_state'],
                  delta=f"R${state_stats.iloc[0]['total_pendapatan']/1e6:.1f}M")
    with col2:
        st.metric("🗺️ Total Negara Bagian", f"{len(state_stats)}")
    with col3:
        st.metric("📊 Rata-rata per State", f"R${state_stats['total_pendapatan'].mean()/1e3:.1f}K")

    st.markdown("---")

    top_n = st.slider("Tampilkan Top N Negara Bagian", min_value=5, max_value=len(state_stats), value=15)
    p2 = state_stats.head(top_n).sort_values('total_pendapatan', ascending=True)
    colors_p2 = plt.cm.Greens(np.linspace(0.3, 0.9, len(p2)))

    fig, ax = plt.subplots(figsize=(11, max(5, top_n * 0.4)), facecolor='#f0fdf4')
    ax.set_facecolor('#FFFFFF')
    bars = ax.barh(p2['seller_state'], p2['total_pendapatan'] / 1e6,
                   color=colors_p2, edgecolor='white', linewidth=0.8, zorder=3)
    ax.set_title(f'Top {top_n} Negara Bagian berdasarkan Total Pendapatan Seller',
                 fontsize=12, fontweight='bold', color='#1a1a2e', pad=12)
    ax.set_xlabel('Total Pendapatan (Juta R$)', fontsize=10)
    ax.set_ylabel('Negara Bagian', fontsize=10)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R${x:.1f}M'))
    ax.grid(axis='x', linestyle='--', alpha=0.5, color=GREEN_PALE, zorder=0)
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
    }).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#15803d'), ('color', 'white'), ('font-weight', 'bold')]}
    ]), use_container_width=True)

    st.success("**Insight:** São Paulo (SP) mendominasi dengan R$13.3M (~65% total). Terdapat kesenjangan besar antara SP dengan negara bagian lain, menunjukkan peluang ekspansi bisnis yang besar.")

# ══════════════════════════════════════════════════════════════
# PAGE: CLUSTERING SELLER
# ══════════════════════════════════════════════════════════════
elif page == "📦 Clustering Seller":
    st.markdown("""
    <div class='green-banner'>
        <h1 style='color:white; margin:0; font-size:24px;'>📦 Clustering Seller Berdasarkan Performa</h1>
        <p style='color:rgba(255,255,255,0.85); margin:6px 0 0 0; font-size:13px;'>
        Pengelompokan seller ke dalam kategori Low, Medium, dan High Performer menggunakan teknik Binning.
        </p>
    </div>
    """, unsafe_allow_html=True)

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
        st.metric("🟡 Medium Performer", f"{n_med:,} seller", delta=f"R${q33:,.0f} – R${q66:,.0f}")
    with col3:
        n_high = (seller_perf['category'] == 'High Performer').sum()
        st.metric("🏆 High Performer", f"{n_high:,} seller", delta=f"> R${q66:,.0f}")

    st.markdown("---")

    category_order  = ['Low Performer', 'Medium Performer', 'High Performer']
    colors_cluster  = ['#86efac', '#22c55e', '#15803d']
    count_data      = seller_perf['category'].value_counts().reindex(category_order)
    avg_rev_data    = seller_perf.groupby('category')['total_revenue'].mean().reindex(category_order)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor='#f0fdf4')
    fig.suptitle('Clustering Seller Berdasarkan Performa Pendapatan (2017-2018)',
                 fontsize=12, fontweight='bold', color='#1a1a2e')

    ax1 = axes[0]
    bars1 = ax1.bar(category_order, count_data.values, color=colors_cluster,
                    edgecolor='white', linewidth=1.5, zorder=3)
    ax1.set_title('Jumlah Seller per Kategori', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Jumlah Seller', fontsize=10)
    ax1.set_facecolor('#FFFFFF')
    ax1.grid(axis='y', linestyle='--', alpha=0.5, color=GREEN_PALE, zorder=0)
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
    ax2.grid(axis='y', linestyle='--', alpha=0.5, color=GREEN_PALE, zorder=0)
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
    }).set_table_styles([
        {'selector': 'thead th', 'props': [('background-color', '#15803d'), ('color', 'white'), ('font-weight', 'bold')]}
    ]), use_container_width=True)

    st.success("**Insight:** Distribusi seller relatif merata di ketiga kategori. Gap pendapatan antara High Performer dengan Low/Medium sangat signifikan. Platform dapat merancang program insentif berbeda untuk setiap kategori.")

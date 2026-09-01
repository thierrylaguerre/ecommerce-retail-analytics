import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

NAVY="#1E2D5A"; TEAL="#0D7377"; GREEN="#14A085"; ORANGE="#E8813A"; LIGHT="#F7F9FC"; GRAY="#95A5A6"
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,
    'axes.facecolor':LIGHT,'figure.facecolor':'white','axes.titlesize':14,'axes.titleweight':'bold',
    'axes.titlecolor':NAVY,'axes.labelcolor':NAVY,'xtick.color':NAVY,'ytick.color':NAVY})

print("Chargement des données...")
clicks    = pd.read_csv('/mnt/user-data/uploads/fact_clickstream_sample.csv')
sales     = pd.read_csv('/mnt/user-data/uploads/fact_sale.csv')
customers = pd.read_csv('/mnt/user-data/uploads/dim_customer.csv')
products  = pd.read_csv('/mnt/user-data/uploads/dim_product.csv')

clicks['session_start_time'] = pd.to_datetime(clicks['session_start_time'])
clicks['session_end_time']   = pd.to_datetime(clicks['session_end_time'])
clicks['session_duration_min'] = (clicks['session_end_time'] - clicks['session_start_time']).dt.total_seconds() / 60
clicks['hour'] = clicks['session_start_time'].dt.hour

sales['transaction_timestamp'] = pd.to_datetime(sales['transaction_timestamp'])
sales['month_str'] = sales['transaction_timestamp'].dt.to_period('M').astype(str)
sales['margin']    = sales['line_total'] - sales['line_cost']

# Jointures correctes : sales → clicks → customers → products
sales_full = sales.merge(
    clicks[['session_id','customer_id','device_type','traffic_source']].dropna(subset=['customer_id']),
    on='session_id', how='left')
sales_full = sales_full.merge(products[['product_id','product_name','product_segment']], on='product_id', how='left')
sales_full = sales_full.merge(
    customers[['customer_id','loyalty_status','customer_persona','gender','signup_channel']],
    on='customer_id', how='left')

total_sessions  = len(clicks)
total_purchases = clicks['purchased_flag'].sum()
total_cart      = clicks['added_to_cart_flag'].sum()
conv_rate       = total_purchases / total_sessions * 100
total_revenue   = sales['line_total'].sum()
total_margin    = sales['margin'].sum()
margin_rate     = total_margin / total_revenue * 100
print(f"✅ Sessions: {total_sessions:,} | Conv: {conv_rate:.2f}% | CA: {total_revenue:,.0f}€ | Marge: {margin_rate:.1f}%\n")

# ── FIG 1 — ENTONNOIR ─────────────────────────────────────
funnel_labels = ['Sessions totales','Page produit visitée','Ajout panier','Achat finalisé']
funnel_values = [total_sessions, int(clicks['product_page_visited_flag'].sum()), int(total_cart), int(total_purchases)]
funnel_pct    = [v/total_sessions*100 for v in funnel_values]
fig, ax = plt.subplots(figsize=(10,5)); fig.patch.set_facecolor('white'); ax.set_facecolor('white')
for i,(label,val,pct,color) in enumerate(zip(funnel_labels,funnel_values,funnel_pct,[NAVY,TEAL,GREEN,ORANGE])):
    w = pct/funnel_pct[0]
    ax.barh(i, w, color=color, height=0.6, alpha=0.9)
    ax.text(w+0.01, i, f"{val:,.0f}  ({pct:.1f}%)", va='center', fontsize=11, color=NAVY, fontweight='bold')
ax.set_yticks(range(4)); ax.set_yticklabels(funnel_labels, fontsize=11)
ax.set_xlim(0,1.35); ax.xaxis.set_visible(False)
ax.spines['left'].set_visible(False); ax.spines['bottom'].set_color(GRAY)
ax.set_title('🛒  Entonnoir de Conversion — E-commerce Retail', pad=15)
plt.tight_layout(); plt.savefig('/home/claude/fig1_funnel.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✅ fig1_funnel.png")

# ── FIG 2 — DEVICE ────────────────────────────────────────
device = clicks.groupby('device_type').agg(sessions=('session_id','count'),purchases=('purchased_flag','sum')).reset_index()
device['conv_rate'] = device['purchases']/device['sessions']*100
device = device.sort_values('conv_rate', ascending=False)
fig, axes = plt.subplots(1,2,figsize=(12,5)); fig.patch.set_facecolor('white')
colors_d = [NAVY,TEAL,ORANGE]
wedges,texts,autotexts = axes[0].pie(device['sessions'], labels=device['device_type'], autopct='%1.1f%%',
    colors=colors_d, startangle=90, wedgeprops=dict(width=0.6), textprops=dict(color=NAVY,fontsize=11))
[at.set_fontweight('bold') for at in autotexts]
axes[0].set_title('Répartition des Sessions'); axes[0].set_facecolor('white')
bars = axes[1].bar(device['device_type'], device['conv_rate'], color=colors_d, width=0.5, alpha=0.9)
for bar,val in zip(bars,device['conv_rate']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.03, f"{val:.2f}%", ha='center', fontsize=11, fontweight='bold', color=NAVY)
axes[1].set_title("Taux de Conversion par Device"); axes[1].set_ylabel("Taux de conversion (%)")
axes[1].set_ylim(0, device['conv_rate'].max()*1.25); axes[1].set_facecolor(LIGHT)
fig.suptitle("📱  Performance par Device", fontsize=15, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout(); plt.savefig('/home/claude/fig2_device.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✅ fig2_device.png")

# ── FIG 3 — TRAFIC ────────────────────────────────────────
traffic = clicks.groupby('traffic_source').agg(sessions=('session_id','count'),purchases=('purchased_flag','sum')).reset_index()
traffic['conv_rate'] = traffic['purchases']/traffic['sessions']*100
traffic = traffic.sort_values('conv_rate', ascending=True)
palette = [NAVY,TEAL,GREEN,ORANGE,"#8E44AD"]
fig, axes = plt.subplots(1,2,figsize=(13,5)); fig.patch.set_facecolor('white')
axes[0].barh(traffic['traffic_source'], traffic['sessions'], color=palette, alpha=0.9)
for i,val in enumerate(traffic['sessions']):
    axes[0].text(val+500, i, f"{val:,.0f}", va='center', fontsize=10, color=NAVY)
axes[0].set_title("Sessions par Source de Trafic"); axes[0].set_xlabel("Nombre de sessions"); axes[0].set_facecolor(LIGHT)
axes[1].barh(traffic['traffic_source'], traffic['conv_rate'], color=palette, alpha=0.9)
for i,val in enumerate(traffic['conv_rate']):
    axes[1].text(val+0.02, i, f"{val:.2f}%", va='center', fontsize=10, fontweight='bold', color=NAVY)
axes[1].set_title("Taux de Conversion par Source (%)"); axes[1].set_xlabel("Taux de conversion (%)"); axes[1].set_facecolor(LIGHT)
fig.suptitle("🔗  Performance par Source de Trafic", fontsize=15, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout(); plt.savefig('/home/claude/fig3_traffic.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✅ fig3_traffic.png")

# ── FIG 4 — SESSIONS PAR HEURE ────────────────────────────
hourly = clicks.groupby('hour').agg(sessions=('session_id','count'),purchases=('purchased_flag','sum')).reset_index()
hourly['conv_rate'] = hourly['purchases']/hourly['sessions']*100
fig, ax1 = plt.subplots(figsize=(13,5)); fig.patch.set_facecolor('white'); ax1.set_facecolor(LIGHT)
ax1.bar(hourly['hour'], hourly['sessions'], color=NAVY, alpha=0.75)
ax1.set_xlabel("Heure de la journée"); ax1.set_ylabel("Nombre de sessions", color=NAVY)
ax1.tick_params(axis='y', labelcolor=NAVY); ax1.set_xticks(range(24))
ax2 = ax1.twinx()
ax2.plot(hourly['hour'], hourly['conv_rate'], color=ORANGE, linewidth=3, marker='o', markersize=6)
ax2.set_ylabel("Taux de conversion (%)", color=ORANGE); ax2.tick_params(axis='y', labelcolor=ORANGE)
ax2.spines['right'].set_color(ORANGE)
p1=mpatches.Patch(color=NAVY,label='Sessions'); p2=mpatches.Patch(color=ORANGE,label='Taux conversion (%)')
ax1.legend(handles=[p1,p2], loc='upper left')
ax1.set_title("⏰  Sessions & Taux de Conversion par Heure", pad=15)
plt.tight_layout(); plt.savefig('/home/claude/fig4_hourly.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✅ fig4_hourly.png")

# ── FIG 5 — REVENUS MENSUELS ──────────────────────────────
monthly = sales_full.groupby('month_str').agg(revenue=('line_total','sum'),margin=('margin','sum')).reset_index().sort_values('month_str')
fig, ax1 = plt.subplots(figsize=(14,5)); fig.patch.set_facecolor('white'); ax1.set_facecolor(LIGHT)
x = range(len(monthly))
ax1.bar(x, monthly['revenue'], color=NAVY, alpha=0.8)
ax1.set_ylabel("Revenus (€)", color=NAVY); ax1.set_xlabel("Mois")
ax1.set_xticks(x); ax1.set_xticklabels(monthly['month_str'], rotation=45, ha='right', fontsize=8)
ax2 = ax1.twinx()
ax2.plot(x, monthly['margin'], color=GREEN, linewidth=3, marker='o', markersize=5)
ax2.set_ylabel("Marge brute (€)", color=GREEN); ax2.tick_params(axis='y', labelcolor=GREEN)
ax2.spines['right'].set_color(GREEN)
p1=mpatches.Patch(color=NAVY,label='Revenus (€)'); p2=mpatches.Patch(color=GREEN,label='Marge brute (€)')
ax1.legend(handles=[p1,p2], loc='upper left')
ax1.set_title("📅  Évolution Revenus & Marge Brute — Vue Mensuelle", pad=15)
plt.tight_layout(); plt.savefig('/home/claude/fig5_monthly.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✅ fig5_monthly.png")

# ── FIG 6 — FIDÉLITÉ CLIENTS ──────────────────────────────
loyalty = sales_full.groupby('loyalty_status').agg(revenue=('line_total','sum'),customers=('customer_id','nunique')).reset_index().dropna()
loyalty['rev_per_customer'] = loyalty['revenue']/loyalty['customers']
loyalty = loyalty.sort_values('revenue', ascending=False)
colors_l = [NAVY,TEAL,GREEN,ORANGE]
fig, axes = plt.subplots(1,2,figsize=(12,5)); fig.patch.set_facecolor('white')
bars = axes[0].bar(loyalty['loyalty_status'], loyalty['revenue']/1e6, color=colors_l, alpha=0.9, width=0.5)
for bar,val in zip(bars,loyalty['revenue']/1e6):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1, f"{val:.1f}M€", ha='center', fontsize=10, fontweight='bold', color=NAVY)
axes[0].set_title("Revenus par Statut de Fidélité"); axes[0].set_ylabel("Revenus (M€)"); axes[0].set_facecolor(LIGHT)
bars2 = axes[1].bar(loyalty['loyalty_status'], loyalty['rev_per_customer'], color=colors_l, alpha=0.9, width=0.5)
for bar,val in zip(bars2,loyalty['rev_per_customer']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+5, f"{val:,.0f}€", ha='center', fontsize=10, fontweight='bold', color=NAVY)
axes[1].set_title("Revenu Moyen par Client"); axes[1].set_ylabel("Revenu moyen (€)"); axes[1].set_facecolor(LIGHT)
fig.suptitle("👥  Performance par Statut de Fidélité Client", fontsize=15, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout(); plt.savefig('/home/claude/fig6_loyalty.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✅ fig6_loyalty.png")

# ── FIG 7 — TOP 10 PRODUITS PAR MARGE ────────────────────
top_products = sales_full.groupby('product_name').agg(revenue=('line_total','sum'),margin=('margin','sum')).reset_index()
top10 = top_products.nlargest(10,'margin').sort_values('margin')
top10['label'] = top10['product_name'].str[:45]
fig, ax = plt.subplots(figsize=(12,6)); fig.patch.set_facecolor('white'); ax.set_facecolor(LIGHT)
bars = ax.barh(top10['label'], top10['margin']/1000, color=TEAL, alpha=0.9)
for bar,val in zip(bars,top10['margin']/1000):
    ax.text(val+0.5, bar.get_y()+bar.get_height()/2, f"{val:.0f}K€", va='center', fontsize=9, fontweight='bold', color=NAVY)
ax.set_xlabel("Marge brute (K€)"); ax.set_title("🏆  Top 10 Produits par Marge Brute", pad=15)
plt.tight_layout(); plt.savefig('/home/claude/fig7_top_products.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✅ fig7_top_products.png")

# ── FIG 8 — HEATMAP SEGMENT × CANAL ──────────────────────
seg_channel = sales_full.groupby(['product_segment','signup_channel']).agg(revenue=('line_total','sum')).reset_index().dropna()
pivot = seg_channel.pivot(index='product_segment', columns='signup_channel', values='revenue').fillna(0) / 1e6
fig, ax = plt.subplots(figsize=(10,5)); fig.patch.set_facecolor('white')
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='Blues', ax=ax, linewidths=0.5, linecolor='white',
    annot_kws={'size':11,'weight':'bold'}, cbar_kws={'label':'Revenus (M€)'})
ax.set_title("🔥  Revenus (M€) — Segment Produit × Canal d'Acquisition", pad=15, fontsize=13, fontweight='bold', color=NAVY)
ax.set_xlabel("Canal d'acquisition", color=NAVY); ax.set_ylabel("Segment produit", color=NAVY)
plt.tight_layout(); plt.savefig('/home/claude/fig8_heatmap.png', dpi=150, bbox_inches='tight'); plt.close()
print("  ✅ fig8_heatmap.png")

print(f"\n{'='*55}\n✅ ANALYSE TERMINÉE — 8 graphiques générés\n{'='*55}")
print(f"\n📊 KPIs GLOBAUX :")
print(f"  Sessions          : {total_sessions:>10,}")
print(f"  Taux conversion   : {conv_rate:>10.2f}%")
print(f"  Taux panier       : {total_cart/total_sessions*100:>10.2f}%")
print(f"  CA total          : {total_revenue:>10,.0f} €")
print(f"  Marge brute       : {total_margin:>10,.0f} €")
print(f"  Taux de marge     : {margin_rate:>10.1f}%")

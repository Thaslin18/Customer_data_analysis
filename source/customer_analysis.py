from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/customer_data.csv')
OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
print('Shape:',df.shape,'\\nMissing values:\\n',df.isna().sum(),'\\nDuplicate rows:',df.duplicated().sum())
df=df.drop_duplicates()
df['Annual_Income']=df['Annual_Income'].fillna(df['Annual_Income'].median())
df['Gender']=df['Gender'].fillna('Unknown'); df['Region']=df['Region'].fillna('Unknown')
df.to_csv(OUT/'cleaned_customer_data.csv',index=False)
df.describe(numeric_only=True).to_csv(OUT/'numeric_summary.csv')
region=df.groupby('Region').agg(Customers=('Customer_ID','nunique'),Total_Spend=('Total_Spend','sum'),Average_Spend=('Total_Spend','mean'),Orders=('Orders','sum')).sort_values('Total_Spend',ascending=False)
region.to_csv(OUT/'region_analysis.csv')
tier=df.groupby('Loyalty_Tier').agg(Customers=('Customer_ID','nunique'),Average_Spend=('Total_Spend','mean'),Total_Spend=('Total_Spend','sum'),Average_Orders=('Orders','mean')).sort_values('Total_Spend',ascending=False)
tier.to_csv(OUT/'loyalty_tier_analysis.csv')
spend_cut=df['Total_Spend'].quantile(.67); order_cut=df['Orders'].quantile(.67)
conditions=[(df['Total_Spend']>=spend_cut)&(df['Orders']>=order_cut),(df['Total_Spend']>=spend_cut),(df['Orders']>=order_cut)]
df['Customer_Segment']=np.select(conditions,['High Value','High Spenders','Frequent Buyers'],default='Regular Customers')
seg=df.groupby('Customer_Segment').agg(Customers=('Customer_ID','nunique'),Avg_Spend=('Total_Spend','mean'),Avg_Orders=('Orders','mean'),Total_Spend=('Total_Spend','sum')).sort_values('Total_Spend',ascending=False)
seg.to_csv(OUT/'customer_segment_analysis.csv'); df.to_csv(OUT/'customer_segments.csv',index=False)
for series,title,filename,ylabel in [(df.groupby('Region')['Total_Spend'].sum(),'Spend by Region','spend_by_region.png','Total Spend'),(df.groupby('Loyalty_Tier')['Total_Spend'].mean(),'Average Spend by Loyalty Tier','average_spend_by_loyalty.png','Average Spend'),(seg['Customers'],'Customer Count by Segment','customers_by_segment.png','Customers')]:
    plt.figure(); series.sort_values().plot(kind='bar'); plt.title(title); plt.ylabel(ylabel); plt.tight_layout(); plt.savefig(OUT/filename,dpi=150); plt.close()
print('Region summary:\\n',region,'\\nSegment summary:\\n',seg,'\\nOutputs saved to',OUT)

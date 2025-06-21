# --- 步驟 1: 匯入 pandas ---
import pandas as pd

# --- 步驟 2: 讀取 NPA_LineID.csv ---
df = pd.read_csv('../NPA_LineID.csv')

# --- 步驟 3: 重新命名欄位，使其更易於使用 ---
# 根據您的截圖，欄位應為「編號」、「LINE ID」、「通報日期」
df.rename(columns={
    '編號': 'serial_no',
    'LINE ID': 'line_id',
    '通報日期': 'report_date'
}, inplace=True)

# --- 步驟 4: 將 'report_date' 欄位轉換為真正的日期格式 ---
# 這是整個專案最關鍵的一步
df['report_date'] = pd.to_datetime(df['report_date'], errors='coerce')

# --- 步驟 5: 刪除日期轉換失敗或為空值的資料 ---
df.dropna(subset=['report_date'], inplace=True)

# --- 步驟 6: 確認成果 ---
print("清理與轉換後的資料資訊：")
df.info()
print("\n資料前五筆預覽：")
print(df.head())

# --- 步驟 7: 建立新的時間特徵欄位 ---
df['year'] = df['report_date'].dt.year
df['month'] = df['report_date'].dt.month
df['day_of_week'] = df['report_date'].dt.day_name()

# 為了方便後續按月份排序，我們建立一個年月欄位
df['year_month'] = df['report_date'].dt.to_period('M')

print("\n增加了年月特徵的資料預覽：")
df.head()


# --- 步驟 8: 按「年月」分組，並計算每個月的通報數量 ---
monthly_counts = df.groupby('year_month').size()

print("各月份詐騙通報數量統計：")
print(monthly_counts.tail(12)) # 印出最近 12 個月的數據看看

# --- 步驟 9: 按「星期幾」分組，並計算每個星期的通報數量 ---
weekly_counts = df.groupby('day_of_week').size()

# 為了讓星期排序正確 (週一到週日)
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekly_counts = weekly_counts.reindex(day_order)

print("\n各星期詐騙通報數量統計：")
print(weekly_counts)

# --- 步驟 10: 繪製每月通報數量的折線圖 ---
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---- 匯入中文字體 ----
!wget -O TaipeiSansTCBeta-Regular.ttf https://drive.google.com/uc?id=1eGAsTN1HBpJAkeVM57_C7ccp7hbgSz3_&export=download
fm.fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
plt.rc('font', family='Taipei Sans TC Beta')


plt.figure(figsize=(15, 7))
monthly_counts.plot(kind='line', marker='o', linestyle='-')

plt.title('每月詐騙LINE ID通報數量趨勢圖', fontsize=16)
plt.xlabel('月份', fontsize=12)
plt.ylabel('通報數量', fontsize=12)
plt.grid(True) # 加入格線
plt.show()

# --- 步驟 11: 繪製每週通報數量的長條圖 ---
plt.figure(figsize=(10, 6))
weekly_counts.plot(kind='bar', color='skyblue')

plt.title('每週各日詐騙通報數量分佈', fontsize=16)
plt.xlabel('星期', fontsize=12)
plt.ylabel('通報總數量', fontsize=12)
plt.xticks(rotation=0) # 標籤轉正
plt.show()

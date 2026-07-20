import random
from datetime import datetime, timedelta
import argparse
import csv
import time

def str_volume_to_int(s):
    """去除引号、千分逗号，转整数"""
    return int(s.replace('"', '').replace(',', ''))

def int_to_volume_str(num):
    """数字转为带千分逗号"""
    return f"{num:,}"

def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")

def format_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def append_stock_data(stock_num, interval, add_rows, min_vol_add, max_vol_add):
    
    csv_path = f"stock_tick_{datetime.now().strftime('%Y-%m-%d')}.csv"
    
    # read CSV file
    all_rows = []
    
    with open(csv_path, "a+", encoding="utf-8", newline="") as f:
        f.seek(0)
        reader = csv.reader(f)
        for row in reader:
            if row:
                all_rows.append(row)
    
    stock_meta = []     # per stock quote
    
    # If there's no such file, we create a new line
    if not all_rows:
        print(f"无{csv_path}文件，初始化{stock_num}只股票初始数据...")
        init_row = ["0", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        
        for i in range(stock_num):
            init_p = round(random.uniform(1.5, 99.5), 2)    
            init_t = round(random.uniform(1.5, 99.5), 2)
            init_row.extend([f"{init_p}", "0", "0", f"{init_t}"]) # price, change, volume, target 
            stock_meta.append([init_p, init_p, 0, init_t])  # Open Price, Last Price, Last Volume, Target
        
        with open(csv_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL) 
            writer.writerow(init_row)
            f.flush()   # 更新
        
        all_rows.append(init_row)
    else:
        first_row = all_rows[0]
        last_row = all_rows[-1]
        for i in range(stock_num):
            col_off = 2 + i * 4
            base_p = float(first_row[col_off])
            last_p = float(last_row[col_off])
            last_vol = str_volume_to_int(last_row[col_off + 2])
            target_p = float(last_row[col_off + 3])
            stock_meta.append([base_p, last_p, last_vol, target_p])
    
    # If there exists csv, we append new lines.
    print(f"{csv_path}读取完成,开始生成{add_rows}条Tick")
    last_dt = parse_time(all_rows[-1][1])
    current_dt = last_dt

    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for idx in range(add_rows):

            current_dt += timedelta(seconds=interval)  
            row_data = ["0", format_time(current_dt)]
            
            # iterate each stock
            for i in range(stock_num):
                base_p, last_p, last_vol, target_p = stock_meta[i]
            
                # 随机价格波动 ±0.1
                price_delta = round(random.uniform(-0.1, 0.1), 2)
                current_price = round(last_p + price_delta, 2) 

                # 计算涨跌金额、涨跌幅百分比
                price_diff = round(current_price - base_p, 2)
                pct_diff = round((price_diff / base_p) * 100, 2)
                sign = "+" if price_diff >= 0 else ""
                change_str = f"{sign}{price_diff} ({sign}{pct_diff}%)"

                # 累计成交量随机增加
                vol_add = random.randint(min_vol_add, max_vol_add)
                current_vol = last_vol + vol_add
                vol_str = int_to_volume_str(current_vol)

                row_data.extend([f"{current_price}", change_str, vol_str, f"{target_p}"])  
                stock_meta[i][1] = current_price
                stock_meta[i][2] = current_vol
                
            writer.writerow(row_data)
            f.flush()   # 更新
            print(f"已写入第{idx+1}/{add_rows}条：{','.join(row_data[:6])}")
            time.sleep(interval)

    print(f"✅ 成功追加 {add_rows} 条行情数据到 {csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="模拟股票实时行情数据")
   
    parser.add_argument("--num", type=int, default=2, help="股票数量")        # 必选
    parser.add_argument("--interval", type=int, default=1, help="Tick生成间隔")  # 可选
    parser.add_argument("--rows", type=int, default=100, help="需要追加的数据行数")
    parser.add_argument("--min-vol", type=int, default=400000, help="单次最小成交量增量")
    parser.add_argument("--max-vol", type=int, default=2800000, help="单次最大成交量增量")

    args = parser.parse_args()
    append_stock_data(
        stock_num=args.num,   
        interval=args.interval, 
        add_rows=args.rows,
        min_vol_add=args.min_vol,
        max_vol_add=args.max_vol
    )
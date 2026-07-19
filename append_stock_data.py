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

def append_stock_data(csv_path, add_rows, min_vol_add, max_vol_add, freq):
    # read CSV file
    all_rows = []
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                all_rows.append(row)

    if not all_rows:
        print("错误：CSV文件为空！")
        return

    # 第一行为开盘价
    base_price = float(all_rows[0][2])
    
    # 最后一行作为变化基准
    last_row = all_rows[-1]
    last_dt = parse_time(last_row[1])
    last_price = float(last_row[2])
    last_acc_vol = str_volume_to_int(last_row[4])
    target_price = last_row[5]

    current_price = last_price
    current_dt = last_dt
    current_vol = last_acc_vol

    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)

        for idx in range(add_rows):
            # 时间 +10秒
            current_dt += timedelta(seconds=freq)  
            
            # 随机价格波动 ±0.8
            price_delta = round(random.uniform(-0.8, 0.8), 2)
            current_price = round(current_price + price_delta, 2) 

            # 计算涨跌金额、涨跌幅百分比
            price_diff = round(current_price - base_price, 2)
            pct_diff = round((price_diff / base_price) * 100, 2)
            sign = "+" if price_diff >= 0 else ""
            change_str = f"{sign}{price_diff} ({sign}{pct_diff}%)"

            # 累计成交量随机增加
            vol_add = random.randint(min_vol_add, max_vol_add)
            current_vol += vol_add
            vol_str = int_to_volume_str(current_vol)

            # 拼接单行数据
            row_data = [
                "0",
                format_time(current_dt),
                f"{current_price}",
                change_str,
                vol_str,
                target_price
            ]
            writer.writerow(row_data)
            f.flush()   # 更新
            print(f"已写入第{idx+1}/{add_rows}条：{','.join(row_data)}")
            
            # 开启延迟
            time.sleep(freq)

    print(f"✅ 成功追加 {add_rows} 条行情数据到 {csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="股票CSV追加模拟累计成交量行情数据")
    # 必选参数
    parser.add_argument("--csv", type=str, default="2026-07-19 stock data.csv", help="目标CSV文件路径")
    parser.add_argument("--rows", type=int, default=10, help="需要追加的数据行数")
    parser.add_argument("--freq", type=int, default=10, help="实时延迟")
    
    # 可选参数
    parser.add_argument("--min-vol", type=int, default=400000, help="单次最小成交量增量")
    parser.add_argument("--max-vol", type=int, default=2800000, help="单次最大成交量增量")

    args = parser.parse_args()
    append_stock_data(
        csv_path=args.csv,        
        add_rows=args.rows,
        min_vol_add=args.min_vol,
        max_vol_add=args.max_vol,
        freq=args.freq
    )
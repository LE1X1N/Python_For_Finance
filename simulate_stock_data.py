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

def append_stock_data(stock_code, interval, add_rows, min_vol_add, max_vol_add):
    
    csv_path = f"{datetime.now().strftime('%Y-%m-%d')} {stock_code}.csv"
    
    # read CSV file
    all_rows = []
    
    with open(csv_path, "a+", encoding="utf-8", newline="") as f:
        f.seek(0)
        reader = csv.reader(f)
        for row in reader:
            if row:
                all_rows.append(row)
    
    # If there's no such file, we create a new line
    if not all_rows:
        print(f"无{csv_path}文件，正在模拟数据进行生成...")
        with open(csv_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL) 
            row_data = [
                "0",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"{round(random.uniform(1.5, 99.5),2)}",
                "0",
                "0",
                f"{round(random.uniform(1.5, 99.5),2)}"
            ]
            writer.writerow(row_data)
            f.flush()   # 更新
            all_rows.append(row_data)
     
    
    # If there exists csv, we append new lines.
    print(f"{csv_path}读取完成进行生成...")

    # 第一行为开盘价
    base_price = float(all_rows[0][2])
    
    # 最后一行作为变化基准
    last_row = all_rows[-1]
    last_dt = parse_time(last_row[1])
    last_price = float(last_row[2])
    last_acc_vol = str_volume_to_int(last_row[4])
    target_price = last_row[5]
    
    print(f"开盘价：{base_price}")
    print(f"最新价格：{last_price}({last_dt})")
    print(f"最新成交量：{last_acc_vol}({last_dt})")
    print(f"目标价：{target_price}")

    current_price = last_price
    current_dt = last_dt
    current_vol = last_acc_vol

    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)

        for idx in range(add_rows):
            # 时间 + interval
            current_dt += timedelta(seconds=interval)  
            
            # 随机价格波动 ±0.1
            price_delta = round(random.uniform(-0.1, 0.1), 2)
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

            # 拼接数据
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
            time.sleep(interval)

    print(f"✅ 成功追加 {add_rows} 条行情数据到 {csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="模拟股票实时行情数据")
   
    parser.add_argument("--code", type=str, default="BABA", help="股票代码")     # 必选
    parser.add_argument("--interval", type=int, default=1, help="Tick生成间隔")  # 可选
    parser.add_argument("--rows", type=int, default=100, help="需要追加的数据行数")
    parser.add_argument("--min-vol", type=int, default=400000, help="单次最小成交量增量")
    parser.add_argument("--max-vol", type=int, default=2800000, help="单次最大成交量增量")

    args = parser.parse_args()
    append_stock_data(
        stock_code=args.code,   
        interval=args.interval, 
        add_rows=args.rows,
        min_vol_add=args.min_vol,
        max_vol_add=args.max_vol
    )
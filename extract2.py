import csv
import sys
from collections import defaultdict

def extract_and_list_information(input_file, category, value, output_file=None):
    """
    指定したカテゴリと値に基づいてIP範囲と行数を抽出し、結果を出力する。

    Args:
        input_file (str): 入力CSVファイル名。
        category (str): 抽出対象カテゴリ (例: country_name, continent_name, asn, as_name, as_domain)。
        value (str): カテゴリ内の特定の値 (例: "Japan")。
        output_file (str, optional): 出力CSVファイル名。指定しない場合はコンソールに出力。
    """
    category_index = {
        "country_name": 3,
        "continent_name": 5,
        "asn": 6,
        "as_name": 7,
        "as_domain": 8,
    }

    if category not in category_index:
        print(f"エラー: 無効なカテゴリ '{category}' が指定されました。")
        return

    index = category_index[category]
    results = []
    total_count = 0

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        current_range = None
        ip_list = []
        count = 0

        for row in reader:
            if len(row) == 0:  # 空行で範囲を終了
                if current_range and current_range[index] == value:
                    results.append((current_range, count, ip_list))
                    total_count += count
                current_range = None
                ip_list = []
                count = 0
                continue

            if current_range is None:  # 範囲のヘッダー行
                current_range = row
            else:  # IPアドレス行
                if current_range[index] == value:
                    ip_list.append(row[0])
                    count += 1

        if current_range and current_range[index] == value:  # 最後の範囲を確認
            results.append((current_range, count, ip_list))
            total_count += count

    # 結果の出力
    if output_file:
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([value])
            writer.writerow(["Total Count", total_count])
            writer.writerow([])

            for current_range, count, ip_list in results:
                writer.writerow(current_range)
                writer.writerow([count])
                for ip in ip_list:
                    writer.writerow([ip])
                writer.writerow([])

        print(f"結果が'{output_file}'に出力されました。")
    else:
        print(value)
        print(f"Total Count: {total_count}\n")

        for current_range, count, ip_list in results:
            print(",".join(current_range))
            print(count)
            for ip in ip_list:
                print(ip)
            print()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("使用方法: python extract2.py <category> <value> <input_file> [output_file]")
        print("カテゴリは以下から選択してください: country_name, continent_name, asn, as_name, as_domain")
    else:
        category = sys.argv[1]
        value = sys.argv[2]
        input_file = sys.argv[3]
        output_file = sys.argv[4] if len(sys.argv) > 4 else None
        extract_and_list_information(input_file, category, value, output_file)

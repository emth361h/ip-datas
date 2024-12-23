import csv
import sys
from collections import defaultdict

def extract_information(input_file, category, output_file=None):
    """
    指定したカテゴリごとにIPの行数を集計する。

    Args:
        input_file (str): 入力CSVファイル名。
        category (str): 抜き出すカテゴリ名 (例: country_name, continent_name, asn, as_name, as_domain)。
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
    counts = defaultdict(int)

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        current_category = None

        for row in reader:
            if len(row) == 0:  # 空行は範囲の区切り
                current_category = None
                continue

            if current_category is None:  # 範囲のヘッダー行
                current_category = row[index]
            else:  # IPアドレス行
                counts[current_category] += 1

    # 結果の出力
    if output_file:
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([category, "Count"])
            for key, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
                writer.writerow([key, count])
        print(f"結果が'{output_file}'に出力されました。")
    else:
        print(f"{category.capitalize()}\tCount")
        for key, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{key}\t{count}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使用方法: python extract.py <category> <input_file> [output_file]")
        print("カテゴリは以下から選択してください: country_name, continent_name, asn, as_name, as_domain")
    else:
        category = sys.argv[1]
        input_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        extract_information(input_file, category, output_file)

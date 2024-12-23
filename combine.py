import csv
import ipaddress
from bisect import bisect_left, bisect_right

# 入力ファイルと出力ファイルのパス
ipinfo_file = "output1.csv"  # IP範囲情報が含まれるCSVファイル
iplist_file = "output2.csv"  # 単一のIPアドレスが含まれるCSVファイル
output_file = "end.csv"  # 結合された結果を書き込むCSVファイル

def ip_to_int(ip):
    """
    IPアドレスを整数に変換する（高速な比較のため）。
    """
    return int(ipaddress.ip_address(ip))

def merge_ipinfo_and_iplist(ipinfo_file, iplist_file, output_file):
    """
    IP範囲情報と単一IPアドレスを結合し、新しいファイルに出力する。
    範囲内にIPが一つもない行は削除する。
    """
    with open(ipinfo_file, 'r', encoding='utf-8') as ipinfo, open(iplist_file, 'r', encoding='utf-8') as iplist, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        ipinfo_reader = csv.reader(ipinfo)
        iplist_reader = csv.reader(iplist)
        output_writer = csv.writer(outfile)

        # IPリストを整数リストとしてソート
        ip_set = sorted(ip_to_int(row[0]) for row in iplist_reader if row)

        # IP範囲ごとに対応するIPを挿入
        for ipinfo_row in ipinfo_reader:
            if len(ipinfo_row) == 0 or ipinfo_row[0] == "start_ip":  # 空行やヘッダーをスキップ
                continue

            start_ip, end_ip = ip_to_int(ipinfo_row[0]), ip_to_int(ipinfo_row[1])

            # 二分探索で範囲内のIPを取得
            start_idx = bisect_left(ip_set, start_ip)
            end_idx = bisect_right(ip_set, end_ip)
            matching_ips = ip_set[start_idx:end_idx]

            # ログ出力: 範囲情報と一致するIP
            print(f"Checking range {ipinfo_row[0]} - {ipinfo_row[1]}, found {len(matching_ips)} matching IPs.")

            # 対応するIPがない場合はスキップ
            if not matching_ips:
                print(f"No matching IPs for range {ipinfo_row[0]} - {ipinfo_row[1]}, skipping.")
                continue

            # IP範囲を出力
            output_writer.writerow(ipinfo_row)
            print(f"Writing range: {ipinfo_row}")

            # 対応するIPを出力
            for ip in matching_ips:
                output_writer.writerow([ipaddress.ip_address(ip)])
                print(f"Writing IP: {ipaddress.ip_address(ip)}")

            # 空行を挿入
            output_writer.writerow([])
            print("Adding empty line after range.")

def main():
    merge_ipinfo_and_iplist(ipinfo_file, iplist_file, output_file)
    print(f"'{ipinfo_file}'と'{iplist_file}'を結合して'{output_file}'に出力しました。")

if __name__ == "__main__":
    main()

import csv
import ipaddress

# 入力ファイルと出力ファイルのパス
input_file = "country_asn.csv"  # 元のCSVファイル
output_file = "output2.csv"  # IPv4のみを含むCSVファイル

def filter_ipv4_rows(input_file, output_file):
    """
    IPv6アドレスを含む行を削除し、IPv4アドレスのみを保持する。
    """
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)

        # ヘッダー行を処理
        header = next(csv_reader)
        csv_writer.writerow(header)

        # 各行を処理
        for row in csv_reader:
            try:
                # start_ipの列をチェック
                ip = ipaddress.ip_address(row[0])
                if isinstance(ip, ipaddress.IPv4Address):
                    csv_writer.writerow(row)
            except ValueError:
                # IPアドレスとして認識できない場合は無視
                continue

def main():
    filter_ipv4_rows(input_file, output_file)
    print(f"IPv4のみのデータを'{output_file}'に出力しました。")

if __name__ == "__main__":
    main()

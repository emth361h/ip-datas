import re
import csv

# 入力ファイルと出力ファイルのパスを指定します
input_file = "log.txt"  # IPアドレスが含まれるテキストファイル
output_file = "output1.csv"  # 抽出されたIPアドレスを書き込むCSVファイル

# IPアドレスの正規表現
ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"

def extract_ips_from_file(input_file):
    """
    指定したファイルからIPアドレスを抽出します。
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    return re.findall(ip_pattern, content)

def write_ips_to_csv(ips, output_file):
    """
    抽出したIPアドレスをCSVファイルに書き込みます。
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["IP Address"])
        for ip in ips:
            csv_writer.writerow([ip])

def main():
    # テキストファイルからIPアドレスを抽出
    ips = extract_ips_from_file(input_file)

    # 重複を除外してオクテッドごとにソート
    unique_ips = sorted(set(ips), key=lambda ip: list(map(int, ip.split('.'))))

    # 抽出したIPアドレスをCSVに出力
    write_ips_to_csv(unique_ips, output_file)
    print(f"{len(unique_ips)}個のIPアドレスを'{output_file}'に書き込みました。")

if __name__ == "__main__":
    main()

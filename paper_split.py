import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf_by_pages(input_pdf_path, output_dir, max_pages=100, max_size_mb=50):
    # pdfリーダーでpdfを読み込む
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)

    # ファイルサイズを取得 (MBに変換)
    file_size_mb = os.path.getsize(input_pdf_path) / (1024 * 1024)

    # 条件チェック：101ページ以上または50MB以上のファイルのみ分割
    if total_pages < max_pages + 1 and file_size_mb < max_size_mb:
        print(f"{input_pdf_path} は処理をスキップします（{total_pages}ページ, {file_size_mb:.2f}MB）")
        return

    # 分割するセグメント数を計算
    num_segments = -(-total_pages // max_pages)  # 端数を切り上げるための計算

    # 各セグメントを分割・保存
    for i in range(num_segments):
        writer = PdfWriter()
        start_page = i * max_pages
        end_page = min(start_page + max_pages, total_pages)

        # ページをpdfライターに追加
        for j in range(start_page, end_page):
            writer.add_page(reader.pages[j])

        # 分割ファイル名を生成
        base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
        output_filename = f"{base_name}_{i + 1}-{num_segments}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        # ファイルを保存
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

        print(f"{output_path} を作成しました ({end_page - start_page}ページ)")

def process_pdfs_in_directory(directory_path):
    # "split" フォルダを作成
    output_dir = os.path.join(directory_path, "split")
    os.makedirs(output_dir, exist_ok=True)

    # 指定ディレクトリ内のpdfファイルをすべて取得
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            split_pdf_by_pages(file_path, output_dir)

# 使用例：対象ディレクトリを指定
directory = "/please replace your directory"
process_pdfs_in_directory(directory)

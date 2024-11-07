import os
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs_in_directory(directory):
    # "merged"フォルダを作成
    output_dir = os.path.join(directory, "merged")
    os.makedirs(output_dir, exist_ok=True)

    # ディレクトリ内のpdfファイルを取得
    pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]

    # pdfファイルをプレフィックスごとにグループ化
    pdf_groups = {}
    for pdf_file in pdf_files:
        prefix = pdf_file.rsplit("_", 1)[0]  # "_"より前の文字列を取得
        if prefix not in pdf_groups:
            pdf_groups[prefix] = []
        pdf_groups[prefix].append(pdf_file)

    for prefix, files in pdf_groups.items():
        # 数字の順序でファイルをソート
        files.sort(key=lambda f: int(f.rsplit("_", 1)[-1].split("-")[0]))

        # 結合用のPdfWriterを準備
        pdf_writer = PdfWriter()

        # 各ファイルを順に追加
        for pdf_file in files:
            file_path = os.path.join(directory, pdf_file)
            pdf_reader = PdfReader(file_path)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

        # 結合後のファイル名を作成
        output_filename = f"{prefix}_merged.pdf"
        output_path = os.path.join(output_dir, output_filename)

        # 結合ファイルを保存
        with open(output_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

        print(f"Created: {output_path}")

directory = "/please replace your directory"
merge_pdfs_in_directory(directory)

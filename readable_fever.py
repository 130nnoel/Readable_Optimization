import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

# ディレクトリ設定
UPLOAD_URL = "https://readable.jp/translate/" #Readable URL変更しないこと
INPUT_DIR = "/please replace your directory"  # pdfファイルが格納されているディレクトリ
OUTPUT_DIR = "/please replace your directory"  # 翻訳後のpdfを保存するディレクトリ
WAIT_TIME = 30  # 翻訳完了待機時間（秒）

# フォルダの作成
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chromeのダウンロード設定
options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": OUTPUT_DIR,  # ダウンロード先フォルダ
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
options.add_argument("--user-data-dir=/please replace your directory") # profile path
options.add_argument("--profile-directory=please replace your profile")

# Chromedriverの初期化
service = Service('/please replace your directory')  # Chromedriverのパスを指定
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 60)  # 最大待機時間を設定


def upload_and_download_pdf(file_path):
    try:
        driver.get(UPLOAD_URL)

        # ログイン情報取得のため2秒待機
        time.sleep(2)

        # アップロードボタンをクリックし、ファイルをアップロード
        upload_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-ff82bce6-0.fiCMrC button.sc-8546a92d-0.ljwDRV")) # ボタンクラスだけの指定だと「お支払いの管理」と同クラス名で誤動作するため上位クラスと併せて指定
        )
        upload_button.click()

        # 1秒待機
        time.sleep(1)

        # <input type="file"> 要素にファイルパスを送信
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(file_path)

        # ダウンロードリンクが表示されるまで待機(ここでは日英交互を設定。日本語のみに変更したい場合は下記"al"を"ja"にする)
        download_link = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'ja-')]"))
        )

        # ダウンロードリンクのURLを取得してファイルを保存
        download_url = download_link.get_attribute("href")
        response = requests.get(download_url)

        # ダウンロードファイルの保存
        file_name = os.path.join(OUTPUT_DIR, os.path.basename(download_url))
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {file_name}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

        # 1秒待機
        time.sleep(1)

def main():
    # 指定ディレクトリからPDFファイルを取得
    pdf_files = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        upload_and_download_pdf(pdf_file)

    driver.quit()

if __name__ == "__main__":
    main()

""" Downloader with Python & Selenium
"""


from selenium import webdriver
from pathlib import Path
import time
import glob
import shutil
from queue import Queue


class Downloader:
    """
    Downloader Class
    
    Attributes
    ----------  
    driver: webdriver.Chrome
        クロームのWEBドライバー
    incompete_directory: Path
        ダウンロード完了前のファイルを保存するディレクトリ
    download_directory: Path
        ダウンロード完了後のファイルを保存するディレクトリ
    profile_directory: Path
        プロファイルを保存するディレクトリ
    downloading_count: int
        進行中のダウンロード数
    """

    def __init__(self, incomplete_directory, download_directory, profile_directory, isHeadless=True):
        """
        初期処理 フォルダを作ったりWEBドライバーをセットアップしたりする

        Parameters
        ----------------
        incompete_directory: str
            ダウンロード完了前のファイルを保存するディレクトリ
        download_directory: str
            ダウンロード完了後のファイルを保存するディレクトリ
        profile_directory: str
            プロファイルを保存するディレクトリ
        isHeadless: bool
            ヘッドレス動作かどうかを示すBoolean
        """
        self.incomplete_directory =  Path(incomplete_directory)
        self.download_directory = Path(download_directory)  
        self.profile_directory = Path(profile_directory)  
        self.downloading_count = 0

        # ディレクトリを作る
        self.incomplete_directory.mkdir(exist_ok=True)        
        self.download_directory.mkdir(exist_ok=True)
        self.profile_directory.mkdir(exist_ok=True)

        # ドライバのセットアップ
        self.driver = self.setUpDriver(
            str(self.incomplete_directory.resolve()),
            str(self.profile_directory.resolve()), 
            isHeadless
            )

    def setUpDriver(self, incomplete_directory, profile_directory, isHeadless):
        """
        Seleniumドライバーをセットアップする
        
        Parameters
        ----------------
        incompete_directory: str
            ダウンロード完了前のファイルを保存するディレクトリ（絶対パス）
        profile_directory: str
            プロファイルを保存するディレクトリ（絶対パス）
        isHeadless: bool
            ヘッドレス動作かどうかを示すBoolean

        Returns
        -------
        driver: webdriver.Chrome
            クロームのWEBドライバー          
        """        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": incomplete_directory,
            "plugins.always_open_pdf_externally": True
        })
        options.add_argument('--user-data-dir=' + profile_directory)
        if isHeadless:       
            options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)

        if isHeadless:
            # ヘッドレス時のダウンロード設定
            driver.command_executor._commands["send_command"] = (
                "POST",
                '/session/$sessionId/chromium/send_command'
            )
            params = {
                'cmd': 'Page.setDownloadBehavior',
                'params': {
                    'behavior': 'allow',
                    'downloadPath': incomplete_directory
                }
            }
            driver.execute("send_command", params=params)
        return driver

    def login(self):
        """ ログイン処理 子クラスで使う
        """
        pass

    @property
    def finishedItems(self):
        """
        ダウンロードが終了したアイテムのファイル名をジェネレータで返す

        Returns
        -------
        items: generator
            ダウンロードが終了したアイテムのジェネレータ 
        """
        for item in glob.glob(str(self.incomplete_directory.joinpath("*"))):
            if(not ".crdownload" in item):
                yield item

    def fromURL(self, url):
        """ 
        URLからダウンロードする
        """
        self.driver.get(url)

    def moveToDownloadDirectory(self, incomplete_path):
        """
        ファイルをincompleteからdownloadに移動する
        """
        basename =  Path(incomplete_path).name
        shutil.move(
            incomplete_path,
            str(self.download_directory.joinpath(basename))
        )

    def run(self, queue_file):
        """
        ダウンローダーを起動する

        Parameters
        ----------------
        queue_file: str
            キューファイルのパス      
        """
        queue = Queue(queue_file)
        self.login()

        while not queue.finished:
            if self.downloading_count == 0 and queue.hasQueue:
                # ダウンロードに追加
                self.downloading_count += 1    
                url = queue.next()
                queue.save()
                self.fromURL(url)

            for item in self.finishedItems:
                # ダウンロード完了時処理
                self.downloading_count -= 1                
                self.moveToDownloadDirectory(item)
                url = queue.findFromDownloading(Path(item).name)
                queue.toFinished(url)
                queue.save()
            time.sleep(1)

    def idle(self):
        """
        ブラウザを起動したまま待機する  
        """
        self.login()

        while True:
            time.sleep(1)

    def __del__(self):
        """
        デストラクタでドライバーを開放する
        """
        self.driver.quit()
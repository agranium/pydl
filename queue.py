import json


class Queue:
    """
    キューを管理するためのクラス
    """

    def __init__(self, path):
        self.path = path
        self.data = None
        self.load()
        if len(self.downloading) != 0:
            self.queue.extend(self.downloading)
            self.downloading.clear()

    @property
    def queue(self):
        """キューのリストを返す
        """
        return self.data["queue"]

    @property
    def downloading(self):
        """ダウンロード中のリストを返す
        """
        return self.data["downloading"]

    @property
    def finished(self):
        """完了済みのリストを返す
        """
        return self.data["finished"]

    @property
    def hasQueue(self):
        """未処理のキューが有るかBooleanで返す
        """
        if len(self.queue):
            return True
        else:
            return False
            
    @property
    def isDownloading(self):
        """ダウンロード中かBooleanで返す
        """
        if len(self.downloading):
            return True
        else:
            return False

    @property
    def isFinished(self):
        """全部完了しているかBooleanで返す
        """
        return not (self.hasQueue or self.isDownloading)

    def load(self):
        """ 
        Queueをロードする
        """
        data = None
        with open(self.path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self):
        """
        Queueをセーブする
        """
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def next(self):
        """
        Queueの要素を取り出してDownloadingに移す
        """
        url = self.queue.pop(0)     
        self.downloading.append(url)
        return url
    
    def findFromDownloading(self, name):
        """
        Downloadingから対象のファイルを探してURLを返す
        """
        for url in self.downloading:
            if(name in url):
                return url

    def toFinished(self, url):
        """
        URLをDownloadingからFinishedに移動する
        """
        self.downloading.remove(url)
        self.finished.append(url)
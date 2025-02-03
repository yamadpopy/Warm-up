# common_logger.py
# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import yaml
from logging.handlers import TimedRotatingFileHandler

###############################################################################
# 日次ローテーション + yyyy-mmフォルダ/ yyyy-mm-dd.log
###############################################################################
class DailyDirectoryRotatingFileHandler(TimedRotatingFileHandler):
    """
    TimedRotatingFileHandlerを継承し、日付単位でyyyy-mmフォルダを作り、
    ファイル名をyyyy-mm-dd.logとして出力するハンドラ
    """
    def __init__(
        self,
        base_dir: str,
        when: str = "midnight",
        interval: int = 1,
        backupCount: int = 7,
        encoding: str = "utf-8",
        utc: bool = False,
    ):
        self.base_dir = base_dir
        initial_filename = self._make_daily_log_file_path()
        super().__init__(
            filename=initial_filename,
            when=when,
            interval=interval,
            backupCount=backupCount,
            encoding=encoding,
            utc=utc,
        )

    def _make_daily_log_file_path(self) -> str:
        now = datetime.datetime.now()
        yyyy_mm = now.strftime("%Y-%m")       # 例: 2023-10
        yyyy_mm_dd = now.strftime("%Y-%m-%d") # 例: 2023-10-17

        # base_dir/python1/2023-10/[2023-10-17].log のイメージ
        sub_dir = os.path.join(self.base_dir, yyyy_mm)
        os.makedirs(sub_dir, exist_ok=True)
        return os.path.join(sub_dir, f"{yyyy_mm_dd}.log")

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        new_log_path = self._make_daily_log_file_path()
        self.baseFilename = os.path.abspath(new_log_path)
        super().doRollover()


###############################################################################
# ロガー設定関数
###############################################################################
def setup_daily_logger(self):
    """
    フォルダ設定.yamlから「大元ログフォルダ」を読み込み、さらにサブフォルダ名をPythonコード側で指定し、
    指定されたフォルダに対して日次ローテーションログ設定を行う。

    Parameters
    ----------

    sub_folder_name : str
        大元ログフォルダの下に作りたいサブフォルダ名
        例: "python1", "加工予定表_ダンプ" など

    log_level : int
        ログレベル (logging.INFO, logging.DEBUG など)

    Returns
    -------
    logging.Logger
        セットアップが完了したロガーインスタンス
    """

    # サブフォルダを組み合わせて、出力先となるフォルダを作成
    # 例: C:\Business_type\製造レシピ\ver1.0\log\python1
    base_dir = os.path.join(
        self.dic['NASベースパス'],
        self.dic['プロジェクト名'],
        '現地_log'
        )
    os.makedirs(base_dir, exist_ok=True)

    # ロガー取得
    self.logger = logging.getLogger("")
    self.logger.setLevel(logging.INFO)

    # 既存のハンドラをクリア（重複追加防止）
    self.logger.handlers = []

    # Console出力
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    self.logger.addHandler(console_handler)

    # 日次ローテーションファイル出力 (yyyy-mm-dd.log)
    rotation_handler = DailyDirectoryRotatingFileHandler(base_dir=base_dir)
    rotation_handler.setLevel(logging.INFO)
    rotation_handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    self.logger.addHandler(rotation_handler)

    self.logger.info(f"ログ設定完了: base_dir={base_dir}")

# -*- coding: utf-8 -*-
import psutil

def startup_confirmation(adc_exe):
    for proc in psutil.process_iter(attrs=['pid', 'exe']):
        try:
            # プロセス名と実行パスを表示
            if adc_exe == proc.info['exe']:
                return [True , proc.info['pid']]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # プロセスが終了している場合やアクセスが拒否される場合はスキップ
            continue
    return [False , 0]

def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()  # 終了要求
        p.wait()       # プロセスが終了するまで待つ
        print(f"プロセス {pid} を終了しました。")
    except psutil.NoSuchProcess:
        print(f"プロセス {pid} は存在しません。")
    except psutil.AccessDenied:
        print(f"プロセス {pid} にアクセスできません。")
    except Exception as e:
        print(f"エラー: {e}")


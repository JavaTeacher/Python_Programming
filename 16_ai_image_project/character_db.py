# 이미지 DB 모듈
# - SQLite 캐릭터 / 인식 기록 테이블 생성/저장/조회 담당

import os
import sqlite3

# ===========================================================
#  2. DB 처리
#  - init_db()          : 테이블 생성 + 캐릭터 3명 넣기 (이미 있으면 그대로 둠)
#  - save_detection()   : 인식 기록 한 건 저장
#  - load_detections()  : 인식 기록 조회 (최신순)
# ===========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "character.db")

# ===========================================================
#  1. init_db() : 테이블 생성
# ===========================================================

def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score REAL NOT NULL,
                image_path TEXT
            )
        """)

    except sqlite3.Error as e:
        print("DB 오류:", e)
        raise
 
    finally:
        if conn is not None:
            conn.close()


# ===========================================================
#  2. save_detection() : 인식 기록 저장
#  - id          : 기록 번호 (자동 증가)
#  - name        : 인식된 캐릭터
#  - score       : AI 확률 (0~1)
#  - image_path  : 사진 경로
# ===========================================================

def save_detection(name, score, image_path=None):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO detections (name, score, image_path) VALUES (?, ?, ?)",
            (name, score, image_path),
        )
        conn.commit()

    except sqlite3.Error as e:
        print("DB 오류:", e)
        if conn is not None:
            conn.rollback()
        raise

    finally:
        if conn is not None:
            conn.close()


# ===========================================================
#  3. load_detections() : 인식 기록 조회
# ===========================================================

def load_detections(name=None):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        if not name:
            cur.execute("SELECT * FROM detections")
        else:
            cur.execute("SELECT * FROM detections WHERE name = ?", (name,))

        return cur.fetchall()

    except sqlite3.Error as e:
        print("DB 오류:", e)
        raise

    finally:
        if conn is not None:
            conn.close()

# 리뷰 DB 모듈
# - SQLite 리뷰 테이블 생성/저장/조회 담당

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "review.db")

# ===========================================================
#  1. init_db() : 테이블 생성
# ===========================================================

def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mlsv_ymd TEXT NOT NULL,
                content TEXT NOT NULL,
                label TEXT NOT NULL,
                score REAL NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
            )
        """)

    except sqlite3.Error as e:
        print("DB 오류:", e)
        raise
 
    finally:
        if conn is not None:
            conn.close()


# ===========================================================
#  2. load_reviews(): 저장된 리뷰 정보 조회
# ===========================================================

def load_reviews(mlsv_ymd, label=None):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        if not label:
            cur.execute("SELECT * FROM reviews WHERE mlsv_ymd = ?", (mlsv_ymd,))
        else:
            cur.execute("SELECT * FROM reviews WHERE mlsv_ymd = ? AND label = ?", (mlsv_ymd, label))

        return cur.fetchall()

    except sqlite3.Error as e:
        print("DB 오류:", e)
        raise

    finally:
        if conn is not None:
            conn.close()


# ===========================================================
#  3. save_review() : 리뷰 정보 저장
# ===========================================================

def save_review(mlsv_ymd, content, label, score):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reviews (mlsv_ymd, content, label, score) VALUES (?, ?, ?, ?)",
            (mlsv_ymd, content, label, score),
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


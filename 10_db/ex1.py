# 데이터베이스 사용

# ===========================================================
#  1. SQLite란?
#  - 별도의 서버 없이 하나의 파일에 데이터를 (  ) 형태로 저장하는
#    가볍고 간단한 관계형 데이터베이스(RDBMS)
#  - 파이썬에 sqlite3 모듈이 기본으로 포함되어 있어 추가 설치가 필요 없음
#
#  [DB 사용 순서]
#  - connect() : DB에 (  ), 데이터베이스 파일이 없으면 자동 생성
#  - cursor()  : SQL을 실행하는 (  ) 객체 생성
#  - execute() : SQL을 (  )
#  - commit()  : INSERT/UPDATE/DELETE 후 변경사항을 확정
#  - close()   : 사용이 끝나면 연결 (  )
#
#  [기본 SQL문]
#  - (  ) : 테이블 생성
#  - (  ) : 데이터 삽입
#  - (  ) : 데이터 조회
#  - (  ) : 데이터 변경
#  - (  ) : 데이터 삭제
# ===========================================================

import os
import sqlite3

# DB 파일 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "school.db")


# ===========================================================
#  1. Student 클래스
#  - Student 테이블에 대한 DB Wrapper 클래스 (DAO: Data Access Object)
# ===========================================================

# class Student:
    # 생성자: Student 객체 초기화
    # def __init__(self, db_path):
    #     self.conn = sqlite3.( )(db_path)    # DB 연결        
    #     self.cur = self.conn.( )()           # Cursor: SQL을 실행하는 객체
    #     self.(  )()

    # 테이블 생성
    # def create_table(self):
    #     self.cur.( )("""
    #         CREATE TABLE IF NOT EXISTS student (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             name TEXT,
    #             age INTEGER,
    #             score INTEGER
    #         )
    #     """)

    # 데이터 삽입 (? 사용)
    # ===========================================================
    #  (중요) ? (Placeholder)
    #  - SQL 문에서 값이 들어갈 자리에 ( )를 쓰고, 실제 값은 ( )로 전달한다.
    #  - ?와 튜플의 값은 순서대로 짝지어진다.
    #  - SQL Injection 방지
    # ===========================================================
    # def insert(self, name, age, score):
    #     self.cur.( )(
    #         "INSERT INTO student (name, age, score) VALUES (?, ?, ?)",
    #         (name, age, score)
    #     )
    #     self.conn.( )()              # 변경사항 확정 (INSERT/UPDATE/DELETE 후 필수)
    #     print("INSERT 완료")

    # 전체 조회
    # def show_all(self):
        # self.cur.( )("SELECT * FROM student")
        # for row in self.cur.( )():
        #     print(row)

    # 점수가 min_score 이상인 데이터 조회
    # def select_by_score(self, min_score):
    #     self.cur.( )("SELECT * FROM student WHERE score >= ?", (min_score,))
    #     return self.cur.( )()

    # 이름으로 점수 변경
    # def update_score(self, name, score):
    #     self.cur.( )("UPDATE student SET score = ? WHERE name = ?", (score, name))
    #     self.conn.( )()
    #     print("UPDATE 완료")

    # 이름으로 삭제
    # def delete(self, name):
    #     self.cur.( )("DELETE FROM student WHERE name = ?", (name,))
    #     self.conn.( )()
    #     print("DELETE 완료")

    # 전체 삭제
    # def delete_all(self):
    #     self.cur.( )("DELETE FROM student")
    #     self.conn.( )()
    #     print("DELETE ALL 완료")

    # 연결 종료
    # def close(self):
    #     self.conn.( )()


# ===========================================================
#  2. Student 메소드 호출하기
# ===========================================================

student = None

# try:
#     student = Student(DB_PATH)

#     student.delete_all()

#     student.insert("뽀로로", 5, 90)
#     student.insert("크롱", 4, 95)

#     student.show_all()

#     # 조회 조건 추가
#     for row in student.select_by_score(92):
#         print(row)

#     student.update_score("뽀로로", 100)
#     student.show_all()

#     student.delete("크롱")
#     student.show_all()

# except sqlite3.Error as e:
#     print("DB 오류:", e)

# finally:
#     # 오류가 나더라도 반드시 connection close하기
#     if student is not None:
#         student.close()

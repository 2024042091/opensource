import sqlite3

# 학생 클래스
class Student:
    def __init__(self, student_id, name, eng, c_lang, python):
        self.student_id = student_id
        self.name = name
        self.eng = eng
        self.c_lang = c_lang
        self.python = python
        self.total = eng + c_lang + python
        self.avg = round(self.total / 3, 2)
        self.grade = self.get_grade()

    def get_grade(self):
        if self.avg >= 90: return 'A'
        elif self.avg >= 80: return 'B'
        elif self.avg >= 70: return 'C'
        elif self.avg >= 60: return 'D'
        else: return 'F'


# 데이터베이스 연동 관리자
class GradeManagerDB:
    def __init__(self, db_name="grades.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                eng INTEGER,
                c_lang INTEGER,
                python INTEGER,
                total INTEGER,
                avg REAL,
                grade TEXT
            )
        ''')
        self.conn.commit()

    def insert(self, student):
        self.cursor.execute('''
            INSERT OR REPLACE INTO students
            (student_id, name, eng, c_lang, python, total, avg, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (student.student_id, student.name, student.eng, student.c_lang,
              student.python, student.total, student.avg, student.grade))
        self.conn.commit()

    def delete(self, student_id):
        self.cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        self.conn.commit()

    def search_by_id(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        return self.cursor.fetchone()

    def search_by_name(self, name):
        self.cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        return self.cursor.fetchall()

    def sort_by_total(self):
        self.cursor.execute('SELECT * FROM students ORDER BY total DESC')
        return self.cursor.fetchall()

    def count_high_scores(self):
        self.cursor.execute('SELECT COUNT(*) FROM students WHERE avg >= 80')
        return self.cursor.fetchone()[0]

    def calculate_ranks(self):
        students = self.sort_by_total()
        rank_dict = {}
        for i, student in enumerate(students):
            student_id = student[0]
            rank_dict[student_id] = i + 1
        return rank_dict

    def print_all(self):
        ranks = self.calculate_ranks()
        self.cursor.execute('SELECT * FROM students ORDER BY total DESC')
        rows = self.cursor.fetchall()
        print("학번\t이름\t영어\tC-언어\t파이썬\t총점\t평균\t학점\t등수")
        for r in rows:
            rank = ranks.get(r[0], '-')
            print(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[5]}\t{r[6]}\t{r[7]}\t{rank}")

    def close(self):
        self.conn.close()


# 메인 실행 함수
def main():
    manager = GradeManagerDB()
    while True:
        print("\n[ 메뉴 ] 1.추가 2.삭제 3.검색(학번) 4.검색(이름) 5.전체출력 6.80점 이상 수 0.종료")
        choice = input("선택: ")

        if choice == '1':
            print("여러 명을 입력할 수 있습니다. 입력을 끝내려면 학번에 'q'를 입력하세요.")
            while True:
                student_id = input("학번: ")
                if student_id.lower() == 'q':
                    break
                name = input("이름: ")
                try:
                    eng = int(input("영어 점수: "))
                    c_lang = int(input("C-언어 점수: "))
                    python = int(input("파이썬 점수: "))
                except ValueError:
                    print("점수는 숫자로 입력해주세요.")
                    continue
                student = Student(student_id, name, eng, c_lang, python)
                manager.insert(student)
                print("학생 정보가 저장되었습니다.")

        
        elif choice == '2':
            student_id = input("삭제할 학번: ")
            manager.delete(student_id)
            print("삭제 완료.")

        elif choice == '3':
            student_id = input("검색할 학번: ")
            result = manager.search_by_id(student_id)
            print("결과:", result if result else "없음")
        
        elif choice == '4':
            name = input("검색할 이름: ")
            results = manager.search_by_name(name)
            print("결과:")
            for r in results:
                print(r)
            if not results:
                print("없음")

        elif choice == '5':
            manager.print_all()

        elif choice == '6':
            count = manager.count_high_scores()
            print(f"80점 이상 학생 수: {count}명")

        elif choice == '0':
            print("종료합니다.")
            manager.close()
            break

        else:
            print("올바른 번호를 선택하세요.")


if __name__ == "__main__":
    main()

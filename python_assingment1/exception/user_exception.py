# path : exception\user_exception.py
# module : exception.user_exception


class EmpNotFoundException(Exception):
    def __init__(self, empid):
        super().__init__(f"사번 '{empid}'에 해당하는 직원 정보가 존재하지 않습니다.")
        self.empid = empid


class InvalidSalaryException(Exception):
    def __init__(self):
        super().__init__("급여는 숫자로 입력해야 합니다.")


class EmpFileNotFoundException(Exception):
    def __init__(self, filename):
        super().__init__(f"파일 '{filename}'을 찾을 수 없습니다. 먼저 저장을 먼저 하세요.")
        self.filename = filename


class InvalidScoreException(Exception):
    def __init__(self):
        super().__init__("점수는 0~100 사이의 숫자로 입력해야 합니다.")


class InvalidIndexException(Exception):
    def __init__(self, idx, length):
        super().__init__(f"순번 {idx}은(는) 유효하지 않습니다. 0 ~ {length - 1} 범위로 입력해야 합니다.")
        self.idx = idx

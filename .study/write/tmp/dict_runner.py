# dict_runner.py
# 파이썬 dict 동작을 종합적으로 검증하기 위한 실행 스크립트.
# 각 섹션의 출력은 블로그 본문에 인용/캡쳐로 들어간다.

import sys
import io
import os
import pickle
import copy
import tempfile
from contextlib import redirect_stdout

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "blog", "img")
OUT_DIR = os.path.normpath(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def section(title):
    bar = "=" * 60
    print(bar)
    print(f"# {title}")
    print(bar)


def run_section(name, fn):
    buf = io.StringIO()
    with redirect_stdout(buf):
        section(name)
        fn()
    text = buf.getvalue()
    print(text, end="")
    log_path = os.path.join(LOG_DIR, f"{name}.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(text)
    return text


# ---------------------------------------------------------------- 1
def s1_create():
    d1 = dict(name="aman", age=33, city="seoul")
    d2 = {"name": "Alice", "age": 30, "city": "New York"}
    d3 = dict([("a", 1), ("b", 2), ("c", 3)])
    d4 = dict(zip(["x", "y", "z"], [10, 20, 30]))
    d5 = dict.fromkeys(["a", "b", "c"], 0)
    print("dict():     ", d1, type(d1).__name__)
    print("literal:    ", d2)
    print("from list:  ", d3)
    print("from zip:   ", d4)
    print("fromkeys:   ", d5)
    # 키 다양성: 해시 가능한 객체면 무엇이든 가능, 리스트는 불가
    mixed = {1: "int key", "a": "str key", (1, 2): "tuple key", 3.14: "float key"}
    print("mixed keys: ", mixed)
    try:
        bad = {[1, 2]: "list key"}
    except TypeError as e:
        print("list key  -> TypeError:", e)


# ---------------------------------------------------------------- 2
def s2_access():
    d = {"a": 1, "b": 2, "c": 3}
    print("d['a'] =", d["a"])
    print("d.get('z') =", d.get("z"))
    print("d.get('z', -1) =", d.get("z", -1))
    try:
        _ = d["z"]
    except KeyError as e:
        print("d['z']  -> KeyError:", e)
    print("'a' in d:", "a" in d)
    print("3 in d.values():", 3 in d.values())
    print("len(d):", len(d))


# ---------------------------------------------------------------- 3
def s3_mutate():
    d = {"a": 1, "b": 2, "c": 3}
    d["a"] = 100             # 갱신
    d["d"] = 4                # 추가
    print("after set/add:", d)

    d.update({"b": 200, "e": 5})
    print("after update :", d)

    val = d.pop("c")
    print("pop('c')     :", val, "->", d)

    last = d.popitem()
    print("popitem()    :", last, "->", d)

    d.setdefault("f", 0)
    d.setdefault("a", 999)    # 이미 있으면 안 바뀐다
    print("setdefault   :", d)

    del d["b"]
    print("del d['b']   :", d)

    d.clear()
    print("clear()      :", d)


# ---------------------------------------------------------------- 4
def s4_views():
    d = {"a": 1, "b": 2, "c": 3}
    keys = d.keys()
    values = d.values()
    items = d.items()
    print("keys  :", keys)
    print("values:", values)
    print("items :", items)
    # 뷰는 딕셔너리 변경을 동적으로 반영한다 (라이브 뷰)
    d["d"] = 4
    print("after add d['d']=4 -> keys :", keys)


# ---------------------------------------------------------------- 5
def s5_order_and_compare():
    # 3.7+ 보장: 삽입 순서를 유지한다
    d = {}
    for k in ["c", "a", "b"]:
        d[k] = ord(k)
    print("insertion order :", list(d.items()))
    # 동등성은 순서와 무관, 키-값 쌍이 같으면 같다
    a = {"x": 1, "y": 2}
    b = {"y": 2, "x": 1}
    print("a == b ?", a == b)


# ---------------------------------------------------------------- 6
def s6_copy():
    src = {"name": "홍길동", "ids": [1, 2, 3]}
    shallow = src.copy()
    deep = copy.deepcopy(src)
    shallow["ids"].append(4)   # 얕은 복사 -> 원본 영향
    deep["ids"].append(99)     # 깊은 복사 -> 원본 무관
    print("src    :", src)
    print("shallow:", shallow)
    print("deep   :", deep)
    print("id same? src vs shallow:", id(src["ids"]) == id(shallow["ids"]))
    print("id same? src vs deep   :", id(src["ids"]) == id(deep["ids"]))


# ---------------------------------------------------------------- 7
def s7_merge_and_or():
    # 3.9+ : | 와 |= 연산자
    a = {"x": 1, "y": 2}
    b = {"y": 20, "z": 30}
    print("a | b :", a | b)            # b 가 이긴다
    a |= {"w": 9}
    print("a |= {} -> a :", a)


# ---------------------------------------------------------------- 8
def s8_comprehension():
    nums = [1, 2, 3, 4, 5]
    sq = {n: n * n for n in nums}
    print("squares:", sq)
    swapped = {v: k for k, v in sq.items()}
    print("swapped:", swapped)
    only_even = {k: v for k, v in sq.items() if v % 2 == 0}
    print("filter :", only_even)


# ---------------------------------------------------------------- 9
def s9_hash_and_sizeof():
    d = {}
    sizes = []
    for i in range(0, 17):
        sizes.append((len(d), sys.getsizeof(d)))
        d[i] = i
    print("len -> sys.getsizeof(dict)")
    for n, sz in sizes:
        print(f"  len={n:>2}  size={sz} bytes")
    print("hash('python') =", hash("python"))
    print("hash(42)       =", hash(42))
    print("hash((1,2,3))  =", hash((1, 2, 3)))
    try:
        hash([1, 2, 3])
    except TypeError as e:
        print("hash(list) -> TypeError:", e)


# ---------------------------------------------------------------- 10
def s10_employee_crud():
    """fileio_mission.py 의 emp_list 기능을 입력 대화 없이 재현."""
    emp_list = {}

    def add(empid, info):
        emp_list[empid] = info

    add("200", ["홍길순", "851225-2234567", "hong@test.com",
                "010-1234-5678", 3800000, "대리", "개발부"])
    add("201", ["김철수", "900101-1234567", "kim@test.com",
                "010-2222-3333", 4200000, "과장", "개발부"])
    add("202", ["이영희", "920510-2345678", "lee@test.com",
                "010-7777-8888", 3500000, "사원", "기획부"])

    print(">> 전체 출력")
    for k, v in emp_list.items():
        print(f"  {k} : {v}")

    print(">> 201 삭제 후")
    del emp_list["201"]
    for k, v in emp_list.items():
        print(f"  {k} : {v}")

    # 파일 저장 / 불러오기 (pickle)
    tmp = os.path.join(tempfile.gettempdir(), "employees.dat")
    with open(tmp, "wb") as f:
        pickle.dump(emp_list, f)
    with open(tmp, "rb") as f:
        loaded = pickle.load(f)
    print(">> pickle round-trip 동등성:", loaded == emp_list)
    print(">> 불러온 키 목록      :", list(loaded.keys()))
    os.remove(tmp)


# ---------------------------------------------------------------- 11
def s11_runtime_error_during_iter():
    """반복 중 사이즈 변경 시 RuntimeError 검증."""
    d = {"a": 1, "b": 2, "c": 3}
    try:
        for k in d:
            if k == "a":
                d["new"] = 0   # 반복 중 변경
    except RuntimeError as e:
        print("RuntimeError:", e)


def main():
    run_section("01_create", s1_create)
    run_section("02_access", s2_access)
    run_section("03_mutate", s3_mutate)
    run_section("04_views", s4_views)
    run_section("05_order", s5_order_and_compare)
    run_section("06_copy", s6_copy)
    run_section("07_merge", s7_merge_and_or)
    run_section("08_comprehension", s8_comprehension)
    run_section("09_hash_sizeof", s9_hash_and_sizeof)
    run_section("10_employee", s10_employee_crud)
    run_section("11_runtime_error", s11_runtime_error_during_iter)


if __name__ == "__main__":
    main()

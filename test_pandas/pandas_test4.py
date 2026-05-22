# path : pandas_test4.py
# 2026-05-22

import pandas as pd
import numpy as np


# DataFrame 인덱스 조작
# 인덱스 라벨(행라벨)이 없는 데이터프레임에 행라벨을 지정하거나 제거하는 것
# 행라벨과 열라벨을 서로 바꿔야 할 떄도 인덱스 조작할 수 있음 (인덱스 교환)
# set_index() 메소드 : 기존의 행 라벨을 제거하고, 데이터 열 중에서 하나를 행 라벨로 설정할 떄 사용한다
#                   열(세로값들) 값들 => 행 인덱스 라벨로 사용
# reset_index() : 기존 행라벨을 제거하고, 인덱스를 열(컬럼) 값들로 추가함
#                   행라벨 => 컬럼값이 됨

np.random.seed(0)

df1 = pd.DataFrame(
    np.vstack( [list('ABCDE'), np.round(np.random.rand(3, 5), 2)] ).T,
    columns=['C1', 'C2', 'C3', 'C4']
) 
#   C1    C2    C3    C4
# 0  A  0.55  0.65  0.79
# 1  B  0.72  0.44  0.53
# 2  C   0.6  0.89  0.57
# 3  D  0.54  0.96  0.93
# 4  E  0.42  0.38  0.07
print(df1)
print("-----------------------------")

# set_index()
df2 = df1.set_index('C1')
print(df2)

print(df2.set_index('C3'))
print("-----------------------------")

# reset_index()
print(df2.reset_index())
print("-----------------------------")

# drop=True 인수를 사용하면, 행인덱스로 변경된 열이 원래 상태로 돌아오지 않고 지워짐
print(df2.reset_index(drop=True))
print("-----------------------------")

# 다중 인덱스 
# 행이나 열에 여러 계층의 인덱스라벨이 지정된 것
# 데이터프레임 생성할 떄 column 인수에 [[], []] 리스트의 리스트(행렬)로 설정하면 됨
np.random.seed(0)
df3 = pd.DataFrame( np.round( np.random.rand(5, 4), 2 ), columns=[ ['A', 'A', 'B', 'B'], ['C1', 'C2', 'C3', 'C4'] ] )
print(df3)

# columns.names 속성
# 다중 인덱스라벨에 이름 지정시 사용함. 이름들은 리스트로 지정함
df3.columns.names = ['Cidx1', 'Cidx2']
print(df3)

# 행라벨도 다중인덱스 적용할 수 있음, 이름도 각각 지정할 수 있음 (index.names 사용)
df4 = pd.DataFrame( np.round( np.random.rand(6, 4), 2 ), 
                   columns=[ ['A', 'A', 'B', 'B'], ['C1', 'C2', 'C3', 'C4'] ], 
                   index=[ ['M', 'M', 'M', 'F', 'F', 'F'], [ 'id_' + str( i + 1 ) for i in range(3) ] * 2 ] )
print(df4)
print("-----------------------------")

df4.columns.names = ['Cidx1', 'Cidx2']
df4.index.names = ['Gidx1', 'Gidx2']
print(df4)
print("-----------------------------")

# 행라벨과 열라벨 교환 : stack(), unstack()
# stack() : 열인덱스라벨 => 행인덱스라벨
print(df4.stack('Cidx1')) # Cidx1 열인덱스라벨이 행인덱스라벨로 이동됨
print("-----------------------------")

# unstack() : 행인덱스라벨 => 열라벨로 변환
print(df4.unstack('Gidx2'))
print("-----------------------------")
# 인덱스 이름(name)
print(df4.unstack(0) )


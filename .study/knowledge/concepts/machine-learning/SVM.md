# SVM

## 한 줄 정의

SVM은 클래스 사이의 간격인 margin을 크게 만드는 결정 경계를 찾는 분류 모델이다.

## 왜 배웠나

선형 경계로 분류하기 어려운 데이터에서 margin, kernel, C, gamma가 모델 복잡도와 일반화에 어떤 영향을 주는지 보기 위해 배웠다.

## 핵심 질문

- margin은 왜 클수록 좋은가?
- support vector는 결정 경계에 어떤 영향을 주는가?
- RBF kernel은 어떤 데이터를 분리할 수 있게 해주는가?
- C와 gamma를 조절하면 과적합 위험이 어떻게 바뀌는가?

## 직접 검증한 것

- circles 데이터에서 선형 모델과 RBF kernel의 차이를 확인했다.
- C와 gamma 조합에 따라 경계가 과하게 구부러지는 현상을 확인했다.
- SVM, KNN, Naive Bayes 실습에서 스케일링과 하이퍼파라미터의 영향을 비교했다.

## 헷갈리는 지점

- C가 크다고 무조건 좋은 것이 아니다.
- gamma가 크면 지역적으로 민감해져 과적합될 수 있다.
- kernel은 데이터를 실제로 눈에 보이는 공간으로 옮긴다기보다, 고차원 유사도를 계산하는 방식에 가깝다.

## 연결 개념

- margin
- kernel trick
- RBF
- scaling
- overfitting
- KNN

## 관련 notes

- `.study/notes/04~05/머신러닝 하이퍼파라미터 최적화 방법 - Google Gemini.mhtml`

## 관련 산출물

- `.blog/day0529_svm.html`
- `.blog/ml_practice03_svm_knn_nb.html`
- `.study/test/svm_intro/`
- `.study/test/ml_practice03/`

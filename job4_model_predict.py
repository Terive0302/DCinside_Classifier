import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model

df = pd.read_csv('./crawling_data/dcinside_1019.csv') # 검증하기 위한 크롤링 데이터
print(df.head())
df.info()

X = df['titles']    # okt객체로 만들어서 형태소 분리해야 할 내용
Y = df['category']  # 형태소 분리한 객체가 정답인지 판단하기 위한 내용

with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
    # 범주형 데이터를 정수형으로 변경한 객체를 파일로 저장한 것을 다시 가져와서 encoder객체 불러옴
labeled_y = encoder.transform(Y)
# fit 트랜스폼을 하면 정보를 새로 가짐, 우리는 정보를 그대로 쓸 것이기 때문에 그냥 트랜스폼
label = encoder.classes_ # 정수형으로 변경했던 것을 다시 범주형으로 보여주는 코드

onehot_y = to_categorical(labeled_y) # 원 핫 인코딩
print(onehot_y) # 각 카테고리마다 이진수가 되어서 분류됨 1 0 0 0 0, 0 1 0 0 0 등...

okt = Okt() # 오늘 받은 뉴스 헤드라인 토큰나이징

for i in range(len(X)): # X는 타겟으로 한 내용이 담긴 데이터프레임
    try:
        X[i] = okt.morphs(X[i], stem=True)
    except:
        print("error {}".format(X[i]))
    # X[i]에 들어온 텍스트를 형태로 단위로 분석
    # stem=True 옵션을 통해 어간 형태로 변경
    # stem = True를 주면 원형으로 바꿔줌 (하다)
    # stem = True를 안주면 동사 변형(하며 하는 하니 등)으로 되므로 학습이 잘 안됨
    # try - except 구문을 넣어 NaN값 또는 이상치를 배제하기 위해 사용

stopwords = pd.read_csv('./stopwords.csv', index_col=0) # 불용어 csv파일을 불러옴

#불용어 제거
for j in range(len(X)): # X는 타겟 내용 데이터프레임, "타겟의 갯수"만큼 반복
    words = []
    for i in range(len(X[j])):  # 타겟 데이터프레임의 인덱싱, 그 안에 들어있는 "타겟 텍스트 길이"만큼 반복
        if len(X[j][i]) > 1:  # 1글자 초과 조건문 / 1글자짜리 단어는 제외
            if X[j][i] not in list(stopwords['stopword']):  # 불용어 파일에 없는 단어
                words.append(X[j][i])  # 그 단어들만 추가
    X[j] = ' '.join(words)  # 불용어를 제외하고 남은 단어들만 추가되어 하나의 문장이 됨

#불용어 제거한 후 토큰나이징
with open('./models/dc_token.pickle', 'rb') as f:
    token = pickle.load(f) # 저장된 토큰객체를 불러와서 변수에 저장

tokened_x = token.texts_to_sequences(X) # 타겟 내용 각 텍스트를 단어 인덱스로 변환한 결과 저장

for i in range(len(tokened_x)): # 토큰화된 텍스트 데이터에서 가장 긴 길이를 찾는 구문
    if len(tokened_x[i]) > 11: # 가장 긴 길이보다 가져온 텍스트 데이터가 길다면
        tokened_x[i] = tokened_x[i][:12] # 길이를 잘라줌
x_pad = pad_sequences(tokened_x, 11) # 짧은 문장을 가장 긴 길이만큼 만들어주기 위해 0을 채워줌

model = load_model('./models/dcinside_category_classification_model_0.6155555844306946.h5')
# 학습된 모델 데이터를 불러옴
preds = model.predict(x_pad) # 패딩된 데이터에 대한 예측을 수행하고 변수에 저장
predicts = []
for pred in preds: # 검증 데이터를 예측한 결과 갯수만큼 반복
    most = label[np.argmax(pred)] # 각 검증 데이터의 가장 큰 확률을 변수에 저장
    pred[np.argmax(pred)] = 0 # 예측값중에 가장 큰 값의 인덱스를 0으로 초기화, 다시 argmax하면 두번째가 첫번째가 됨
    second = label[np.argmax(pred)] # 두번째로 큰 확률을 변수에 저장
    predicts.append([most, second]) # 첫번째와 두번째 결과를 빈 리스트에 저장
df['predict'] = predicts # 이를 원본 데이터 프레임에 저장
print(df.head(30))

# 다시 한 번 정확도 계산
df['OX'] = 0
for i in range(len(df)): # 검증 데이터 프레임의 각 행만큼 반복
    if df.loc[i, 'category'] in df.loc[i, 'predict']: # 각 카테고리 행과 예측결과 행이 같다면
        df.loc[i, 'OX'] = 'O' # O로 출력
    else:
        df.loc[i, 'OX'] = 'X' # 틀리면 X로 출력
print(df['OX'].value_counts()) # O와 X의 갯수 출력
print(df['OX'].value_counts()/len(df)) # O와 X의 퍼센트 출력
for i in range(len(df)): # 틀린것만 출력하는 구문
    if df['category'][i] not in df['predict'][i]:
        print(df.iloc[i])
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle


pd.set_option('display.unicode.east_asian_width', True)
# 한국어 맞춤 글자 폭 으로 세팅
df = pd.read_csv('../crawling_data/dcinside_20231019.csv')
# csv파일을 읽음
# print(df)
# print("------------------------------")
# df.info()
# print("------------------------------")

X = df['titles']    # okt객체로 만들어서 형태소 분리해야 할 내용
Y = df['category']   # 카테고리

print(X) # 본문 내용이 출력됨
print("----------------------------------------")
print(Y) # 카테고리가 출력됨

encoder = LabelEncoder() # 범주형 데이터를 정수형으로 변경해주는 클래스
labeled_y = encoder.fit_transform(Y)
# fit 트랜스폼하면 일반 0, 소식 1, 후기 2, 팁 3, MOD 4로 바뀜
print(labeled_y[:], "카테고리로 나눈 것들")
label = encoder.classes_ # 정수형으로 변경했던 것을 다시 범주형으로 보여주는 코드
print(label, "카테고리 출력")

with open('../models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)
    # 범주형 데이터를 정수형으로 변경한 객체를 파일로 저장
    # 이 파일을 열어 encoder객체를 다시 가져오기 위해 사용

onehot_y = to_categorical(labeled_y) # 원 핫 인코딩
print(onehot_y)

okt = Okt() # Open korea text 한국어 형태소 분석 클래스 객체 만들기

# # test
# # print(okt.morphs(X[102], stem=True), "테스트를 위한 형태소")

for i in range(len(X)): # X는 본문 데이터프레임
    # okt_morph_x = okt.morphs(X[0], stem = True)
    try:
        X[i] = okt.morphs(X[i], stem=True)
    except:
        print("error {}".format(X[i]))

    # X[i]에 들어온 텍스트를 형태로 단위로 분석
    # stem=True 옵션을 통해 어간 형태로 변경
    # stem = True를 주면 원형으로 바꿔줌 (하다)
    # stem = True를 안주면 동사 변형(하며 하는 하니 등)으로 되므로 학습이 잘 안됨
print(X[i], "\nOKT 프린팅")

# 전처리 / stopword, 불용어 제거
stopwords = pd.read_csv('../stopwords.csv', index_col = 0)
for j in range(len(X)): # X는 본문 데이터프레임, 본문의 갯수만큼 반복
    words = []
    try:
        for i in range(len(X[j])):  # 본문 데이터프레임의 인덱싱, 그 안에 들어있는 텍스트 길이만큼 반복
            if len(X[j][i]) > 1:  # 1글자 이상 조건문
                if X[j][i] not in list(stopwords['stopword']):  # stopwords csv파일에 없는 단어
                    words.append(X[j][i])  # 그 단어들만 추가
        X[j] = ' '.join(words)
    except:
        print("error {}".format(j))
for i in range(3):
    print(X[i])
    print('\n')

    # 오류 잡음, 타이틀만 있는 건 오류 없었음
# X = [str(x) for x in X]

token = Tokenizer()
token.fit_on_texts(X)
tokened_x = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1
print(tokened_x[:])
print(wordsize, "워드사이즈입니다.") # 13270, 2508

with open('../models/dc_token.pickle', 'wb') as f:
    pickle.dump(token, f) # 토큰을 f에다 저장

max = 0
for i in range(len(tokened_x)):
    if max < len(tokened_x[i]):
        max = len(tokened_x[i])
print(max, "맥스사이즈입니다.") # 990, 11

x_pad = pad_sequences(tokened_x, max) # 문장을 주고, 길이를 주면 모자란 갯수만큼 0을 채워줌
# , padding='post', truncating='post' options
print(x_pad[:])

X_train, X_test, Y_train, Y_test = train_test_split(
    x_pad, onehot_y, test_size=0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('../crawling_data/dcinside_data_max_{}_wordsize_{}'.format(max, wordsize), xy)
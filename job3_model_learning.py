import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *

X_train, X_test, Y_train, Y_test = np.load(
    './crawling_data/dcinside_data_max_11_wordsize_2508.npy', allow_pickle=True)
# 전처리하여 Numpy 배열 형식으로 저장된 데이터를 불러옴,
# pickle옵션을 통해 Numpy 배열 이외에 파이썬 객체를 포함하는 파일을 불러올 수 있도록 함 -> 변수 4개에 저장
print(X_train.shape, Y_train.shape) # 제대로 저장이 되었다면 데이터셋 크기는 같을 것임
print(X_test.shape, Y_test.shape)   # 이를 확인하기 위한 출력

model = Sequential() # 시퀀스 모델 생성, 레이어를 순차적으로 쌓는 방식의 모델임
model.add(Embedding(2508, 300, input_length=11))
# 단어들을 단어 갯수만큼의 차원을 가지는 공간상의 배치 워드사이즈가 2508
# 300은 차원 축소
# 입션 시퀀스의 길이 / 맥스 사이즈 길이 11
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu'))
# 문장은 한줄 1차원이니까 1D를 씀, 필터 32개
model.add(MaxPooling1D(pool_size=1))
# 풀 사이즈 1이므로 아무 일도 일어나지 않음, 빼도 되는 레이어지만 Conv레이어를 써주면 같이 써주는게 좋음
model.add(LSTM(128, activation='tanh', return_sequences=True))
# 순서에 따른 학습을 위해 LSTM, 순차적인 정보 학습
# return_sequences=True 모든 시퀀스 출력 반환, 하나 들어갈 때마다 저장, 이게 없으면 맨 마지막 출력만 내놓음
model.add(Dropout(0.3)) # 과적합 방지를 위해 일부 뉴런을 랜덤하게 비활성화
model.add(LSTM(64, activation='tanh', return_sequences=True))
# 다음에 LSTM이 있으니 리턴 시퀀스 True
model.add(Dropout(0.3))
model.add(LSTM(64, activation='tanh'))
# 다음 LSTM없으니 리턴 시퀀스 없음
model.add(Dropout(0.3))
model.add(Flatten()) # 필터가 사용되면 다차원이 되므로 이를 다시 1차원으로 변경
model.add(Dense(128, activation='relu'))
model.add(Dense(5, activation='softmax')) # 카테고리 갯수만큼 레이어 [ 5 ], 다중 클래스 분류를 위해 softmax
model.summary() # 모델 정보 출력

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# 손실 함수 설정 loss='categorical_crossentropy'
# 가중치 알고리즘 설정 optimizer='adam'
# 모델 평가 지표 설정 metrics=['accuracy'], accuracy지표는 모델의 정확도 측정
fit_hist = model.fit(X_train, Y_train, batch_size=25, epochs=50, validation_data=(X_test, Y_test))
# 학습시킬 데이터가 약 2500개밖에 안되므로 batch_size = 25, 대신 50번 돌 수 있도록 함
# 데이터 검증을 위해 만들었던 X_test와 Y_test를 사용
model.save('./models/dcinside_category_classification_model_{}.h5'.format(fit_hist.history['val_accuracy'][-1]))
# 학습된 모델을 저장, 학습 모델의 정확도를 같이 저장되도록 함
plt.plot(fit_hist.history['val_accuracy'], label='validation accuracy') # 모델의 학습률을 시각화하여 출력
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.legend()
plt.show()
# Experiment Reproduction(SemiSeg with CPS)
Semi Supervised Semantic Segmentation with Cross Pseudo Supervision

- Paper : https://arxiv.org/abs/2106.01226

- Code : https://github.com/charlesCXK/TorchSemiSeg

## 1. 배경
- Semantic Segmentation은 컴퓨터 비전에서 기본적인 Recognition 작업으로, Semantic segmentation 훈련 데이터는 픽셀 수준의 라벨링하는 절차가 필요하며, 이는 Image Classification과 Object Detection과 같은 다른 비전 작업에 비해 훨씬 많은 비용이 소모되는 단점을 가진다.
- 그러기 때문에, 라벨이 지정된 데이터와 라벨이 지정되지 않은 추가 데이터를 사용하여 segmentation모델을 학습시키는 Semi Supervised Segmentation을 연구가 필요로 하게 되었다.

## 2. 연구 설명
- 동일한 구조를 가지지만 다르게 초기화된 두 Segmentation Network에 대해 라벨을 가진 이미지와 가지지 않는 이미지를 제공하여, 우선 라벨을 가진 이미지를 두 Network에 거쳐 각각 Ground truth segmentation map을 이용해 supervise한다.
- 여기서 주요포인트인 Cross Pseudo Supervision을 제시하여, 각 Segmentation Network는 이미지를 입력받으면 Pseudo segmentation map을 리턴하는데, 리턴받은 map을 활용하여 다른 Segmentation network를 supervise하는데 사용된다.

## 3. 연구 방법
- 라벨을 가지는 데이터셋과 라벨을 가지지 않는 데이터셋이 각각 주어지며, Semi supervised semantic segmentation는 주어진 모든 이미지를 탐색하여 Segmentation Network를 학습하는 것을 목표로 한다.
### 1) 데이터셋
  |Dataset|Class|Labeled|Unlabeled|Val|Etc|
  |------|------|------|------|------|------|
  |PASCAL VOC 2012|21(배경포함)|1323(1/8)|9259(7/8)|1449|JPG|
  |Cloud Open Dataset|4(배경포함)|163(1/16)|2452(15/16)|320|JPG, NIR제거|<br><br>
- PASCAL VOC 2012 : JPG로 된 이미지로, 20개의 객체 클래스와 1개의 배경 클래스를 가진다. 10,582개의 학습 데이터 중 1/8에 해당하는 1323개는 라벨을 가지는 이미지로, 나머지 9259개는 라벨을 가지지않는 이미지로 활용한다. 검증용 이미지는 1449개의 이미지를 사용한다.
- Open_Dataset : 4채널(+NIR) TIF로 된 이미지를 3채널 JPG로 변경한 것으로, 3개의 객체 클래스(두꺼운 구름, 얇은 구름, 그림자)와 1개의 배경 클래스를 가진다.  130개의 학습 데이터를 1024x1024로 나눈 2615개의 학습 데이터 중 1/16에 해당하는 163개는 라벨을 가지는 이미지로, 나머지 2452개는 라벨을 가지지않는 이미지로 활용한다.  검증용 이미지는 1024x1024로 나눠진 320개를 가진다. 
### 2) 공통된 설정
  |Dataset|Class|
  |------|------|
  |Model Architecture|Evaluation Metric|
  |Optimizer|Mini Batch SGD|
  |Momentum|0.9|
  |Weight decay|0.0005|
  |Evaluation Metric|mIoU|<br><br>
### 3) 차별된 설정 : Cross Pseudo Supervion

## 4. 연구 결과
### 1) CPS vs Only Supervised
### 2) 기타 결과 

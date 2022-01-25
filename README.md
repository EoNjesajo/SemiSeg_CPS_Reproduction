# Experiment Reproduction and Review(SemiSeg with CPS)
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
![11](https://user-images.githubusercontent.com/90492809/150950613-1c2b5a15-4a34-469e-a42b-3a9ff1d882fb.png)
- 두 개의 Parallel Segmentation Network로 구성된다. 두 네트워크는 동일한 구조를 가지지만, 가중치(θ1, θ2)은 다르게 초기화 된다.

![Parallel Segmentation Network](https://user-images.githubusercontent.com/90492809/150950958-1f0372f9-a153-40e1-966a-03949c69ed9f.png)
- 입력 X에는 동일한 증대가 적용되며, P는 Softmax normalization을 거친 후 network 출력인 Segmentation confidence map이고, Y는 pseudo segmentation map이라 불리는, One-Hot label Map이다.

![structure](https://user-images.githubusercontent.com/90492809/150951044-c9477eef-c949-4ebb-a5fa-9bc1cc33874c.png)
- Supervision loss는 두 개의 Parallel Segmentation Network를 통해 라벨이 지정된 이미지에 대해 표준 픽셀 단위 Cross Entropy Loss(lce)를 사용한다. y*i는 Ground Truth, W와 H는 각각 입력이미지의 너비와 높이를 나타낸다.

<img width="400" alt="supervised loss" src="https://user-images.githubusercontent.com/90492809/150951736-bf44422f-98c1-43a5-a927-cd4079b6f7c1.png">
- Cross Pseudo Supervision loss는 양방향이다. 첫 번째는 f(θ1)에서 f(θ2)로, f(θ1)에서 출력된 label map인 Y1을 사용하여 f(θ2)의 픽셀 단위 confidence map인 P2를 supervise한다. 두 번째는 f(θ2)에서 f(θ1)이다. 라벨이 지정되지 않은 데이터에 대한 CPS는 아래와 같이 작성되며, 같은 방식으로 라벨이 지정된 CPS도 정의된다.

<img width="400" alt="CPS loss" src="https://user-images.githubusercontent.com/90492809/150951641-aa4a2726-31ed-4749-96c8-2d8ebb8bdc39.png">
- 그래서 최종 Loss는 다음과 같이 작성된다.(λ는 trade-off 가중치를 의미한다.)

![final loss](https://user-images.githubusercontent.com/90492809/150951835-c2e82c46-f407-4fb6-a0fe-bc60313b856d.png)


## 4. 연구 결과
### CPS vs Only Supervised
  |Loss(super)|Loss(super)|PASCAL VOC 2012|Open_Dataset|
  |------|------|------|------|
  |✓||69.183%|51.792%|
  |✓|✓|71.028%|51.792%|<br><br>
- Cross Pseudo Supervision Loss을 적용하면 Supervision Loss만 적용한 결과보다 개선된다는 것을 알 수 있다. Coss Pseudo supervision Loss은 PASCAL VOC 2012에서 1.85%로, 논문에서의 향상(3.77%)보다는 저조한 결과지만 향상된 것을 확인할 수 있다.
- Open_Dataset은 얇은 구름 외 클래스는 개선을 보인 반면, 얇은 구름은 Baseline(IoU 약10~14%) 비해 낮은 결과(약2~3%)의 결과를 보인다. 
- 그 외 구름 데이터셋에서 나타난 공통적인 특징은 IoU가 낮은 클래스에 대해 성능이 감소하는 것을 확인할 수 있다.
- Open Dataset 시각화 결과(image, GT, CPS, BaseLine)
![result](https://user-images.githubusercontent.com/90492809/150952699-01caf552-7593-4763-9301-a03aadf20195.png)

## 5. 평가
- 라벨을 가지지 않은 이미지를 사용해서 성능을 개선할 수 있는 방법이지만, 본 실험에서는 큰 개선 결과는 보이지 못했다.
- 특히, IoU가 낮은 클래스에 대해서는 CPS에서 성능이 하락되게 되는데, 이는 라벨을 가진 이미지로 학습된 네트워크의 출력 결과로 해당 클래스에 대한 알맞지 않은  Pseudo segmentation map을 제공하고, 이를 통해 다른 네트워크에 대해 supervise하기 때문이라고 추측할 수 있다.
- 그렇기 때문에, 모든 클래스에서 충분한 IoU를 갖추고, 라벨을 가지지 않는 이미지를 충분히 제공한다면 성능 향상에 도움이 될 것이다.
- 장점 : 라벨을 가지지 않는 이미지를 통해 라벨링에 필요한 비용 소모 없이 성능 향상을 시킬 수 있다.
- 단점 : 라벨을 가지지 않는 이미지더라도 많은 양의 이미지를 필요로 하며, supervised에서 저조한 IoU를 가진 클래스에 대해서는 성능하락을 보인다. 

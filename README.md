# WorkerModel

Crowdsourcing에서 true label을 얻기 위해서는 여러 worker들이 각 task들에 할당한 label들을 수집해 true label을 추정함

하지만, 모든 worker들이 task에 정확하게 label을 부여하지는 않기 때문에 WorkerModel을 설계할 필요가 있음

가장 단순한 방법인 MV 방법과 MV의 단점을 보완한 BP, EM 알고리즘을 사용해 WokerModel을 구현

## MV(Majority Voting)

각 task들에 대해 할당된 worker들이 부여한 label 중 가장 많은 worker들이 선택한 label을 true label로 사용함

Worker들의 reliability를 고려하지 않고, 모든 worker들을 동일하게 취급하기 때문에 가장 단순한 방법이지만 정확도가 떨어지는 단점이 존재함

## BP(Belief Propagation)

Worker를 factor로 지정하고 task를 variable로 지정해서 factor graph를 생성함

매 iteration마다 아래와 같이 message를 전달함
$$
\large m_{i\rightarrow u}^{t+1}(s_i)\propto\Pi_{v\in M_i\text{\\}\{u\}}m_{v\rightarrow i}^t(s_i)
$$
Task $$i$$에서 worker $$u$$에게 message를 전달함, 즉, $$u$$의 reliability를 update함

이 값은 이전 time step $$t$$에서 $$i$$가 연결된 worker들에게 받은 message 값들의 product로 추정함
$$
\large m_{u\rightarrow i}^{t+1}(s_i)\propto\sum_{s_{N_u\text{\\}\{i\}}}f_u(s_{N_u})\Pi_{j\in N_u\text{\\}\{i\}}m_{j\rightarrow u}^{t+1}(s_j)
$$
Worker $$u$$에서 task $$i$$에게 message를 전달함, 즉, $$i$$의 label을 update함

이 값은 time step $$t+1$$에서 $$u$$가 연결된 task들에게 받은 message와 factor 값의 곱의 sum으로 추정함
$$
\large b_i^{t+1}(s_i)\propto\Pi_{u\in M_i}m_{u\rightarrow i}^{t+1}(s_i)
$$
Task들의 belief를 update함, 즉, 각 task들의 label의 확률들이 어느정도의 신뢰성이 있는지를 추정함

이 값은 time step $$t+1$$에서 $$i$$가 연결된 worker들에게 받은 message 값들의 product로 추정함
$$
\large \hat{s}_i^{(k)}=argmax_{s_i}b_i^k(s_i)
$$
$$k$$번의 iteration 후의 task $$i$$의 label은 $$i$$의 belief $$b_i^k$$를 최대화하는 값으로 할당함

## EM(Expectation Maximization)

Prior인 worker들의 reliability $$p_u$$가 beta distribution을 따른다고 가정함

### E-step

E-step에서는 아래와 같이 $$p_u$$를 고정시키고 $$s_i$$의 확률을 추정함
$$
\large \mathbb{P}(s_i\mid A,p)\propto\Pi_{u\in W_i}\:p_u^{1[A_{iu}=s_i]}(1-p_u)^{1[A_{iu}\neq s_i]}\\
W_i:\text{ workers assigned to task, }i\\
A_{iu}:\text{assigned label of task, }i\text{, by worker, }u\\
s_i:\text{label of task, }i
$$
Task $$i$$의 label은 다음과 같이 추정함
$$
\large \hat{s}_i(A,p)=argmax_{s_i}\Pi_{u\in W_i}\: \mathbb{P}(s_i\mid A,p)
$$

### M-step

M-step에서는 E-step에서 계산한 $$s_i$$의 확률을 사용해 새로운 $$\hat{p_u}$$를 추정함
$$
\large \hat{p_u}=\frac{\sum_{i\in N_u}\mathbb{P}(A_{iu})+\alpha-1}{\mid N_u\mid+\alpha+\beta-2}\\
N_u:\text{ tasks assigned to worker, }u\\
\mathbb{P}(A_{iu})=\mathbb{P}(s_i=1),\text{ if }A_{iu}=1\\
\mathbb{P}(A_{iu})=\mathbb{P}(s_i=2),\text{ if }A_{iu}=2
$$
추정한 값을 통해 worker $$u$$의 reliability를 update함

## Data

각 worker에 연결된 task의 수 $$r$$에 변화를 주는 SYN dataset과 각 task에 연결된 worker의 수 $$l$$에 변화를 주는 SIM dataset을 사용

**대학 과목의 project에 사용했던 data이기 때문에 data는 공개하지 않음**

## 결과

![SYN_data](./images/SYN.PNG)

SYN dataset에서는 각 worker에 연결된 task 수 $$r$$을 $$[1,3,5,7,9,11,13]$$으로 변화시키며 MV, BP, EM 알고리즘에 대해 error rate를 측정함

$$r$$이 증가해도 MV 알고리즘의 성능은 향상되지 않는 것을 확인

BP와 EM 알고리즘은 $$r$$이 증가할 수록 성능이 향상됨

![SIM_data](./images/SIM.PNG)

SIM dataset에서는 각 task에 연결된 worker 수 $$l$$을 $$[1,5,10,15,20,25]$$으로 변화시키며 MV, BP, EM 알고리즘에 대해 error rate를 측정함

BP 알고리즘을 naive하게 구현해서 $$l$$이 증가하면 시간이 오래걸려 BP 알고리즘에 대해서는 $$l$$이 $$[1,5]$$ 일 때만 error rate를 측정함

$$l$$이 증가하면 MV 알고리즘을 포함해 모두 성능은 향상되는 것을 확인


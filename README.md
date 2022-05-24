## **: Join sports⚽**

---

딥러닝을 접목하여 사진을 인식하고 그것을 토대로 같은 스포츠 관심사를 가진 사람들을 매칭해주는 사이트 

### 팀원소개

- 이민기
- 최재완
- 김하진
- 백선영

### 기술

**HTML, CSS, JavaScript, FLASK, TensorFlow, Keras, Convolution Neural Network,** 

**Transfer Learning, Github, MongoDB, YOLO5**

### Mockup

👇클릭!

![스크린샷 2022-05-18 오후 2.52.00.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b1deccab-e369-417c-8446-6edea3e77674/스크린샷_2022-05-18_오후_2.52.00.png)

### Position

- Front End
    - Login Page, Join Page, Main Page, Member Page Design

- Back End
    - Login, Join, Main, Deep Learning, Image Processing, MongoDB CRUD, YOLO5

- Front - Login.html , Join.html
- Back - Login , Join
    - 백선영

- Front - MainPage.html , Modal_page, Event page
- Back - Modal,Modal Comment
    - 이민기

- 모델 학습, Deep Learning, YOLO5
    - 김하진, 최재완
    
- Back - Main Page(API), Event  Page(API)
    - 김하진, 최재완

### Mongo DB

| Collection | Table |
| --- | --- |
| User
(회원가입 유저 정보) | _id : PK
email : String (이메일형식)
nick : String (닉네임)
pwd : String (SHA256 해시값)
pr_photo : String (파일 경로)
pr_desc : String (유저 소개)
category : String (분류명) |
| Photo
(이미지 등록) | _id : PK
photo : String (파일경로)
category : String (분류명) |
| Comment
(방명록 등록) | _id : PK
comment_id : String (작성한곳 유저 아이디)
comment_nick : String (해당 가입자 닉네임)
comment_desc : String (코멘트 내용)
comment_time : 분단위 (date_time) |
| slide_photo | _id : PK
photo : String (파일경로)
category : String (분류명) |

### API

| Method | End Point | request | return | DB |
| --- | --- | --- | --- | --- |
| GET | /join_page |  | Join.html |  |
| GET | /login_page |  | Login.html |  |
| POST | /join | ‘email’ : email
’pwd’ : pwd
’nick’ : nick
’pr_photo’ : pr_photo | {
‘result’ : ‘success’,
’result’: ‘fail’
} | {
’email’ : email,
’pwd’ : pwd(hash),
’nick’ : nick,
’pr_photo’ : pr_photo,
’pr_desc’ : ‘’,
’category’ : baseball
      (딥러닝 검증결과에 따라 다름)
} |
| POST | /login | ‘email’ : email
’pwd’ : pwd | { 
‘result’ : ‘success’,
’result’: ‘fail’,
‘photo’ : photo
} |  |
| GET | /main |  | { 
‘result’ : ‘success’,
‘my_data’ : my_data, 
‘member_data’ : member_data,
‘slide_photo’ : slide_photo,
 } |  |
| GET | /soccer |  | { 
‘result’ : ‘success’,
’members_data’: members_data
} |  |
| GET | /baseball |  | { 
‘result’ : ‘success’,
’members_data’: members_data
} |  |
| GET | /basketball |  | { 
‘result’ : ‘success’,
’members_data’: members_data
} |  |
| GET | /volleyball |  | { 
‘result’ : ‘success’,
’members_data’: members_data
} |  |
| POST | /modal | ’member_id’: member_id | { 
‘result’ : ‘success’,
’member_data’: member_data,
’comment’: comment
} |  |
| POST | /my_desc_edit | ’pr_desc’: pr_desc | {‘result’ : ‘success’} |  |
| POST | /my_photo_edit | ‘pr_photo’: pr_photo | {‘result’ : ‘success’} |  |
| POST | /comment | ‘comment_desc’: comment_desc | {‘result’ : ‘success’} |  |

### 참고 Datasets

- [https://www.kaggle.com/datasets/gpiosenka/sports-classification](https://www.kaggle.com/datasets/gpiosenka/sports-classification)
- [https://www.kaggle.com/datasets/fabrciohenrique/soccer-images](https://www.kaggle.com/datasets/fabrciohenrique/soccer-images)
- [https://www.kaggle.com/datasets/sankalp1999/sportsclassiferimproveddataset](https://www.kaggle.com/datasets/sankalp1999/sportsclassiferimproveddataset)
- [https://www.kaggle.com/datasets/gpiosenka/balls-image-classification](https://www.kaggle.com/datasets/gpiosenka/balls-image-classification)

### D**eadLine**

| Apportion | DeadLine |
| --- | --- |
| Front Page (Login.html,Join.html,Main.html,Modal popup, Event Modal popup) | 5/23 12:00 까지 작업완료 |
| Back end (Login, Join, Main(CRUD), Category, Comment) | 5/23 12:00 까지 작업완료 |
| YOLO5 Keras 데이터 수집 및 검증 작업 | 5/20 19:00 까지 작업완료 |
| 데이터 검증 및 서버 및 클라이언트 테스트 | 5/20 19:00 학습 중간 테스트 |
| 최종 테스트 | 5/24 17:00 최종 테스트 |

YOLO5

![yolo5.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d1406979-c530-407c-a194-c386aae2df9e/yolo5.png)

[https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5)

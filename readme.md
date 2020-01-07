# IDOL 랭킹 예측 사이트
인기인/아이돌에 대한 인기 차트를 수집해, 랭킹을 시각화하고 수집된 데이터를 바탕으로 향후
인기도에 대해 tensorflow, LSTM 모델링을 통해 예측하는 프로젝트

## 폴더, 파일 구조

 - _compose : 기본 폴더. django+python 관련 빌드 이미지 포함
 - _config : ngynx 설정 config 
 - _mysql : mysql 이미지 빌드시 자동 생성되며, db 실제 데이터가 저장됨.
 - django_app : django 관련 전체 사이트 설정
 - static : django 이미지 빌드시 자동생성돼 마운트 됨. django 용 static 파일
 - media : django 이미지 빌드시 자동생성돼 마운트 됨. django 용 media 파일
 - templates : django 프로젝트를 위해 추가한 폴더. 사이트 베이스 템플릿 html 등
 - web_crawl : 웹크롤링 수집 관련 파이썬 파일 및 딥러닝 모델
 - 기타 폴더 : django 프로젝트를 위해 추가한 폴더. 사이트 베이스 템플릿 등
 - 루트 파일 :
   * docker-compose.yml : docker-compose 를 사용해 이미지를 빌드하고 관리.
   * requirements.txt : docker를 이용한 이미지 설치시 python 라이브러리 설치용

  #### 작업시 주의 사항
  ```
   # django_app 폴더내의 파일들은 docker-compose images 에 포함되는 부분으로
   # 수정됐을 경우 아래 명령을 사용해 빌딩해주어야 함.
   docker-compose down
   docker-compose up -d --build
   ```

----

## 가상환경 생성 및 설치

1. python 가상환경 venv 생성 및 활성화
```
# python 가상환경 venv 로 만들기
python -m venv C:\Study\project_idol\venv

# python 가상환경 venv 실행하기
C:\Study\project_idol\venv\Scripts\activate.bat

# python 가상환경 venv 비활성화 하기
C:\Study\project_idol\venv\Scripts\deactivate.bat
```
2. pip 설치 및 의존성 패키지 requirements.txt 생성
```
# pip 업그레이드
python -m pip install --upgrade pip

# pip 으로 의존성 패키지 리스트 목록화 하기
pip freeze > requirements.txt

# pip 으로 의존성 패키지 한번에 설치하기
pip install -r requirements.txt

#**** 프로젝트 파일의 실행경로가 달라지는 경우 venv/Scripts/acvate.bat 파일 수정
# 11라인에서 수정 --> set "VIRTUAL_ENV=C:\Study\project_idol\venv"
```
----

## django 프로젝트 생성 및 관리
1. django 프로젝트 초기화
```
# django 프로젝트 초기화
// django-admin startproject django_app ./djangoIdol
django-admin startproject django_app .

# django 사이트 관리자 생성
python manage.py createsuperuser
```
2. 작업순서
- settings.py
- models.py
- urls.py
- views.py
- templates

3. 설정 변경 후 실행
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
----

## Docker 및 Docker-compose 관리
1. docker desktop for windows 2.1.7.0 버전 이상 설치
<https://download.docker.com/win/edge/41561/Docker%20Desktop%20Installer.exe>

2. cmd 를 관리자 권한으로 실행

3. docker-compose 가 있는 프로젝트 폴더로 이동

4. 아래 명령어 실행
```
docker-compose up -d
   -d: 서비스 실행 후 콘솔로 빠져나옵니다. (docker run에서의 -d와 같습니다.)
   --force-recreate: 컨테이너를 지우고 새로 만듭니다.
   --build: 서비스 시작 전 이미지를 새로 만듭니다.
```
5. docker-compose 관련 명령
```
1) 서비스 상태 확인
docker-compose ps

2) 서비스 시작-종료
docker-compose start
docker-compose stop

3) docker compose images 다시 빌드
docker-compose build
docker-compose up

4) 서비스 삭제. 컨테이너와 네트워크를 삭제
docker-compose down
docker-compose down --volume   # 볼륨까지 삭제

5) 실행중 컨테이너에서 명령어 실행. 자동화된 마이그레이션용 파일 생성이나 유닛 테스트, lint 등을 실행할 때 사용
docker-compose exec app python ./manage.py makemigrations

6) 서비스 로그 확인. logs 뒤에 서비스 이름을 적지 않으면 도커 컴포즈가 관리하는 모든 서비스의 로그 보여줌.
docker-compose logs django
```

6. Docker-compose 로 django 명령어 사용
```
docker-compose exec app python ./manage.py createsuperuser
```

#### 자세한 내용은 아래 링크 참고
<https://www.44bits.io/ko/post/almost-perfect-development-environment-with-docker-and-docker-compose>

#### docker 관련 명령어
- 프로세스 확인 : docker ps
- 컨테이너 삭제 : docker rm 프로세스ID
- 컨테이너 강제 삭제  : docker rm -f 프로세스ID
- 이미지 확인 : docker images
- 이미지 삭제 : docker rmi 이미지ID
- 이미지 강제 삭제  : docker rmi -f 이미지ID

from django.test import TestCase, Client
from bs4 import BeautifulSoup

from .models import Post, Category, Tag
from django.contrib.auth.models import User

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        '''
        기본적으로 설정되어야 하는 내용을 적는 함수
        Client() 사용
        user, category 설정
        포스트 3개 작성
        :return:
        '''
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')
        # 권한 부여
        self.user_obama.is_staff = True
        self.user_obama.save()

        self.category_programming = Category.objects.create(name='PROGRAMMING', slug='programming')
        self.category_java = Category.objects.create(name='JAVA', slug='java')

        self.tag_python_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')

        self.post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World, We are the world.',
            category=self.category_programming,
            author=self.user_obama,
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='콩',
            category=self.category_java,
            author=self.user_trump,
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트입니다.',
            content='카테고리 없음',
            author=self.user_trump,
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)



    def test_post_list(self):
        '''
        포스트 리스트에 포스트가 제대로 있는지 확인
        :return:
        '''
        # 포스트가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag.python_kor.name, post_001_card.text)
        self.assertNotIn(self.tag.python.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag.python.name, post_002_card.text)
        self.assertNotIn(self.tag.python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag.python_kor.name, post_003_card.text)
        self.assertIn(self.tag.python.name, post_003_card.text)


        # 작성자명 대문자로 변환
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)


    def test_post_detail(self):
        '''
        포스트 디테일
        url에 제대로 접근되는지 확인
        리스트 목록 페이지와 똑같은 내비게이션 바
        등등등....
        :return:
        '''
        # 1.2 그 포스트의 url은 '/blog/1/' 이다
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2 첫 번째 포소트의 상세 페이지 테스트
        # 2.1 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다(status code: 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다
        self.navbar_test(soup)
        self.category_card_test(soup)
        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다
        self.assertIn(self.post_001.title, soup.title.text)
        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)
        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다 (아직 구현 못 함, author 필드를 안 만듦)
        self.assertIn(self.user_obama.username.upper(), post_area.text)
        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다
        self.assertIn(self.post_001.content, post_area.text)

        # 태그 있는지 확인
        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)

    def test_category_page(self):
        '''
        338p 카테고리 페이지
        get_absolute_url() : 모델에 정의됨
        1. 응답하는지 확인
        2. 파싱해서 저장 및 내가 설정한 카테고리명이 카테고리 카드에 있는지 확인
        3. 제목에 카테고리가 있는지 확인
        4. 메인 파트에 카테고리 이름과 포스트 제목이 잘 있는지 확인
        :return:
        :return:
        '''
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post(self):
        # 로그인을 하지 않으면 status code가 200이면 안된다
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # 로그인을 한다. self.client는 테스트 환경의 가상의 웹 브라우저, login() 함수
        self.client.login(username='trump', password='somepassword') # 일반 사용자가 로그인
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='obama', password='somepassword')  # staff가 로그인
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        self.assertEqual(Post.objects.count(), 3) # test

        self.client.post(
            #  첫 번째 인수인 경로로 두 번째 인수인 딕셔너리 정보를 POST 방식(http 통신 방식)으로 보냄
            '/blog/create_post/',
            {
                # Post 모델로 만든 폼은 title과 content 필드를 필수적으로 채워야 작동
                'title' : 'Post Form 만들기',
                'content': "Post Form 페이지를 만듭시다."
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        last_post = Post.objects.last() # Post 레코드 중 마지막 레코드
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, 'obama')


    def category_card_test(self, soup):
        '''
        내가 설정한 카테고리명이 카테고리 카드에 있는지 확인
        soup = BeautifulSoup(response.content, 'html.parser') html 요소를 파싱에서 soup에 담음
        response = self.client.get('/blog/')
        :param soup:
        :return:
        '''
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_java.name} ({self.category_java.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def navbar_test(self, soup):
        '''
        파싱해서 담은 nav 요소를 navBar에 담음
        제대로 있는지 확인
        요소 이름을 찾고 그 요소가 잘 이동하고 있는지 확인
        :param soup:
        :return:
        '''
        navBar = soup.nav
        self.assertIn('Blog', navBar.text)
        self.assertIn('About me', navBar.text)

        logo_btn = navBar.find('a', text='태경의 웹 패이지')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navBar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navBar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navBar.find('a', text='About me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')


    def test_post_list(self):
        # Post가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')  # id가 post-1인 div를 찾아서, 그 안에
        self.assertIn(self.post_001.title, post_001_card.text)  # title이 있는지
        self.assertIn(self.post_001.category.name, post_001_card.text)  # category가 있는지
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)  # 작성자명이 있는지
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        # Post가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')  # id가 main-area인 div태그를 찾습니다.
        self.assertIn('아직 게시물이 없습니다', main_area.text)
    def test_post_detail(self):
        # 1.2 그 포스트의 url은 '/blog/1/' 이다
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2 첫 번째 포소트의 상세 페이지 테스트
        # 2.1 첫 번째 포스트의 url로 접근하면 정상적으로 작동한다(status code: 200)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다
        self.navbar_test(soup)
        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다
        self.assertIn(self.post_001.title, soup.title.text)
        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다 (아직 구현 못 함, author 필드를 안 만듦)
        self.assertIn(self.user_obama.username.upper(), post_area.text)
        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다
        self.assertIn(self.post_001.content, post_area.text)


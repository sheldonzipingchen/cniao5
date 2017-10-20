# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime
from urlparse import urlparse
from uuid import uuid4

import requests
import sys
from bs4 import BeautifulSoup
from qiniu import put_file, Auth

from app.dao.thread_dao import ThreadDao, ForumThreadRelationDao, ForumDao
from app.models import Thread, ForumThreadRelation
reload(sys)
sys.setdefaultencoding( "utf-8" )

bucket_name='cniao5-imgs'

base_dir="//Users/Ivan.Wong/tempdata"
base_img_url="http://7mno4h.com1.z0.glb.clouddn.com/"
baseurl ="http://www.jianshu.com/"
article_base_url =baseurl+"/p/";

listurl = baseurl +str("collections/284/notes?order_by=added_at&page=")


user_ids=[10277,10278,10279,10280,10281,10282,10283,10284,10285,10286,10287,10288,10289,10290,10291,10292,10293,10294,10295,10296,10297,10298,
10299,10300,10301,10302,10303,10304,10305,10306,10307,10308,10309,10310,10311,
10312,10313,10314,10315,10316,10317,10318,10319,10320,10321,10322,10323,10324,10325,10326,10327,10328]

q = Auth('GidEaGEf5Sk_RNLCeCZtSfAjHrgFZWkVp8rZY0aO', 'WGXHmjvC-2dmZysxzGl9fK_4-LEyVZ8O4OqD57wr')


class HtmlSpider():

    def save_article_to_db(self,title,content,brief,img_links,user_id=None,forum_id=None):

            img_links = ",".join(img_links)

            if user_id==None:
                try:
                    user_id = user_ids[random.randint(0, 52)]
                except:
                    user_id=user_ids[0]

            try:
                read_count = random.randint(200, 10000)
                like_count = random.randint(20, 1000)

                thread = Thread(
                        title=title,
                        content=content,
                        imgs=img_links,
                        user_id=user_id,
                        created_time=datetime.now(),
                        read_count=read_count,
                        is_original=0,
                        brief=brief,
                        status =1,
                        like_count=like_count,
                        thread_type=1
                        )

                thread_dao = ThreadDao()
                thread_dao.save(thread)

                print 'forum_id='+str(forum_id)

                if forum_id is not None and forum_id>0:

                    relation= ForumThreadRelation(forum_id=forum_id,thread_id=thread.id,
                                      created_time=datetime.now())
                    ForumThreadRelationDao().save(relation)

                    forum_dao = ForumDao()
                    forum = forum_dao.get(forum_id)
                    #数量加1
                    forum.thread_count+=1
                    forum_dao.save(forum)

            except:
                pass

    def download_img(self,url_str,filename=None):

        try:

            if filename==None:
                filename==self.get_filename(url_str)

            self.mkdirs(base_dir)
            r = requests.get(url_str,timeout=10)
            chunk_size=100
            with open(base_dir+filename, 'wb') as fd:
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)

            self.upload_file_to_qiniu(base_dir+filename,filename)
        except:
            pass

    def delfile_from_dir(self,file_path):
        os.remove(file_path)

    def mkdirs(self,path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def get_filename(self,url_str):


        url = urlparse(url_str)
        i = len(url.path) - 1
        while i > 0:
            if url.path[i] == '/':
                break
            i = i - 1
        file_name=url.path[i+1:len(url.path)]

        extension="jpg"
        if file_name !='':
            try:
                extension=file_name.split(".")[1]
            except:
                pass
        return  str(uuid4())+"."+extension

    def upload_file_to_qiniu(self,file_path,file_key):

        token = q.upload_token(bucket_name, file_key, 3600)
        ret, info = put_file(token, file_key, file_path)
        if(info.status_code==200):
            # self.delfile_from_dir(file_path)
            print 'upload file finish %s'%file_key

    def delfile_from_dir(self,file_path):
        os.remove(file_path)

class JianshuSpider(HtmlSpider):


    def get_jianshu_articles(self,startpage,endpage):

        while startpage<=endpage:

            self.getlist(startpage)
            startpage+=1


    def getlist(self,pageindex):
        url =listurl+str(pageindex)
        page = requests.get(url);

        soup =BeautifulSoup(page.content,'html5lib')
        titles = soup.find_all("h4",{"class":"title"});
        for title in titles:
            next = title.next_element
            href= next.get("href")
            article_url = baseurl+href

            self.get_article_detail(article_url)

        print "finish page=============="+str(pageindex)


    def get_jianshu_article(self,article_id,user_id=None,forum_id=None):
        url = article_base_url+str(article_id)
        self.get_article_detail(url,user_id,forum_id)


    def get_article_detail(self,url,user_id=None,forum_id=None):

        page = requests.get(url);

        soup =BeautifulSoup(page.content,'html5lib')

        article = soup.find("div",{"class":"article"})
        title = article.find("h1",{"class":"title"}).text
        context = article.find("div",{"class":"show-content"})

        imgs = context.find_all("img")

        img_links =[]
        if len(imgs)>0:
            for img in imgs:
                img_url= img.get("src");

                if  'githubusercontent.com' in img_url or 'github.com' in img_url:
                    continue

                filename = self.get_filename(img_url)
                src =base_img_url+filename

                img["src"]=src
                img["data-original-src"]=src

                self.download_img(img_url,filename)
                img_links.append(src)


        brief = context.text[0:200]

        self.save_article_to_db(title,context.prettify(),brief,img_links,user_id,forum_id)

class LcodeSpider(HtmlSpider):

    def get_article_detail(self,url,user_id=None,forum_id=None):

        page = requests.get(url);

        soup =BeautifulSoup(page.content,'html5lib')

        article_eml= soup.find("article")

        title = article_eml.find("h1",{"class":"entry-title"}).text.strip()

        content_eml = article_eml.find("div",{'class':'entry-content'})


        content_eml.find("div",{"class":"ads_page_top"}).decompose()
        gutters = content_eml.select(".gutter")

        if len(gutters)>0:
            for gutter in gutters:
                gutter.decompose()

        line_numbers= content_eml.select(".line-numbers")
        if len(line_numbers)>0:
            for line in line_numbers:
                line.decompose()


        js_scritpts = content_eml.select("script")
        if len(js_scritpts)>0:
            for js in js_scritpts:
                js.decompose()



        content_eml.find(id="jiathis_style_32x32").parent.decompose()


        single_pages= content_eml.select(".pull-right.single-pages")


        if len(single_pages)>0:
            for sp in single_pages:
                sp.decompose()

        ps = content_eml.select("p")
        for p in ps:
            string = p.string


            if '关注我的订阅号' in str(string):

               siblings=p.find_next_siblings()
               for sb in siblings:
                     sb.decompose()
               p.decompose()

        imgs = content_eml.find_all("img")
        img_links =[]
        if len(imgs)>0:
            for img in imgs:

                img_url= img.get("data-original");
                if img_url==None:
                    img_url = img.get("src")

                if img_url==None:
                    return

                if img_url.startswith('data'):
                    continue

                filename = self.get_filename(img_url)
                src =base_img_url+filename

                img["src"]=src
                img["data-original"]=src
                img["data-original-src"]=src

                img.parent["href"]=src

                self.download_img(img_url,filename)
                img_links.append(src)


        brief = content_eml.text[0:200]

        self.save_article_to_db(title,content_eml.prettify(),brief,img_links,user_id,forum_id)

    def getlist(self,user_id=None,forum_id=None):

        url ='http://www.lcode.org/react-native/'
        page = requests.get(url);

        soup =BeautifulSoup(page.content,'html5lib')

        content_eml= soup.find("div",{"class":'page-content'})

        links = content_eml.find_all("a")

        for link in links:
            href = link.get("href")
            if href=='http://www.lcode.org' or href=='https://github.com/jiangqqlmj/WeixinArticles/blob/master/README.md':
                continue

            if href=='https://github.com/Bob1993/React-Native-Gank':
                break

            self.get_article_detail(href,user_id,forum_id)

class SegmentfaultSpider(HtmlSpider):
     def get_article_detail(self,url,user_id=None,forum_id=None):
         pass

class CSDNSpider(HtmlSpider):
     def get_article_detail(self,url,user_id=None,forum_id=None):
         pass



class ThreadHtmlPareser(HtmlSpider):


    def __init__(self):
        self.imgs = []
        self.content=''


    def pasert(self,content):

        soup =BeautifulSoup(content,'html5lib')

        js_scritpts = soup.select("script")
        if len(js_scritpts)>0:
            for js in js_scritpts:
                js.decompose()

        imgs = soup.find_all("img")

        if len(imgs)>0:
            for img in imgs:
               self.imgs.append(img.get('src'))


        links = soup.find_all("a")

        if len(links) >0:
            for link in links:

                click_evnt = link.get('onclick')

                if click_evnt is not None:
                    link['onclick']=''


        self.content = soup.body

    def show(self,content,show_hide=False):


        if content==None:
            return

        soup =BeautifulSoup(content,'html5lib')
        if show_hide==False:
            hides = soup.find_all("hide")

            for hide in hides:
                new_tag = soup.new_tag("div")
                new_tag.string='这里有隐藏内容,回复文章后刷新页面可见'
                new_tag['class']='attach_nopermission'
                hide.replace_with(new_tag)

        result = soup.body

        return result


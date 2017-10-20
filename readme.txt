1.运行 python manager.py db upgrade  创建表

要有 cniao5_development 这个数据库

2. python manager.py runserver 启动服务



更新表步骤

1.python manager.py db migrate -m "add xx model"
2.python manager.py db upgrade




部署：


1.su cniao
2.source venv/bin/activate
3. cd cniao5
4.svn update
5.ps -ef | grep 'uwsgi'
6.kill -9 ....
7.uwsgi config.ini
8.sudo service nginx restart


sudo pip install -r requirements.txt

sudo pip install -r requirements.txt  -i http://mirrors.aliyun.com/pypi/simple


sudo pip install --upgrade kombu


ps -ef | grep 'celery'
nohup celery -A tasks worker -l info











python manager.py runserver -p 80


sudo lsof -n -P| grep :80



启动 ngixn

 /usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf




 安装 MySQL-python 失败的解决方案:
 ln -s /usr/local/mysql/bin/mysql_config /usr/local/bin/mysql_config
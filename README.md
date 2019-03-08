# 52av.tv Spider
this spider base on Scrapy

[52av video player is based on this projcet](https://github.com/abadfox233/52av_video_player)

-------

### request
* python3
* scrapy
* MySQL

------

### Firstly 
you should create some table
```sql
  create table movie
(
  movie_url       varchar(200) null,
  image_url       varchar(300) null,
  image_path      varchar(200) null,
  title           varchar(200) null,
  issue_time      datetime     null,
  movie_object_id varchar(100) not null
    primary key
);
    

create table select_rule
(
  id             int auto_increment
    primary key,
  item_name      varchar(100) not null,
  css_selector   varchar(100) null,
  xpath_selector varchar(100) null,
  type           int          not null
);

create table video_images
(
  video_object_id varchar(200)                       null,
  big_images      varchar(200)                       null,
  id              int auto_increment
    primary key,
  big_images_path varchar(200)                       null,
  issue_time      datetime default CURRENT_TIMESTAMP null,
  constraint table_name_movie_video_url_fk
    foreign key (video_object_id) references movie (movie_object_id)
);

create table video_url
(
  id              int auto_increment
    primary key,
  m3u8_url        varchar(200) null,
  video_object_id varchar(200) null,
  constraint video_url_movie_movie_object_id_fk
    foreign key (video_object_id) references movie (movie_object_id)
);


```
> you can import some data into your Mysql
> the SQL file is in ./sql_data/

###Secondly 
you should config your db on project_av/setting.py
```python
MYSQL_HOST = 'localhost'
MYSQL_DBNAME = '52av'
MYSQL_USER = '52av'
MYSQL_PASSWORD = '52av'

SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"

```
the video image store in project_av/images
and you can change it in setting.py
```python
IMAGES_STORE = "some dir"
```
### Thirdly

you can config your proxy on project_av/middlewares.py
```python
class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:1080"
```

### Quickly Start
``` 
   python main.py   
```

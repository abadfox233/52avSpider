create table select_rule
(
  id             int auto_increment
    primary key,
  item_name      varchar(100) not null,
  css_selector   varchar(100) null,
  xpath_selector varchar(100) null,
  type           int          not null
);

INSERT INTO `52av`.select_rule (id, item_name, css_selector, xpath_selector, type) VALUES (1, 'all_page', 'div.pg label span::attr(title)', null, 1);
INSERT INTO `52av`.select_rule (id, item_name, css_selector, xpath_selector, type) VALUES (2, 'movie_list', 'ul.ml.waterfall.cl li', null, 1);
INSERT INTO `52av`.select_rule (id, item_name, css_selector, xpath_selector, type) VALUES (3, 'movie_end_url', 'div.c.cl a::attr(href)', null, 1);
INSERT INTO `52av`.select_rule (id, item_name, css_selector, xpath_selector, type) VALUES (4, 'cover_image', 'div.c.cl a img::attr(src)', null, 1);
INSERT INTO `52av`.select_rule (id, item_name, css_selector, xpath_selector, type) VALUES (5, 'title', 'div.c.cl a img::attr(alt)', null, 1);
INSERT INTO `52av`.select_rule (id, item_name, css_selector, xpath_selector, type) VALUES (6, 'issue_time', 'div.auth.cl span::attr(title)', null, 1);
INSERT INTO `52av`.select_rule (id, item_name, css_selector, xpath_selector, type) VALUES (7, 'start_page', '1', null, 5);
INSERT INTO `52av`.select_rule (id, item_name, css_selector, xpath_selector, type) VALUES (8, 'end_page', '2', null, 5);
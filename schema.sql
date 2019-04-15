CREATE TABLE IF NOT EXISTS `todolist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(1024) NOT NULL,
  `status` int(2) NOT NULL COMMENT '是否完成',
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

insert into todolist(id, user_id, title, status, create_time) values(1, 1, 'Xijinping', '0', 1482214350), (2, 1, 'Trump', '1', 1482214350);


CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(24) DEFAULT NULL,
  `password` varchar(24) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

insert into user values(1, 'admin', 'admin');

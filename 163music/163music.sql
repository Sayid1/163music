/*
Navicat MySQL Data Transfer

Source Server         : Local
Source Server Version : 50624
Source Host           : localhost:3306
Source Database       : 163music

Target Server Type    : MYSQL
Target Server Version : 50624
File Encoding         : 65001

Date: 2017-07-09 22:21:15
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for t_music
-- ----------------------------
DROP TABLE IF EXISTS `t_music`;
CREATE TABLE `t_music` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL COMMENT '歌曲名称',
  `duration` varchar(10) DEFAULT NULL COMMENT '时长',
  `singer` varchar(30) DEFAULT NULL COMMENT '歌手',
  `album` varchar(50) DEFAULT NULL COMMENT '专辑',
  `album_url` varchar(100) DEFAULT NULL COMMENT '专辑图片url',
  `lyric` text COMMENT '歌词',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='歌曲表';

-- ----------------------------
-- Table structure for t_music_sheet
-- ----------------------------
DROP TABLE IF EXISTS `t_music_sheet`;
CREATE TABLE `t_music_sheet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL COMMENT '歌单名称',
  `url` varchar(150) DEFAULT NULL COMMENT '歌单url',
  `profile_url` varchar(150) DEFAULT NULL COMMENT '歌单图片url',
  `players` varchar(20) DEFAULT NULL COMMENT '播放次数eg: 60万',
  `user_id` int(11) DEFAULT NULL COMMENT '歌单作者id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='歌单表';

-- ----------------------------
-- Table structure for t_music_sheet_comment
-- ----------------------------
DROP TABLE IF EXISTS `t_music_sheet_comment`;
CREATE TABLE `t_music_sheet_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT '0',
  `user_id` int(11) NOT NULL COMMENT '评论人ID',
  `comment` varchar(1000) DEFAULT NULL COMMENT '评论内容',
  `goods` int(6) DEFAULT NULL COMMENT '赞数量',
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='歌单评论表';

-- ----------------------------
-- Table structure for t_music_sheet_detail
-- ----------------------------
DROP TABLE IF EXISTS `t_music_sheet_detail`;
CREATE TABLE `t_music_sheet_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sheet_id` int(11) NOT NULL COMMENT '歌单ID',
  `labels` varchar(100) DEFAULT NULL COMMENT '标签',
  `describle` varchar(1000) DEFAULT NULL COMMENT '描述',
  `collections` int(11) DEFAULT NULL COMMENT '收藏数',
  `comments` int(11) DEFAULT NULL COMMENT '评论数',
  `musics` int(5) DEFAULT NULL COMMENT '歌单歌曲数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='歌单详情';

-- ----------------------------
-- Table structure for t_music_sheet_music
-- ----------------------------
DROP TABLE IF EXISTS `t_music_sheet_music`;
CREATE TABLE `t_music_sheet_music` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sheet_id` int(11) NOT NULL COMMENT '歌单ID',
  `music_id` int(11) NOT NULL COMMENT '歌曲ID',
  `comments` int(6) DEFAULT NULL COMMENT '歌单歌曲评论数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='歌单歌曲关系表';

-- ----------------------------
-- Table structure for t_music_sheet_music_comment
-- ----------------------------
DROP TABLE IF EXISTS `t_music_sheet_music_comment`;
CREATE TABLE `t_music_sheet_music_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT '0',
  `sheet_music_id` int(11) NOT NULL COMMENT '歌单关系ID',
  `comment` varchar(1500) DEFAULT NULL COMMENT '评论或回复',
  `wondelful` tinyint(1) DEFAULT NULL COMMENT '是否精彩评论',
  `goods` int(6) DEFAULT NULL COMMENT '赞数量',
  `create_time` datetime DEFAULT NULL COMMENT '评论时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='歌单歌曲评论表';

-- ----------------------------
-- Table structure for t_music_style
-- ----------------------------
DROP TABLE IF EXISTS `t_music_style`;
CREATE TABLE `t_music_style` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL COMMENT '类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_music_type
-- ----------------------------
DROP TABLE IF EXISTS `t_music_type`;
CREATE TABLE `t_music_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `style_id` int(11) DEFAULT NULL,
  `name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=290 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL COMMENT '用户名称',
  `url` varchar(100) DEFAULT NULL COMMENT '用户主页url',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户信息表';

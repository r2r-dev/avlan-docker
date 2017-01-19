CREATE TABLE IF NOT EXISTS `Setting` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `AllowedSetting` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `settingId` int(10) unsigned NOT NULL,
  `value` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `default_setting` bit(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `settingId` (`settingId`),
  CONSTRAINT `fk_settingId_AllowedSetting` FOREIGN KEY (`settingId`) REFERENCES `Setting` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `NodeType` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `type` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `Config` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `active` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `Interface` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`nodeId` INT(10) UNSIGNED NULL DEFAULT NULL,
	`peerNodeId` INT(10) UNSIGNED NULL DEFAULT NULL,
	`peerIfaceId` INT(10) UNSIGNED NULL DEFAULT NULL,
	`ifaceIndex` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_bin',
	`mac` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_bin',
	PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `InterfaceVlan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ifaceId` int(10) unsigned NOT NULL,
  `vlanId` int(10) unsigned NOT NULL,
  `pvid` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ifaceVlan` (`ifaceId`,`vlanId`)
) ENGINE=InnoDB AUTO_INCREMENT=794 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `Node` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `ipAddress` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `sshPort` int(10) unsigned DEFAULT NULL,
  `sshUsername` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `sshPassword` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


CREATE TABLE IF NOT EXISTS `Storage` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `storageLocation` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `storageLocation` (`storageLocation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `Task` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `description` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `storageId` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `fk_storageId_Task` (`storageId`),
  CONSTRAINT `fk_storageId_Task` FOREIGN KEY (`storageId`) REFERENCES `Storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `Token` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `expirationDate` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `value` (`value`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `User` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tokenId` int(10) unsigned DEFAULT NULL,
  `password` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `username` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`username`),
  KEY `fk_tokenId_User` (`tokenId`),
  CONSTRAINT `fk_tokenId_User` FOREIGN KEY (`tokenId`) REFERENCES `Token` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `UserSetting` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userId` int(10) unsigned NOT NULL,
  `settingId` int(10) unsigned NOT NULL,
  `allowedSettingId` int(10) unsigned DEFAULT NULL,
  `value` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_userId_UserSetting` (`userId`),
  KEY `fk_settingId_UserSetting` (`settingId`),
  KEY `fk_allowedSettingId_UserSetting` (`allowedSettingId`),
  CONSTRAINT `fk_allowedSettingId_UserSetting` FOREIGN KEY (`allowedSettingId`) REFERENCES `AllowedSetting` (`id`),
  CONSTRAINT `fk_settingId_UserSetting` FOREIGN KEY (`settingId`) REFERENCES `Setting` (`id`),
  CONSTRAINT `fk_userId_UserSetting` FOREIGN KEY (`userId`) REFERENCES `User` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `Vlan` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `number` int(10) DEFAULT NULL,
  `nodeId` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;


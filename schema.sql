CREATE TABLE urls ( 
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT, //ID of entry - mainly useful for APIs
	`key` BIGINT UNSIGNED NOT NULL, //integer form of base62 string
	`deleted` BOOL NOT NULL, //1 - inactive, 0 - active
	`url` varchar(2000) NOT NULL DEFAULT 'http://smalr.io/',
	PRIMARY KEY (`id`),
	UNIQUE INDEX (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE users (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`login_name` varchar(32) NOT NULL,
	`password_hash` char(40) NOT NULL DEFAULT '',
	`email` varchar(255) NOT NULL DEFAULT '',
	PRIMARY KEY (`id`),
	UNIQUE INDEX (`login_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


#used to get short urls that a particular user ID has ownership of
CREATE TABLE owner_to_url (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` BIGINT UNSIGNED NOT NULL,
	`url_id` BIGINT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

#used to get owners of particular short URL
CREATE TABLE url_to_owner (
	`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
	`url_id` BIGINT UNSIGNED NOT NULL,
	`user_id` BIGINT UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	INDEX (`url_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

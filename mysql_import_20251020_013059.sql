-- =====================================================
-- Magma7 Fitness - MySQL Import File
-- Generated: 2025-10-20 01:30:59
-- From SQLite database: db.sqlite3
-- =====================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO';


-- Table: auth_group_permissions
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "group_id" INT NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" INT NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: auth_user_groups
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "user_id" INT NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" INT NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: auth_user_user_permissions
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "user_id" INT NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" INT NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: django_content_type
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: django_content_type
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'memberships', 'plan'),
(8, 'memberships', 'subscription'),
(9, 'notifications', 'notification'),
(10, 'users', 'memberprofile'),
(11, 'payments', 'payment'),
(12, 'memberships', 'planfeature'),
(13, 'cms', 'partner'),
(14, 'cms', 'program'),
(15, 'cms', 'richpage'),
(16, 'cms', 'service'),
(17, 'cms', 'sitesettings'),
(18, 'cms', 'testimonial'),
(19, 'cms', 'aboutgalleryimage'),
(20, 'cms', 'aboutpage'),
(21, 'cms', 'aboutstatistic'),
(22, 'cms', 'corevalue'),
(23, 'cms', 'whychooseusitem'),
(24, 'cms', 'facilitiespage'),
(25, 'cms', 'facility'),
(26, 'cms', 'teammember'),
(27, 'cms', 'teampage'),
(28, 'memberships', 'workoutlog'),
(29, 'memberships', 'workoutsession'),
(30, 'memberships', 'weeklygoal'),
(31, 'cms', 'heroslide');


-- Table: auth_permission
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "content_type_id" INT NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: auth_permission
INSERT INTO `auth_permission` (`id`, `content_type_id`, `codename`, `name`) VALUES
(1, 1, 'add_logentry', 'Can add log entry'),
(2, 1, 'change_logentry', 'Can change log entry'),
(3, 1, 'delete_logentry', 'Can delete log entry'),
(4, 1, 'view_logentry', 'Can view log entry'),
(5, 2, 'add_permission', 'Can add permission'),
(6, 2, 'change_permission', 'Can change permission'),
(7, 2, 'delete_permission', 'Can delete permission'),
(8, 2, 'view_permission', 'Can view permission'),
(9, 3, 'add_group', 'Can add group'),
(10, 3, 'change_group', 'Can change group'),
(11, 3, 'delete_group', 'Can delete group'),
(12, 3, 'view_group', 'Can view group'),
(13, 4, 'add_user', 'Can add user'),
(14, 4, 'change_user', 'Can change user'),
(15, 4, 'delete_user', 'Can delete user'),
(16, 4, 'view_user', 'Can view user'),
(17, 5, 'add_contenttype', 'Can add content type'),
(18, 5, 'change_contenttype', 'Can change content type'),
(19, 5, 'delete_contenttype', 'Can delete content type'),
(20, 5, 'view_contenttype', 'Can view content type'),
(21, 6, 'add_session', 'Can add session'),
(22, 6, 'change_session', 'Can change session'),
(23, 6, 'delete_session', 'Can delete session'),
(24, 6, 'view_session', 'Can view session'),
(25, 7, 'add_plan', 'Can add plan'),
(26, 7, 'change_plan', 'Can change plan'),
(27, 7, 'delete_plan', 'Can delete plan'),
(28, 7, 'view_plan', 'Can view plan'),
(29, 8, 'add_subscription', 'Can add subscription'),
(30, 8, 'change_subscription', 'Can change subscription'),
(31, 8, 'delete_subscription', 'Can delete subscription'),
(32, 8, 'view_subscription', 'Can view subscription'),
(33, 9, 'add_notification', 'Can add notification'),
(34, 9, 'change_notification', 'Can change notification'),
(35, 9, 'delete_notification', 'Can delete notification'),
(36, 9, 'view_notification', 'Can view notification'),
(37, 10, 'add_memberprofile', 'Can add member profile'),
(38, 10, 'change_memberprofile', 'Can change member profile'),
(39, 10, 'delete_memberprofile', 'Can delete member profile'),
(40, 10, 'view_memberprofile', 'Can view member profile'),
(41, 11, 'add_payment', 'Can add payment'),
(42, 11, 'change_payment', 'Can change payment'),
(43, 11, 'delete_payment', 'Can delete payment'),
(44, 11, 'view_payment', 'Can view payment'),
(45, 12, 'add_planfeature', 'Can add plan feature'),
(46, 12, 'change_planfeature', 'Can change plan feature'),
(47, 12, 'delete_planfeature', 'Can delete plan feature'),
(48, 12, 'view_planfeature', 'Can view plan feature'),
(49, 13, 'add_partner', 'Can add partner'),
(50, 13, 'change_partner', 'Can change partner'),
(51, 13, 'delete_partner', 'Can delete partner'),
(52, 13, 'view_partner', 'Can view partner'),
(53, 14, 'add_program', 'Can add program'),
(54, 14, 'change_program', 'Can change program'),
(55, 14, 'delete_program', 'Can delete program'),
(56, 14, 'view_program', 'Can view program'),
(57, 15, 'add_richpage', 'Can add rich page'),
(58, 15, 'change_richpage', 'Can change rich page'),
(59, 15, 'delete_richpage', 'Can delete rich page'),
(60, 15, 'view_richpage', 'Can view rich page'),
(61, 16, 'add_service', 'Can add service'),
(62, 16, 'change_service', 'Can change service'),
(63, 16, 'delete_service', 'Can delete service'),
(64, 16, 'view_service', 'Can view service'),
(65, 17, 'add_sitesettings', 'Can add site settings'),
(66, 17, 'change_sitesettings', 'Can change site settings'),
(67, 17, 'delete_sitesettings', 'Can delete site settings'),
(68, 17, 'view_sitesettings', 'Can view site settings'),
(69, 18, 'add_testimonial', 'Can add testimonial'),
(70, 18, 'change_testimonial', 'Can change testimonial'),
(71, 18, 'delete_testimonial', 'Can delete testimonial'),
(72, 18, 'view_testimonial', 'Can view testimonial'),
(73, 19, 'add_aboutgalleryimage', 'Can add About Gallery Image'),
(74, 19, 'change_aboutgalleryimage', 'Can change About Gallery Image'),
(75, 19, 'delete_aboutgalleryimage', 'Can delete About Gallery Image'),
(76, 19, 'view_aboutgalleryimage', 'Can view About Gallery Image'),
(77, 20, 'add_aboutpage', 'Can add About Page Content'),
(78, 20, 'change_aboutpage', 'Can change About Page Content'),
(79, 20, 'delete_aboutpage', 'Can delete About Page Content'),
(80, 20, 'view_aboutpage', 'Can view About Page Content'),
(81, 21, 'add_aboutstatistic', 'Can add About Statistic'),
(82, 21, 'change_aboutstatistic', 'Can change About Statistic'),
(83, 21, 'delete_aboutstatistic', 'Can delete About Statistic'),
(84, 21, 'view_aboutstatistic', 'Can view About Statistic'),
(85, 22, 'add_corevalue', 'Can add Core Value'),
(86, 22, 'change_corevalue', 'Can change Core Value'),
(87, 22, 'delete_corevalue', 'Can delete Core Value'),
(88, 22, 'view_corevalue', 'Can view Core Value'),
(89, 23, 'add_whychooseusitem', 'Can add Why Choose Us Item'),
(90, 23, 'change_whychooseusitem', 'Can change Why Choose Us Item'),
(91, 23, 'delete_whychooseusitem', 'Can delete Why Choose Us Item'),
(92, 23, 'view_whychooseusitem', 'Can view Why Choose Us Item'),
(93, 24, 'add_facilitiespage', 'Can add Facilities Page Content'),
(94, 24, 'change_facilitiespage', 'Can change Facilities Page Content'),
(95, 24, 'delete_facilitiespage', 'Can delete Facilities Page Content'),
(96, 24, 'view_facilitiespage', 'Can view Facilities Page Content'),
(97, 25, 'add_facility', 'Can add Facility'),
(98, 25, 'change_facility', 'Can change Facility'),
(99, 25, 'delete_facility', 'Can delete Facility'),
(100, 25, 'view_facility', 'Can view Facility'),
(101, 26, 'add_teammember', 'Can add Team Member'),
(102, 26, 'change_teammember', 'Can change Team Member'),
(103, 26, 'delete_teammember', 'Can delete Team Member'),
(104, 26, 'view_teammember', 'Can view Team Member'),
(105, 27, 'add_teampage', 'Can add Team Page Content'),
(106, 27, 'change_teampage', 'Can change Team Page Content'),
(107, 27, 'delete_teampage', 'Can delete Team Page Content'),
(108, 27, 'view_teampage', 'Can view Team Page Content'),
(109, 28, 'add_workoutlog', 'Can add workout log'),
(110, 28, 'change_workoutlog', 'Can change workout log'),
(111, 28, 'delete_workoutlog', 'Can delete workout log'),
(112, 28, 'view_workoutlog', 'Can view workout log'),
(113, 29, 'add_workoutsession', 'Can add workout session'),
(114, 29, 'change_workoutsession', 'Can change workout session'),
(115, 29, 'delete_workoutsession', 'Can delete workout session'),
(116, 29, 'view_workoutsession', 'Can view workout session'),
(117, 30, 'add_weeklygoal', 'Can add weekly goal'),
(118, 30, 'change_weeklygoal', 'Can change weekly goal'),
(119, 30, 'delete_weeklygoal', 'Can delete weekly goal'),
(120, 30, 'view_weeklygoal', 'Can view weekly goal'),
(121, 31, 'add_heroslide', 'Can add Hero Slide'),
(122, 31, 'change_heroslide', 'Can change Hero Slide'),
(123, 31, 'delete_heroslide', 'Can delete Hero Slide'),
(124, 31, 'view_heroslide', 'Can view Hero Slide');


-- Table: auth_group
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "name" varchar(150) NOT NULL UNIQUE) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: auth_user
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "password" varchar(128) NOT NULL, "last_login" DATETIME NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" DATETIME NOT NULL, "first_name" varchar(150) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: auth_user
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `first_name`) VALUES
(1, 'pbkdf2_sha256$600000$EdXlnJCw5cioSCn1tmmxoS$0YELrXWVtWE+kwEJrXFTma7QsFEPAgZUtH4bYz5w414=', '2025-10-12 23:45:15.426831', 1, 'onahjonah', 'Onah', 'onahjonah@gmail.com', 1, 1, '2025-10-03 10:17:44.321876', 'Jonah'),
(2, 'pbkdf2_sha256$600000$vcdRGYkuJbK7sYfT26im8p$4hGGtI4FYyXTEAliNtPu+pAOQhczEK8KapcS7dywPLQ=', '2025-10-03 10:21:03.775461', 0, 'ojsys', 'Onah', 'onahjonah@gmail.com', 0, 1, '2025-10-03 10:21:03.677084', 'Jonah'),
(3, 'pbkdf2_sha256$600000$LJCLXpx9XqGOm7jSetMpcx$S/A4vWUBn7jEUakm9SjOzcAJ6HL34/QGxTYrTiwIKbE=', NULL, 1, 'admin', '', 'admin@magma7fitness.com', 1, 1, '2025-10-03 11:22:00.845888', ''),
(4, '', NULL, 0, 'testuser', '', 'test@example.com', 0, 1, '2025-10-19 10:23:36.525044', '');


-- Table: memberships_subscription
DROP TABLE IF EXISTS `memberships_subscription`;
CREATE TABLE `memberships_subscription` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "start_date" date NOT NULL, "end_date" date NOT NULL, "status" varchar(12) NOT NULL, "created_at" DATETIME NOT NULL, "updated_at" DATETIME NOT NULL, "last_reminder_days" INT NULL, "plan_id" bigint NOT NULL REFERENCES "memberships_plan" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" INT NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "payment_id" bigint NULL REFERENCES "payments_payment" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: memberships_subscription
INSERT INTO `memberships_subscription` (`id`, `start_date`, `end_date`, `status`, `created_at`, `updated_at`, `last_reminder_days`, `plan_id`, `user_id`, `payment_id`) VALUES
(1, '2025-10-03', '2025-11-02', 'active', '2025-10-03 10:21:10.666469', '2025-10-03 10:21:10.666483', NULL, 1, 2, NULL),
(2, '2025-10-03', '2026-10-03', 'active', '2025-10-03 12:22:22.995255', '2025-10-03 12:22:22.995264', NULL, 3, 2, NULL);


-- Table: notifications_notification
DROP TABLE IF EXISTS `notifications_notification`;
CREATE TABLE `notifications_notification` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "title" varchar(200) NOT NULL, "body" TEXT NOT NULL, "is_read" bool NOT NULL, "created_at" DATETIME NOT NULL, "user_id" INT NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: notifications_notification
INSERT INTO `notifications_notification` (`id`, `title`, `body`, `is_read`, `created_at`, `user_id`) VALUES
(1, 'Subscription Created', 'You subscribed to Monthly through 2025-11-02.', 1, '2025-10-03 10:21:10.668433', 2),
(2, 'Subscription Created', 'You subscribed to Annual through 2026-10-03.', 1, '2025-10-03 12:22:23.004391', 2),
(3, 'Subscription Created', 'You subscribed to Monthly through 2025-11-13.', 1, '2025-10-14 19:21:29.379090', 1),
(4, 'Subscription Created', 'You subscribed to Monthly through 2025-11-15.', 1, '2025-10-16 10:28:52.827328', 1),
(5, 'Subscription Created', 'You subscribed to Quarterly through 2026-01-14.', 1, '2025-10-16 10:29:19.652223', 1),
(6, 'Subscription Created', 'You subscribed to Monthly through 2025-11-16.', 1, '2025-10-16 23:32:08.863201', 1),
(7, 'Subscription Created', 'You subscribed to Monthly through 2025-11-16.', 1, '2025-10-16 23:49:52.038961', 1);


-- Table: payments_payment
DROP TABLE IF EXISTS `payments_payment`;
CREATE TABLE `payments_payment` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "amount" INT unsigned NOT NULL CHECK ("amount" >= 0), "currency" varchar(10) NOT NULL, "provider" varchar(10) NOT NULL, "status" varchar(12) NOT NULL, "reference" varchar(100) NOT NULL UNIQUE, "gateway_response" TEXT NULL CHECK ((JSON_VALID("gateway_response") OR "gateway_response" IS NULL)), "created_at" DATETIME NOT NULL, "updated_at" DATETIME NOT NULL, "completed_at" DATETIME NULL, "plan_id" bigint NOT NULL REFERENCES "memberships_plan" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" INT NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: payments_payment
INSERT INTO `payments_payment` (`id`, `amount`, `currency`, `provider`, `status`, `reference`, `gateway_response`, `created_at`, `updated_at`, `completed_at`, `plan_id`, `user_id`) VALUES
(1, 2500000, 'NGN', 'paystack', 'failed', 'M7_a1603ab18c73632a', '{"exception": "HTTP Error 403: Forbidden"}', '2025-10-19 09:48:42.184642', '2025-10-19 09:48:43.230993', NULL, 1, 1),
(2, 2500000, 'NGN', 'paystack', 'failed', 'M7_94002fed479efbf8', '{"exception": "401 Client Error: Unauthorized for url: https://api.paystack.co/transaction/initialize"}', '2025-10-19 09:59:23.812997', '2025-10-19 09:59:25.066716', NULL, 1, 1),
(3, 2500000, 'NGN', 'paystack', 'pending', 'M7_3be95a16dbf0d30b', NULL, '2025-10-19 10:04:30.453459', '2025-10-19 10:04:30.453473', NULL, 1, 1),
(4, 2500000, 'NGN', 'paystack', 'successful', 'TEST_REF_123456', NULL, '2025-10-19 10:23:36.529521', '2025-10-19 10:23:36.529536', NULL, 1, 4),
(5, 2500000, 'NGN', 'paystack', 'pending', 'M7_fdd7c8397ea8e7ca', NULL, '2025-10-19 20:37:26.731423', '2025-10-19 20:37:26.731510', NULL, 1, 1),
(6, 2500000, 'NGN', 'paystack', 'pending', 'M7_58371fcfc0606a1f', NULL, '2025-10-19 21:34:36.586722', '2025-10-19 21:34:36.586741', NULL, 1, 1);


-- Table: users_memberprofile
DROP TABLE IF EXISTS `users_memberprofile`;
CREATE TABLE `users_memberprofile` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "phone" varchar(20) NOT NULL, "address" varchar(255) NOT NULL, "date_of_birth" date NULL, "user_id" INT NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: users_memberprofile
INSERT INTO `users_memberprofile` (`id`, `phone`, `address`, `date_of_birth`, `user_id`) VALUES
(1, '', '', NULL, 1),
(2, '', '', NULL, 2),
(3, '', '', NULL, 3),
(4, '', '', NULL, 4);


-- Table: cms_partner
DROP TABLE IF EXISTS `cms_partner`;
CREATE TABLE `cms_partner` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "name" varchar(120) NOT NULL, "logo_url" varchar(200) NOT NULL, "website_url" varchar(200) NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: cms_program
DROP TABLE IF EXISTS `cms_program`;
CREATE TABLE `cms_program` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "title" varchar(100) NOT NULL, "description" TEXT NOT NULL, "icon" varchar(50) NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_program
INSERT INTO `cms_program` (`id`, `title`, `description`, `icon`, `order`) VALUES
(1, 'Strength Training', 'Programs to gain strength', 'fitness_center', 1),
(2, 'Basic Yoga', 'Combine yoga with cardio', 'self_improvement', 2),
(3, 'Body Building', 'Increase muscle mass and strength', 'sports_mma', 3),
(4, 'Weight Loss', 'Sustainable lifestyle changes', 'monitor_weight', 4);


-- Table: cms_richpage
DROP TABLE IF EXISTS `cms_richpage`;
CREATE TABLE `cms_richpage` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "slug" varchar(50) NOT NULL UNIQUE, "title" varchar(200) NOT NULL, "body" TEXT NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_richpage
INSERT INTO `cms_richpage` (`id`, `slug`, `title`, `body`) VALUES
(1, 'about', 'About Us', 'Magma7 Fitness Center is more than just a gym. We are a community dedicated to promoting a healthy and active lifestyle for everyone. Our center is located in the heart of Kaduna at No. 30 Zakaria Maimalari Street, Nasfat Layout, and is open to people of all ages and fitness levels.');


-- Table: cms_service
DROP TABLE IF EXISTS `cms_service`;
CREATE TABLE `cms_service` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "title" varchar(120) NOT NULL, "description" TEXT NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_service
INSERT INTO `cms_service` (`id`, `title`, `description`, `order`) VALUES
(1, 'Personal Training', 'Personalized plan and progress tracking', 1),
(2, 'Expert Trainers', 'Certified, skilled trainers to guide you', 2),
(3, 'Flexible Time', 'Off-peak sessions and flexible hours', 3);


-- Table: cms_testimonial
DROP TABLE IF EXISTS `cms_testimonial`;
CREATE TABLE `cms_testimonial` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "name" varchar(120) NOT NULL, "role" varchar(120) NOT NULL, "rating" smallint unsigned NOT NULL CHECK ("rating" >= 0), "quote" TEXT NOT NULL, "avatar_url" varchar(200) NOT NULL, "is_approved" bool NOT NULL, "created_at" DATETIME NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_testimonial
INSERT INTO `cms_testimonial` (`id`, `name`, `role`, `rating`, `quote`, `avatar_url`, `is_approved`, `created_at`) VALUES
(1, 'Happy Member', '', 5, 'Great environment and trainers. I reached my goals!', '', 1, '2025-10-03 11:21:52.845006'),
(2, 'Farhan Rio', '', 5, 'Trainers are amazing and push me to be my best.', '', 1, '2025-10-03 11:21:52.845902');


-- Table: memberships_planfeature
DROP TABLE IF EXISTS `memberships_planfeature`;
CREATE TABLE `memberships_planfeature` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "TEXT" varchar(200) NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0), "plan_id" bigint NOT NULL REFERENCES "memberships_plan" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: cms_sitesettings
DROP TABLE IF EXISTS `cms_sitesettings`;
CREATE TABLE `cms_sitesettings` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "brand_name" varchar(100) NOT NULL, "tagline" varchar(200) NOT NULL, "phone" varchar(30) NOT NULL, "email" varchar(254) NOT NULL, "address" varchar(255) NOT NULL, "hero_headline" varchar(200) NOT NULL, "hero_subtext" TEXT NOT NULL, "hero_cta_text" varchar(50) NOT NULL, "hero_cta_url" varchar(200) NOT NULL, "hero_image_url" varchar(200) NOT NULL, "primary_color" varchar(7) NOT NULL, "accent_color" varchar(7) NOT NULL, "light_color" varchar(7) NOT NULL, "dark_bg" varchar(7) NOT NULL, "card_bg" varchar(7) NOT NULL, "free_guide_description" TEXT NOT NULL, "free_guide_text" varchar(50) NOT NULL, "free_guide_title" varchar(100) NOT NULL, "free_guide_url" varchar(200) NOT NULL, "cta_description" TEXT NOT NULL, "cta_headline" varchar(200) NOT NULL, "cta_image_url" varchar(200) NOT NULL, "cta_primary_text" varchar(50) NOT NULL, "cta_primary_url" varchar(200) NOT NULL, "cta_secondary_text" varchar(50) NOT NULL, "cta_secondary_url" varchar(200) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_sitesettings
INSERT INTO `cms_sitesettings` (`id`, `brand_name`, `tagline`, `phone`, `email`, `address`, `hero_headline`, `hero_subtext`, `hero_cta_text`, `hero_cta_url`, `hero_image_url`, `primary_color`, `accent_color`, `light_color`, `dark_bg`, `card_bg`, `free_guide_description`, `free_guide_text`, `free_guide_title`, `free_guide_url`, `cta_description`, `cta_headline`, `cta_image_url`, `cta_primary_text`, `cta_primary_url`, `cta_secondary_text`, `cta_secondary_url`) VALUES
(1, 'Magma7Fitness', 'Healthy body, healthy mind', '+234 000 000 0000', 'info@magma7fitness.com', 'No. 30 Zakaria Maimalari Street, Nasfat Layout, Kaduna', 'Get Healthy Body with the Perfect Exercises', 'We are here to help you make a healthy body and mind through fitness.', 'Get Started', '/memberships/plans/', 'https://images.unsplash.com/photo-1554284126-aa88f22d8b74?q=80&w=1400&auto=format&fit=crop', '#0b6e4f', '#d4af37', '#ffffff', '#121416', '#1d1f21', 'A comprehensive 30-page guide covering workout routines, nutrition tips, and goal-setting strategies for beginners to advanced fitness enthusiasts.', 'Download Free', 'Complete Fitness Transformation Guide', 'https://example.com/free-fitness-guide.pdf', 'Join thousands of satisfied members who have transformed their lives at Magma7Fitness', 'Ready to Start?', '', 'Sign Up Today', '/accounts/signup/', 'Learn More', '/about/');


-- Table: memberships_plan
DROP TABLE IF EXISTS `memberships_plan`;
CREATE TABLE `memberships_plan` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "name" varchar(100) NOT NULL, "description" TEXT NOT NULL, "price" decimal NOT NULL, "duration_days" INT unsigned NOT NULL CHECK ("duration_days" >= 0), "is_active" bool NOT NULL, "is_featured" bool NOT NULL, "price_period" varchar(50) NOT NULL, "image_url" varchar(200) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: memberships_plan
INSERT INTO `memberships_plan` (`id`, `name`, `description`, `price`, `duration_days`, `is_active`, `is_featured`, `price_period`, `image_url`) VALUES
(1, 'Monthly', '30-day access to all facilities and classes.', 25000, 30, 1, 0, 'Per Month', ''),
(2, 'Quarterly', '90-day access at a discounted rate.', 65000, 90, 1, 0, 'Per Month', ''),
(3, 'Annual', '365-day full access with best value.', 200000, 365, 1, 0, 'Per Month', '');


-- Table: cms_aboutgalleryimage
DROP TABLE IF EXISTS `cms_aboutgalleryimage`;
CREATE TABLE `cms_aboutgalleryimage` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "title" varchar(150) NOT NULL, "image_url" varchar(200) NOT NULL, "description" TEXT NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0), "is_active" bool NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_aboutgalleryimage
INSERT INTO `cms_aboutgalleryimage` (`id`, `title`, `image_url`, `description`, `order`, `is_active`) VALUES
(1, 'Cardio Zone', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600', 'Premium treadmills, ellipticals, and bikes', 1, 1),
(2, 'Weight Training Area', 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=600', 'Complete range of free weights and machines', 2, 1),
(3, 'Group Fitness Studio', 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600', 'Spacious studio for classes and training', 3, 1),
(4, 'Functional Training Zone', 'https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=600', 'Dedicated space for functional fitness', 4, 1),
(5, 'Yoga & Pilates Studio', 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600', 'Peaceful space for mind-body workouts', 5, 1),
(6, 'Juice Bar', 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600', 'Healthy refreshments and snacks', 6, 1);


-- Table: cms_aboutpage
DROP TABLE IF EXISTS `cms_aboutpage`;
CREATE TABLE `cms_aboutpage` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "hero_title" varchar(200) NOT NULL, "hero_subtitle" TEXT NOT NULL, "hero_image_url" varchar(200) NOT NULL, "story_title" varchar(200) NOT NULL, "story_content" TEXT NOT NULL, "story_image_url" varchar(200) NOT NULL, "mission_title" varchar(200) NOT NULL, "mission_content" TEXT NOT NULL, "mission_icon" varchar(50) NOT NULL, "vision_title" varchar(200) NOT NULL, "vision_content" TEXT NOT NULL, "vision_icon" varchar(50) NOT NULL, "why_choose_title" varchar(200) NOT NULL, "why_choose_description" TEXT NOT NULL, "gallery_title" varchar(200) NOT NULL, "gallery_description" TEXT NOT NULL, "cta_title" varchar(200) NOT NULL, "cta_description" TEXT NOT NULL, "cta_button_text" varchar(50) NOT NULL, "cta_button_url" varchar(200) NOT NULL, "cta_image_url" varchar(200) NOT NULL, "updated_at" DATETIME NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_aboutpage
INSERT INTO `cms_aboutpage` (`id`, `hero_title`, `hero_subtitle`, `hero_image_url`, `story_title`, `story_content`, `story_image_url`, `mission_title`, `mission_content`, `mission_icon`, `vision_title`, `vision_content`, `vision_icon`, `why_choose_title`, `why_choose_description`, `gallery_title`, `gallery_description`, `cta_title`, `cta_description`, `cta_button_text`, `cta_button_url`, `cta_image_url`, `updated_at`) VALUES
(1, 'About Magma7Fitness', 'More than just a gym - we\'re a community dedicated to transforming lives through fitness, wellness, and support.', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1200', 'Our Story', 'Magma7 Fitness Center was founded with a simple yet powerful vision: to create a space where everyone, regardless of their fitness level, could feel welcome and supported in their health journey.

Located in the heart of Kaduna at No. 30 Zakaria Maimalari Street, Nasfat Layout, we\'ve grown from a small local gym into a thriving fitness community. Our state-of-the-art facility boasts premium equipment for strength training, cardio, and functional fitness.

What sets us apart isn\'t just our equipment - it\'s our people. Our certified trainers and supportive community members create an environment where you can push your limits while feeling completely at home.', 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=800', 'Our Mission', 'To empower individuals to lead healthy and active lifestyles by providing a welcoming and inclusive environment that offers a range of fitness and wellness services.', 'track_changes', 'Our Vision', 'To be the leading fitness center in Kaduna, known for providing exceptional facilities and services that enable our members to achieve their health and fitness goals.', 'visibility', 'Why Choose Magma7Fitness', 'We offer more than just a place to work out - we provide a complete fitness ecosystem designed for your success.', 'Our World-Class Facility', 'Take a virtual tour of our state-of-the-art gym and see why members love training with us.', 'Ready to Transform Your Life?', 'Join thousands of satisfied members who have achieved their fitness goals with us', 'Start Your Journey', '/memberships/plans/', 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=1200', '2025-10-13 23:25:58.922465');


-- Table: cms_aboutstatistic
DROP TABLE IF EXISTS `cms_aboutstatistic`;
CREATE TABLE `cms_aboutstatistic` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "label" varchar(100) NOT NULL, "value" varchar(50) NOT NULL, "icon" varchar(50) NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0), "is_active" bool NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_aboutstatistic
INSERT INTO `cms_aboutstatistic` (`id`, `label`, `value`, `icon`, `order`, `is_active`) VALUES
(1, 'Active Members', '5,000+', 'people', 1, 1),
(2, 'Expert Trainers', '25+', 'school', 2, 1),
(3, 'Years of Excellence', '10+', 'emoji_events', 3, 1),
(4, 'Success Stories', '2,500+', 'trending_up', 4, 1);


-- Table: cms_corevalue
DROP TABLE IF EXISTS `cms_corevalue`;
CREATE TABLE `cms_corevalue` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "title" varchar(100) NOT NULL, "description" TEXT NOT NULL, "icon" varchar(50) NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0), "is_active" bool NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_corevalue
INSERT INTO `cms_corevalue` (`id`, `title`, `description`, `icon`, `order`, `is_active`) VALUES
(1, 'Health & Wellness', 'We prioritize the health and wellness of our members and aim to promote healthy lifestyles through our services and facilities.', 'favorite', 1, 1),
(2, 'Inclusivity', 'We believe in creating an inclusive environment that welcomes individuals from all backgrounds and fitness levels.', 'diversity_3', 2, 1),
(3, 'Excellence', 'We strive for excellence in everything we do, from the quality of our equipment and facilities to the professionalism of our staff.', 'star', 3, 1),
(4, 'Community', 'We foster a sense of community among our members and staff, promoting mutual support and encouragement.', 'groups', 4, 1),
(5, 'Innovation', 'We embrace innovation in our approach to fitness and wellness, constantly seeking new and effective ways to help our members achieve their goals.', 'lightbulb', 5, 1),
(6, 'Integrity', 'We operate with honesty, transparency, and accountability in all our interactions with members and partners.', 'verified', 6, 1);


-- Table: cms_whychooseusitem
DROP TABLE IF EXISTS `cms_whychooseusitem`;
CREATE TABLE `cms_whychooseusitem` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "title" varchar(150) NOT NULL, "description" TEXT NOT NULL, "icon" varchar(50) NOT NULL, "image_url" varchar(200) NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0), "is_active" bool NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_whychooseusitem
INSERT INTO `cms_whychooseusitem` (`id`, `title`, `description`, `icon`, `image_url`, `order`, `is_active`) VALUES
(1, 'Expert Trainers', 'Our certified personal trainers are dedicated to providing personalized support and guidance throughout your fitness journey.', 'school', '', 1, 1),
(2, 'State-of-the-Art Equipment', 'Access premium cardio and strength training equipment from leading brands, maintained to the highest standards.', 'fitness_center', '', 2, 1),
(3, 'Diverse Class Options', 'From yoga and Pilates to Zumba and kickboxing, we offer group fitness classes for all interests and levels.', 'sports_gymnastics', '', 3, 1),
(4, 'Flexible Membership', 'Choose from a variety of membership plans designed to fit your schedule and budget.', 'calendar_today', '', 4, 1),
(5, 'Women-Only Studio', 'We provide a private, comfortable space for women who prefer a more intimate workout environment.', 'woman', '', 5, 1),
(6, 'Nutrition Support', 'Healthy juice bar and nutritional guidance to complement your fitness routine and accelerate results.', 'restaurant', '', 6, 1);


-- Table: cms_facilitiespage
DROP TABLE IF EXISTS `cms_facilitiespage`;
CREATE TABLE `cms_facilitiespage` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "hero_title" varchar(200) NOT NULL, "hero_subtitle" TEXT NOT NULL, "hero_image_url" varchar(200) NOT NULL, "intro_title" varchar(200) NOT NULL, "intro_content" TEXT NOT NULL, "cta_title" varchar(200) NOT NULL, "cta_description" TEXT NOT NULL, "cta_button_text" varchar(50) NOT NULL, "cta_button_url" varchar(200) NOT NULL, "updated_at" DATETIME NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: cms_facility
DROP TABLE IF EXISTS `cms_facility`;
CREATE TABLE `cms_facility` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "name" varchar(150) NOT NULL, "description" TEXT NOT NULL, "icon" varchar(50) NOT NULL, "image_url" varchar(200) NOT NULL, "features" TEXT NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0), "is_active" bool NOT NULL, "is_featured" bool NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: cms_teammember
DROP TABLE IF EXISTS `cms_teammember`;
CREATE TABLE `cms_teammember` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "name" varchar(150) NOT NULL, "role" varchar(100) NOT NULL, "role_category" varchar(20) NOT NULL, "bio" TEXT NOT NULL, "image_url" varchar(200) NOT NULL, "specialties" TEXT NOT NULL, "certifications" TEXT NOT NULL, "experience_years" INT unsigned NOT NULL CHECK ("experience_years" >= 0), "email" varchar(254) NOT NULL, "phone" varchar(30) NOT NULL, "instagram" varchar(200) NOT NULL, "linkedin" varchar(200) NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0), "is_active" bool NOT NULL, "is_featured" bool NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: cms_teampage
DROP TABLE IF EXISTS `cms_teampage`;
CREATE TABLE `cms_teampage` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "hero_title" varchar(200) NOT NULL, "hero_subtitle" TEXT NOT NULL, "hero_image_url" varchar(200) NOT NULL, "intro_title" varchar(200) NOT NULL, "intro_content" TEXT NOT NULL, "cta_title" varchar(200) NOT NULL, "cta_description" TEXT NOT NULL, "cta_button_text" varchar(50) NOT NULL, "cta_button_url" varchar(200) NOT NULL, "updated_at" DATETIME NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: memberships_workoutlog
DROP TABLE IF EXISTS `memberships_workoutlog`;
CREATE TABLE `memberships_workoutlog` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "workout_type" varchar(20) NOT NULL, "duration" INT unsigned NOT NULL CHECK ("duration" >= 0), "calories" INT unsigned NULL CHECK ("calories" >= 0), "notes" TEXT NOT NULL, "date" date NOT NULL, "created_at" DATETIME NOT NULL, "user_id" INT NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: memberships_workoutlog
INSERT INTO `memberships_workoutlog` (`id`, `workout_type`, `duration`, `calories`, `notes`, `date`, `created_at`, `user_id`) VALUES
(1, 'cardio', 60, NULL, '', '2025-10-14', '2025-10-14 19:53:29.584225', 1);


-- Table: memberships_workoutsession
DROP TABLE IF EXISTS `memberships_workoutsession`;
CREATE TABLE `memberships_workoutsession` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "title" varchar(200) NOT NULL, "workout_type" varchar(20) NOT NULL, "session_date" date NOT NULL, "session_time" time NOT NULL, "duration" INT unsigned NOT NULL CHECK ("duration" >= 0), "trainer" varchar(100) NOT NULL, "notes" TEXT NOT NULL, "created_at" DATETIME NOT NULL, "user_id" INT NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: memberships_weeklygoal
DROP TABLE IF EXISTS `memberships_weeklygoal`;
CREATE TABLE `memberships_weeklygoal` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "goal_type" varchar(20) NOT NULL, "target_value" INT unsigned NOT NULL CHECK ("target_value" >= 0), "week_start" date NOT NULL, "is_active" bool NOT NULL, "created_at" DATETIME NOT NULL, "user_id" INT NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: cms_heroslide
DROP TABLE IF EXISTS `cms_heroslide`;
CREATE TABLE `cms_heroslide` ("id" INT NOT NULL PRIMARY KEY AUTO_INCREMENT, "title" varchar(200) NOT NULL, "image_url" varchar(200) NOT NULL, "is_active" bool NOT NULL, "order" INT unsigned NOT NULL CHECK ("order" >= 0), "created_at" DATETIME NOT NULL, "updated_at" DATETIME NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data for table: cms_heroslide
INSERT INTO `cms_heroslide` (`id`, `title`, `image_url`, `is_active`, `order`, `created_at`, `updated_at`) VALUES
(1, 'Modern Gym Equipment', 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2000&auto=format&fit=crop', 1, 0, '2025-10-16 11:35:35.212657', '2025-10-16 11:35:35.212679'),
(2, 'Personal Training Session', 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?q=80&w=2000&auto=format&fit=crop', 1, 1, '2025-10-16 11:35:35.214775', '2025-10-16 11:35:35.214785'),
(3, 'Group Fitness Class', 'https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=2000&auto=format&fit=crop', 1, 2, '2025-10-16 11:35:35.215609', '2025-10-16 11:35:35.215618'),
(4, 'Cardio Training', 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?q=80&w=2000&auto=format&fit=crop', 1, 3, '2025-10-16 11:35:35.216362', '2025-10-16 11:35:35.216368'),
(5, 'Weight Training', 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2000&auto=format&fit=crop', 1, 4, '2025-10-16 11:35:35.216978', '2025-10-16 11:35:35.216984');


SET FOREIGN_KEY_CHECKS=1;

-- Import completed

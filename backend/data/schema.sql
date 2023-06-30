-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: sdcs
-- ------------------------------------------------------
-- Server version	10.6.5-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `airbase`
--
CREATE DATABASE IF NOT EXISTS sdcs;
USE sdcs;

DROP TABLE IF EXISTS `airbase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `airbase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `airbase_id` int(11) NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pos_u` decimal(20,10) NOT NULL,
  `pos_v` decimal(20,10) NOT NULL,
  `level` int(11) NOT NULL DEFAULT 0,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `functional` tinyint(1) NOT NULL DEFAULT 0,
  `damaged` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Airbase_campaign_id_airbase_id_key` (`campaign_id`,`airbase_id`),
  UNIQUE KEY `Airbase_campaign_id_name_key` (`campaign_id`,`name`),
  CONSTRAINT `Airbase_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=405 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `awacs`
--

DROP TABLE IF EXISTS `awacs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `awacs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `awacs_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pos_u` decimal(20,10) NOT NULL,
  `pos_v` decimal(20,10) NOT NULL,
  `marker_text` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fuel` decimal(11,10) NOT NULL,
  `life_regen_at` datetime(3) DEFAULT NULL,
  `return_to_base` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `Awacs_campaign_id_fkey` (`campaign_id`),
  CONSTRAINT `Awacs_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `campaign`
--

DROP TABLE IF EXISTS `campaign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campaign` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `theatre` enum('Caucasus','PersianGulf','Syria') COLLATE utf8mb4_unicode_ci NOT NULL,
  `start` datetime(3) NOT NULL,
  `end` datetime(3) DEFAULT NULL,
  `winner` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pending_end` datetime(3) DEFAULT NULL,
  `lotatc_blue` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'blue',
  `lotatc_red` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'red',
  `srs_blue` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'blue',
  `srs_red` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'red',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `campaignunitlevelcount`
--

DROP TABLE IF EXISTS `campaignunitlevelcount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `campaignunitlevelcount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `level` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `CampaignUnitLevelCount_campaign_id_level_key` (`campaign_id`,`level`),
  CONSTRAINT `CampaignUnitLevelCount_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `discordlink`
--

DROP TABLE IF EXISTS `discordlink`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `discordlink` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `discord_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires` datetime(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `DiscordLink_discord_id_key` (`discord_id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `farp`
--

DROP TABLE IF EXISTS `farp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `farp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_id` int(11) NOT NULL,
  `pos_u` decimal(20,10) NOT NULL,
  `pos_v` decimal(20,10) NOT NULL,
  `hdg` decimal(13,10) NOT NULL,
  `level` int(11) NOT NULL,
  `alive` tinyint(1) NOT NULL,
  `functional` tinyint(1) NOT NULL,
  `damaged` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Farp_campaign_id_unit_name_key` (`campaign_id`,`unit_name`),
  CONSTRAINT `Farp_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `issues`
--

DROP TABLE IF EXISTS `issues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `issues` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(3) NOT NULL DEFAULT current_timestamp(3),
  `user_id` int(11) NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reported` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `Issues_user_id_fkey` (`user_id`),
  CONSTRAINT `Issues_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lives`
--

DROP TABLE IF EXISTS `lives`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lives` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `origin_airbase_id` int(11) DEFAULT NULL,
  `origin_farp_id` int(11) DEFAULT NULL,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `life_class` enum('RW','FW') COLLATE utf8mb4_unicode_ci NOT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT 0,
  `removed_at` datetime(3) DEFAULT NULL,
  `removed_by_slot` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `pending` tinyint(1) NOT NULL DEFAULT 0,
  `reset_at` datetime(3) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Lives_origin_airbase_id_fkey` (`origin_airbase_id`),
  KEY `Lives_origin_farp_id_fkey` (`origin_farp_id`),
  CONSTRAINT `Lives_origin_airbase_id_fkey` FOREIGN KEY (`origin_airbase_id`) REFERENCES `airbase` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Lives_origin_farp_id_fkey` FOREIGN KEY (`origin_farp_id`) REFERENCES `farp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6344 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `persistentmarker`
--

DROP TABLE IF EXISTS `persistentmarker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persistentmarker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `dcs_marker_id` int(11) NOT NULL,
  `pos_u` decimal(20,10) NOT NULL,
  `pos_v` decimal(20,10) NOT NULL,
  `marker_text` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `removed_at` datetime(3) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `PersistentMarker_campaign_id_fkey` (`campaign_id`),
  CONSTRAINT `PersistentMarker_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shipping`
--

DROP TABLE IF EXISTS `shipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `load_pos_u` decimal(20,10) NOT NULL,
  `load_pos_v` decimal(20,10) NOT NULL,
  `start_pos_u` decimal(20,10) NOT NULL,
  `start_pos_v` decimal(20,10) NOT NULL,
  `end_pos_u` decimal(20,10) NOT NULL,
  `end_pos_v` decimal(20,10) NOT NULL,
  `unload_pos_u` decimal(20,10) NOT NULL,
  `unload_pos_v` decimal(20,10) NOT NULL,
  `group_id` int(11) NOT NULL,
  `started_at` datetime(3) DEFAULT NULL,
  `completed_at` datetime(3) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Shipping_group_id_key` (`group_id`),
  KEY `Shipping_campaign_id_fkey` (`campaign_id`),
  CONSTRAINT `Shipping_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Shipping_group_id_fkey` FOREIGN KEY (`group_id`) REFERENCES `unitgroup` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shippingunits`
--

DROP TABLE IF EXISTS `shippingunits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shippingunits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shipping_id` int(11) NOT NULL,
  `unit_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ShippingUnits_shipping_id_fkey` (`shipping_id`),
  KEY `ShippingUnits_unit_id_fkey` (`unit_id`),
  CONSTRAINT `ShippingUnits_shipping_id_fkey` FOREIGN KEY (`shipping_id`) REFERENCES `shipping` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ShippingUnits_unit_id_fkey` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=183 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime(3) NOT NULL,
  `created_by` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `closed_at` datetime(3) DEFAULT NULL,
  `closed_by` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `closed_comment` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unit`
--

DROP TABLE IF EXISTS `unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `unit_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `unit_suffix` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `spawn_zone` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_type_id` int(11) NOT NULL,
  `pos_u` decimal(20,10) NOT NULL,
  `pos_v` decimal(20,10) NOT NULL,
  `hdg` decimal(13,10) NOT NULL,
  `removed_at` datetime(3) DEFAULT NULL,
  `removed_at_prio` int(11) DEFAULT NULL,
  `removed_reason` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `replace_with_type_id` int(11) DEFAULT NULL,
  `replace_at` datetime(3) DEFAULT NULL,
  `mass_kg` int(11) DEFAULT NULL,
  `spawn_airfield_id` int(11) DEFAULT NULL,
  `spawn_location_level` int(11) DEFAULT NULL,
  `unpacked_from_cargo` tinyint(1) DEFAULT NULL,
  `created_at` datetime(3) NOT NULL DEFAULT current_timestamp(3),
  `zone_entered` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `zone_entered_at` datetime(3) DEFAULT NULL,
  `player_can_drive` tinyint(1) NOT NULL DEFAULT 1,
  `replace_with_comp` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `respawn_when_killed` tinyint(1) NOT NULL DEFAULT 0,
  `respawned` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Unit_campaign_id_unit_id_key` (`campaign_id`,`unit_id`),
  KEY `Unit_unit_type_id_fkey` (`unit_type_id`),
  KEY `Unit_replace_with_type_id_fkey` (`replace_with_type_id`),
  KEY `Unit_user_id_fkey` (`user_id`),
  KEY `Unit_group_id_fkey` (`group_id`),
  CONSTRAINT `Unit_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Unit_group_id_fkey` FOREIGN KEY (`group_id`) REFERENCES `unitgroup` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Unit_replace_with_type_id_fkey` FOREIGN KEY (`replace_with_type_id`) REFERENCES `unittype` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Unit_unit_type_id_fkey` FOREIGN KEY (`unit_type_id`) REFERENCES `unittype` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Unit_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=40943 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unitcargo`
--

DROP TABLE IF EXISTS `unitcargo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unitcargo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `unit_id` int(11) NOT NULL,
  `unit_type_id` int(11) NOT NULL,
  `unit_suffix` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mass_kg` int(11) DEFAULT NULL,
  `cargo_class` enum('CARGO','JTAC','MANPAD') COLLATE utf8mb4_unicode_ci NOT NULL,
  `spawn_airfield_id` int(11) DEFAULT NULL,
  `spawn_location_level` int(11) DEFAULT NULL,
  `spawn_zone` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `removed_at` datetime(3) DEFAULT NULL,
  `removed_reason` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `UnitCargo_unit_id_fkey` (`unit_id`),
  KEY `UnitCargo_unit_type_id_fkey` (`unit_type_id`),
  CONSTRAINT `UnitCargo_unit_id_fkey` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UnitCargo_unit_type_id_fkey` FOREIGN KEY (`unit_type_id`) REFERENCES `unittype` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6502 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unitgroup`
--

DROP TABLE IF EXISTS `unitgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unitgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `group_id` int(11) NOT NULL,
  `parent_group_id` int(11) DEFAULT NULL,
  `group_level` int(11) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `use_iads` tinyint(1) NOT NULL DEFAULT 0,
  `immortal` tinyint(1) NOT NULL DEFAULT 0,
  `disableai` tinyint(1) NOT NULL DEFAULT 0,
  `hidden_on_mfd` tinyint(1) NOT NULL DEFAULT 0,
  `uncontrollable` tinyint(1) NOT NULL DEFAULT 0,
  `group_cost` int(11) DEFAULT NULL,
  `group_desc` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_count` int(11) DEFAULT NULL,
  `template_class` enum('GROUND','SHIP') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'GROUND',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UnitGroup_campaign_id_group_id_key` (`campaign_id`,`group_id`),
  KEY `UnitGroup_parent_group_id_fkey` (`parent_group_id`),
  KEY `UnitGroup_created_by_id_fkey` (`created_by_id`),
  CONSTRAINT `UnitGroup_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UnitGroup_created_by_id_fkey` FOREIGN KEY (`created_by_id`) REFERENCES `user` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `UnitGroup_parent_group_id_fkey` FOREIGN KEY (`parent_group_id`) REFERENCES `unitgroup` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31182 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `unittype`
--

DROP TABLE IF EXISTS `unittype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unittype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `unit_type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shape_name` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `skill` enum('SKILL_RANDOM','SKILL_AVERAGE','SKILL_GOOD','SKILL_HIGH','SKILL_EXCELLENT') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'SKILL_EXCELLENT',
  `can_drive` tinyint(1) NOT NULL DEFAULT 0,
  `unit_class` enum('STANDARD','JTAC','SHELTER','CARGO','STATIC','AMMO','FUEL','NONE','FARP_UTIL','SHELTER_BUILD','EWR','LOGISTIC','AIR','AIR_RW','AIR_INTEL','FACTORY','JTAC_TOWER','COMPOSITION_BUILD') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'STANDARD',
  `is_static` tinyint(1) NOT NULL DEFAULT 0,
  `mass_kg` int(11) DEFAULT NULL,
  `cargo_count` int(11) DEFAULT NULL,
  `can_be_loaded` int(11) NOT NULL DEFAULT 0,
  `can_sling` tinyint(1) NOT NULL DEFAULT 0,
  `is_slot` tinyint(1) NOT NULL DEFAULT 0,
  `troop_count` int(11) DEFAULT NULL,
  `unpack_composition` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unpack_type_id` int(11) DEFAULT NULL,
  `factory_level` int(11) DEFAULT NULL,
  `shelter_level` int(11) DEFAULT NULL,
  `unit_level` int(11) DEFAULT NULL,
  `jtac_priority` int(11) NOT NULL DEFAULT 0,
  `unit_cost` int(11) DEFAULT NULL,
  `cargo_capacity` int(11) NOT NULL DEFAULT 0,
  `cargo_max_level` int(11) NOT NULL DEFAULT 0,
  `jtac_aggr_category` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UnitType_type_name_key` (`type_name`),
  KEY `UnitType_unpack_type_id_fkey` (`unpack_type_id`),
  CONSTRAINT `UnitType_unpack_type_id_fkey` FOREIGN KEY (`unpack_type_id`) REFERENCES `unittype` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=439 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ucid` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_seen` datetime(3) NOT NULL,
  `last_seen` datetime(3) NOT NULL,
  `online` tinyint(1) NOT NULL DEFAULT 0,
  `admin` tinyint(1) NOT NULL DEFAULT 0,
  `taccom` tinyint(1) NOT NULL DEFAULT 0,
  `discord_id` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crate_unpacks` int(11) NOT NULL DEFAULT 0,
  `taccom_revoked` tinyint(1) NOT NULL DEFAULT 0,
  `lotatc_pw` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `lotatc_user` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `User_ucid_key` (`ucid`),
  UNIQUE KEY `User_discord_id_key` (`discord_id`),
  UNIQUE KEY `User_lotatc_user_key` (`lotatc_user`)
) ENGINE=InnoDB AUTO_INCREMENT=368 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `useraliases`
--

DROP TABLE IF EXISTS `useraliases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `useraliases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name_until` datetime(3) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `UserAliases_user_id_fkey` (`user_id`),
  CONSTRAINT `UserAliases_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usercampaigncrates`
--

DROP TABLE IF EXISTS `usercampaigncrates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usercampaigncrates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `unpacks` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UserCampaignCrates_campaign_id_user_id_key` (`campaign_id`,`user_id`),
  KEY `UserCampaignCrates_user_id_fkey` (`user_id`),
  CONSTRAINT `UserCampaignCrates_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UserCampaignCrates_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userflightlegs`
--

DROP TABLE IF EXISTS `userflightlegs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userflightlegs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `flight_id` int(11) NOT NULL,
  `start_lat` decimal(15,12) NOT NULL,
  `start_lon` decimal(15,12) NOT NULL,
  `start_alt` decimal(9,3) NOT NULL,
  `start_time` datetime(3) NOT NULL,
  `start_airbase` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `end_lat` decimal(15,12) DEFAULT NULL,
  `end_lon` decimal(15,12) DEFAULT NULL,
  `end_alt` decimal(9,3) DEFAULT NULL,
  `end_time` datetime(3) DEFAULT NULL,
  `end_airbase` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  `distance_abs` int(11) DEFAULT NULL,
  `end_event` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `UserFlightLegs_flight_id_fkey` (`flight_id`),
  CONSTRAINT `UserFlightLegs_flight_id_fkey` FOREIGN KEY (`flight_id`) REFERENCES `userflights` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userflights`
--

DROP TABLE IF EXISTS `userflights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userflights` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `side` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `start` datetime(3) NOT NULL,
  `leg_count` int(11) DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  `distance_abs` int(11) DEFAULT NULL,
  `duration` time DEFAULT NULL,
  `end_event` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `unit_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `UserFlights_campaign_id_fkey` (`campaign_id`),
  KEY `UserFlights_user_id_fkey` (`user_id`),
  KEY `UserFlights_unit_type_id_fkey` (`unit_type_id`),
  CONSTRAINT `UserFlights_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UserFlights_unit_type_id_fkey` FOREIGN KEY (`unit_type_id`) REFERENCES `unittype` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `UserFlights_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userlives`
--

DROP TABLE IF EXISTS `userlives`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userlives` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `origin_airbase_id` int(11) DEFAULT NULL,
  `origin_farp_id` int(11) DEFAULT NULL,
  `life_class` enum('RW','FW') COLLATE utf8mb4_unicode_ci NOT NULL,
  `removed_at` datetime(3) NOT NULL,
  `returned` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UserLives_user_id_origin_airbase_id_life_class_key` (`user_id`,`origin_airbase_id`,`life_class`),
  UNIQUE KEY `UserLives_user_id_origin_farp_id_life_class_key` (`user_id`,`origin_farp_id`,`life_class`),
  KEY `UserLives_origin_airbase_id_fkey` (`origin_airbase_id`),
  KEY `UserLives_origin_farp_id_fkey` (`origin_farp_id`),
  CONSTRAINT `UserLives_origin_airbase_id_fkey` FOREIGN KEY (`origin_airbase_id`) REFERENCES `airbase` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UserLives_origin_farp_id_fkey` FOREIGN KEY (`origin_farp_id`) REFERENCES `farp` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UserLives_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1315 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userside`
--

DROP TABLE IF EXISTS `userside`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userside` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `coalition` enum('RED','BLUE') COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UserSide_campaign_id_user_id_key` (`campaign_id`,`user_id`),
  KEY `UserSide_user_id_fkey` (`user_id`),
  CONSTRAINT `UserSide_campaign_id_fkey` FOREIGN KEY (`campaign_id`) REFERENCES `campaign` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UserSide_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=379 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `weaponcooldown`
--

DROP TABLE IF EXISTS `weaponcooldown`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weaponcooldown` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `weapon` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `returns_at` datetime(3) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `WeaponCooldown_user_id_fkey` (`user_id`),
  CONSTRAINT `WeaponCooldown_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-28 18:47:56

-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: moviesearcher
-- ------------------------------------------------------
-- Server version	5.7.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tbl_userdata`
--

DROP TABLE IF EXISTS `tbl_userdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_userdata` (
  `name` varchar(70) NOT NULL,
  `username` varchar(35) NOT NULL,
  `password` varchar(100) NOT NULL,
  `twitter_username` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_userdata`
--

LOCK TABLES `tbl_userdata` WRITE;
/*!40000 ALTER TABLE `tbl_userdata` DISABLE KEYS */;
INSERT INTO `tbl_userdata` VALUES ('hello','hello','pbkdf2:sha256:50000$R0lnfUWZ$08e2ad1b96ebf342b07d909083c2152b06dfbe9d89be58fb4f51760087c84370',''),('hello','hello2','pbkdf2:sha256:50000$pTGNRV4D$084747bd0a9b23b6e0f0ceed8b85c4e3154a8ab16fdc41f402a9a246ac5362c4','shikiskhakis'),('hey','hey','pbkdf2:sha256:50000$ppg2S6U9$07971fa8417a9ea7a25577c3efc3f34f70c024ce3d4a86573a8b6f1ac7525242',NULL),('hello','hello3','pbkdf2:sha256:50000$BLb3rHFW$55e3b7b710ed031c3e7ca03c37fe4aa12bfa810d9c2f10f85a090ab11dd83cce','shikiskhakis'),('fndskjf','hello4','pbkdf2:sha256:50000$1v2tcau4$333e167fa7bbf3b616c7771daf18b82e4a89129a1d3175b121b1ded83a792cf2','shikiskhakis'),('nfdskjn','hello5','pbkdf2:sha256:50000$bHUAYAHf$9fdf7a7e557341bf433371235982a1b6480db1b0d3f8073919793069615f40fe',NULL),('huarhuiaiua','hello7','pbkdf2:sha256:50000$AkmpX2bt$de79fa56d9c8bf2b92f41c59a9c2de20c62e6b0b6152f4a58bbf9bf8adc1156e','shikiskhakis'),('dsjkfnks','hi','pbkdf2:sha256:50000$3VREAZbR$6b4f3e6e515bbafcec5f58913ae963a0021ebf1b3ac2fa0d550a4ec22a74a0bb',NULL),('Cool Kid','coolkid','pbkdf2:sha256:50000$HcciHY45$8cdd4685262465655d427a40a50ed2bb0e5d77ed558a0a927234acbe433f9246','moviesearcher41');
/*!40000 ALTER TABLE `tbl_userdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'moviesearcher'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_addTwitterUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addTwitterUser`(
	IN p_username VARCHAR(35),
	IN p_twitterun VARCHAR(15)
)
BEGIN
	update tbl_userData set twitter_username = p_twitterun where username = p_username;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_createUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
	IN p_name VARCHAR(70),
	IN p_username VARCHAR(35),
	IN p_password VARCHAR(100)
)
BEGIN
	IF (select exists (select 1 from tbl_userData where username = p_username)) THEN
		select 'Username already exists!';
	ELSE
		insert into tbl_userData
        (
			name,
			username,
			password
		)
        values
		(
			p_name,
			p_username,
			p_password
		);
	END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_validateUser` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateUser`(
	IN p_username VARCHAR(35)
)
BEGIN
	select * from tbl_userData where username = p_username;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-04 16:30:16

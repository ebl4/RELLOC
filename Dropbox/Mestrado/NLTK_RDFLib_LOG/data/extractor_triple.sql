-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: extractor
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
-- Table structure for table `triple`
--

DROP TABLE IF EXISTS `triple`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `triple` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject_type` varchar(50) NOT NULL,
  `subject_value` varchar(200) NOT NULL,
  `relation_type` varchar(50) NOT NULL,
  `relation_value` varchar(200) NOT NULL,
  `object_type` varchar(50) NOT NULL,
  `object_value` varchar(200) NOT NULL,
  `confidence` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `triple`
--

LOCK TABLES `triple` WRITE;
/*!40000 ALTER TABLE `triple` DISABLE KEYS */;
INSERT INTO `triple` VALUES (90,'O','search Pesqueira Pesqueira Overview Flag Seal Location','O','be in','LOCATION','Brazil Pesqueira Location',1),(91,'O','country Brazil Region Northeast State Pernambuco','O','settle','O','s found May th',1),(92,'PERSON','Pesqueira','O','be municipality in','O','state',1),(93,'O','it','O','have','O','estimate population',1),(94,'PERSON','Pesqueira','O','be','O','formerly know',1),(95,'O','municipality','O','be','O','create',1),(96,'O','seat','O','be','O','transfer',1),(97,'O','saint','O','with','PERSON','Águeda de Pesqueira',1),(98,'O','city','O','be make','O','seat of Roman Catholic Diocese',1),(99,'PERSON','São Bento','O','do','PERSON','Una',1),(100,'LOCATION','Brazil main economic activity','O','be base in','O','commerce',1),(101,'O','Children','O','have','O','Mortality',1),(102,'O','Referencesedit','O','^','O','b Estimativa Populacional Population Estimation',1);
/*!40000 ALTER TABLE `triple` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-28 10:52:34

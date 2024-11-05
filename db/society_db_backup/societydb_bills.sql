-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: societydb
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bills`
--

DROP TABLE IF EXISTS `bills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bills` (
  `bill_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `bill_for_month_of` varchar(20) NOT NULL,
  `book_number` int NOT NULL,
  `bill_number` int NOT NULL,
  `purpose_for` varchar(510) DEFAULT NULL,
  `rent_from` varchar(20) NOT NULL,
  `rent_to` varchar(20) NOT NULL,
  `at_the_rate_of` int NOT NULL,
  `total_months` int NOT NULL,
  `total_rupees` int NOT NULL,
  `received_date` date NOT NULL,
  `extra_payment` int DEFAULT NULL,
  `agreement_date` date DEFAULT NULL,
  `notes` varchar(1020) NOT NULL,
  `tenant_id` int NOT NULL,
  PRIMARY KEY (`bill_id`),
  UNIQUE KEY `id` (`bill_id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bills`
--

LOCK TABLES `bills` WRITE;
/*!40000 ALTER TABLE `bills` DISABLE KEYS */;
INSERT INTO `bills` VALUES (21,'Nov-2023',5,66,'For Residence','Nov-2023','Nov-2023',900,1,900,'2023-11-21',0,NULL,'',39),(23,'Jul-2023',13,1,'For Residence','Oct-2022','Jul-2023',400,10,4000,'2023-11-25',600,NULL,'',15),(24,'Dec-2023',3,26,'For Residence','Oct-2023','Dec-2023',1000,3,3000,'2023-11-25',0,'2023-05-15','',54),(25,'Nov-2023',3,27,'For Residence','Nov-2023','Nov-2023',450,1,450,'2023-11-27',55,NULL,'',51),(26,'Dec-2023',7,41,'For Residence','Jul-2023','Dec-2023',350,6,2100,'2023-11-29',0,NULL,'',59),(27,'Dec-2023',7,42,'For Residence','Sep-2023','Dec-2023',400,4,1600,'2023-12-03',0,NULL,'',68),(28,'Dec-2023',7,43,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-04',300,NULL,'Without Prejudice',67),(29,'Dec-2022',13,2,'For Residence','Oct-2022','Dec-2022',400,3,1200,'2023-12-06',0,NULL,'',4),(30,'Dec-2022',13,3,'For Residence','Oct-2022','Dec-2022',400,3,1200,'2023-12-06',0,NULL,'',5),(31,'Dec-2023',13,4,'For Residence','Oct-2023','Dec-2023',350,3,1050,'2023-12-09',0,NULL,'',13),(32,'Dec-2023',5,97,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-09',325,NULL,'',30),(33,'Dec-2023',7,44,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-09',230,NULL,'',70),(34,'Dec-2023',11,38,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-09',0,NULL,'',93),(35,'Dec-2023',11,39,'For Residence','Oct-2023','Dec-2023',350,3,1050,'2023-12-09',0,NULL,'',92),(36,'Dec-2023',11,40,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-09',0,NULL,'',91),(37,'Dec-2023',11,41,'For Residence','Oct-2023','Dec-2023',550,3,1650,'2023-12-09',0,NULL,'',90),(38,'Dec-2023',11,42,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-09',0,NULL,'',89),(39,'Dec-2023',11,43,'For Residence','Oct-2023','Dec-2023',350,3,1050,'2023-12-09',0,NULL,'',88),(40,'Dec-2023',11,44,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-09',0,NULL,'',87),(41,'Dec-2023',11,45,'For Residence','Oct-2023','Dec-2023',350,3,1050,'2023-12-09',405,NULL,'',86),(42,'Dec-2023',11,46,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-09',0,NULL,'',77),(43,'Dec-2023',11,47,'For Residence','Oct-2023','Dec-2023',350,3,1050,'2023-12-09',0,NULL,'',76),(44,'Dec-2023',11,48,'For Residence','Oct-2023','Dec-2023',500,3,1500,'2023-12-09',0,NULL,'',73),(45,'Dec-2023',11,49,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-09',0,NULL,'',72),(46,'Dec-2023',11,50,'For Residence','Oct-2023','Dec-2023',350,3,1050,'2023-12-09',0,NULL,'',71),(47,'Dec-2023',5,68,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-11',280,NULL,'',43),(48,'Dec-2023',5,69,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2023-12-11',280,NULL,'',44),(49,'Dec-2023',13,5,'For Residence','Oct-2023','Dec-2023',350,3,1050,'2023-12-11',245,NULL,'',14),(50,'Dec-2023',5,98,'For Residence','Dec-2023','Dec-2023',350,1,350,'2023-12-12',0,NULL,'',31),(51,'Dec-2023',3,28,'For Residence','Dec-2023','Dec-2023',450,1,450,'2023-12-12',0,NULL,'',51),(52,'Dec-2023',5,70,'For Residence','Dec-2023','Dec-2023',900,1,900,'2023-12-12',0,NULL,'',39),(53,'Dec-2023',5,71,'For Residence','Dec-2023','Dec-2023',900,1,900,'2023-12-12',0,NULL,'',40),(54,'Dec-2023',13,6,'For Residence','Oct-2023','Dec-2023',350,3,1050,'2023-12-12',0,NULL,'',17),(55,'Dec-2023',11,51,'For Residence','Apr-2023','Dec-2023',500,9,4500,'2023-12-14',0,NULL,'',84),(56,'Dec-2023',7,45,'For Residence','Dec-2023','Dec-2023',400,1,400,'2023-12-18',0,NULL,'',61),(57,'Oct-2023',5,99,'For Residence','Mar-2023','Oct-2023',400,8,3200,'2023-12-19',0,NULL,'',29),(58,'Dec-2023',13,7,'For Residence','Sep-2023','Dec-2023',400,4,1600,'2023-12-23',0,NULL,'',18),(59,'Dec-2023',13,8,'For Residence','Sep-2023','Dec-2023',350,4,1400,'2023-12-28',280,NULL,'',10),(60,'Nov-2023',5,100,'For Residence','Jan-2023','Nov-2023',450,11,4950,'2024-01-01',0,NULL,'',35),(61,'Jan-2024',6,1,'For Residence','Jan-2024','Jan-2024',350,1,350,'2024-01-02',0,NULL,'',31),(62,'Feb-2024',6,2,'For Residence','Jan-2024','Feb-2024',500,2,1000,'2024-01-02',0,NULL,'',32),(64,'Dec-2024',13,9,'For Residence','Jan-2022','Dec-2024',400,36,14400,'2024-01-11',500,NULL,'',20),(65,'Mar-2023',11,52,'For Residence','Oct-2022','Mar-2023',500,6,3000,'2024-01-11',0,NULL,'',81),(66,'Mar-2023',11,53,'For Residence','Oct-2022','Mar-2023',500,6,3000,'2024-01-11',0,NULL,'',83),(69,'Jan-2024',13,10,'For Residence','Dec-2023','Jan-2024',350,2,700,'2024-01-13',0,'2024-02-14','',7),(70,'Dec-2023',7,46,'For Residence','Oct-2023','Dec-2023',400,3,1200,'2024-01-14',0,NULL,'',69),(73,'Mar-2024',3,30,'For Residence Testing','Jan-2024','Mar-2024',1000,3,3000,'2024-01-21',0,NULL,'',54);
/*!40000 ALTER TABLE `bills` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-11 16:41:03

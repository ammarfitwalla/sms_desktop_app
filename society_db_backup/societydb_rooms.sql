-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: societydb
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rooms` (
  `room_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `house_id` int DEFAULT NULL,
  `cts_id` int DEFAULT NULL,
  `room_number` varchar(255) NOT NULL,
  PRIMARY KEY (`room_id`),
  UNIQUE KEY `id` (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rooms`
--

LOCK TABLES `rooms` WRITE;
/*!40000 ALTER TABLE `rooms` DISABLE KEYS */;
INSERT INTO `rooms` VALUES (4,4,5,'1 Gr. & Upr. Fl.'),(5,4,6,'2 Gr. & Upr. Fl.'),(6,4,7,'3 Gr. & Upr. Fl.'),(9,4,10,'4 Gr. & Upr. Fl.'),(10,4,11,'5 Gr. & Upr. Fl.'),(11,4,12,'6 Gr. & Upr. Fl.'),(12,4,13,'7 Gr. & Upr. Fl.'),(13,4,14,'8 Gr. & Upr. Fl.'),(14,4,15,'9 Gr. & Upr. Fl.'),(15,4,16,'10 Gr. & Upr. Fl.'),(16,4,17,'11 Gr. & Upr. Fl.'),(17,4,18,'12 Gr. & Upr. Fl.'),(18,4,19,'13 Gr. Fl.'),(19,4,20,'14 Gr. Fl.'),(20,4,21,'13A & 14A Upr. Fl.'),(21,4,22,'15 Gr. & Upr. Fl.'),(22,4,23,'16 Gr. & Upr. Fl.'),(23,4,24,'17 Gr. Fl.'),(24,4,24,'17A Upr. Fl.'),(25,4,25,'18 Gr. & Upr. Fl.'),(26,4,26,'19 Gr. & Upr. Fl.'),(27,5,27,'1 '),(28,5,28,'2'),(29,5,29,'3 '),(30,5,30,'4'),(31,5,31,'5 Gr. Fl.'),(32,5,31,'5A Upr. Fl.'),(33,5,32,'6A Gr. & Upr. Fl. & 6B Upr. Fl.'),(34,5,32,'6B Gr. Fl.'),(35,5,33,'7'),(36,5,34,'8'),(37,5,35,'9'),(38,5,36,'10'),(39,5,37,'11'),(40,6,38,'1 Gr. & Upr. Fl.'),(41,6,39,'2 Gr. Fl.'),(42,6,39,'2A 1st Fl.'),(43,6,40,'3 '),(44,6,41,'4'),(45,6,42,'5 Gr. Fl.'),(46,6,42,'5A Upr. Fl.'),(47,6,43,'6 Gr. & Upr. Fl.'),(48,6,43,'6A'),(49,6,44,'7'),(50,6,45,'8'),(51,6,46,'9'),(52,6,47,'10 Gr. & Upr. Fl.'),(53,7,48,'1'),(54,7,49,'2'),(55,7,49,'2A'),(56,7,50,'3 '),(57,7,51,'4'),(58,8,52,'A Room Above W.C. Block'),(59,9,53,'1'),(60,9,54,'2'),(61,9,55,'3'),(62,9,56,'4'),(63,9,57,'5'),(64,9,58,'6'),(65,9,59,'7'),(66,9,60,'8'),(67,9,61,'9'),(68,9,62,'10'),(69,9,63,'11'),(70,9,64,'12'),(71,9,65,'13 & 14'),(72,9,66,'15'),(73,10,67,'1 Gr. Fl.'),(74,10,67,'1A Upr. Fl.'),(75,10,67,'1B IInd Fl.'),(76,10,68,'2 Gr. Fl.'),(77,10,68,'2A Upr. Fl.'),(78,10,69,'3 Gr. Fl.'),(79,10,69,'3A Upr. Fl.'),(80,10,70,'4 Gr. Fl.'),(81,10,70,'4A Upr. Fl.'),(82,10,71,'5 Gr. Fl.'),(83,10,71,'5A Upr. Fl.'),(84,10,71,'6 Gr. Fl.'),(85,10,71,'6A Upr. Fl.'),(86,10,72,'7 Gr. Fl.'),(87,10,72,'7A Upr. Fl.'),(88,10,73,'8 Gr. Fl.'),(89,10,73,'8A Upr. Fl.'),(90,10,74,'9 Gr. Fl.'),(91,10,74,'9A Upr. Fl.'),(92,10,75,'10 Gr. Fl.'),(93,10,75,'10A Upr. Fl.'),(94,10,76,'11 Gr. Fl.'),(95,10,76,'11A Upr. Fl.'),(96,11,77,'1'),(97,11,78,'2 & 4'),(98,11,79,'3 ');
/*!40000 ALTER TABLE `rooms` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-13 17:07:14

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
-- Table structure for table `tenants`
--

DROP TABLE IF EXISTS `tenants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tenants` (
  `tenant_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `tenant_name` varchar(255) NOT NULL,
  `notes` varchar(1024) DEFAULT NULL,
  `tenant_mobile` varchar(15) DEFAULT NULL,
  `tenant_dod` date DEFAULT NULL,
  `tenant_gender` enum('Male','Female','Others') NOT NULL,
  `current_tenant` enum('True','False') NOT NULL,
  `room_id` int NOT NULL,
  PRIMARY KEY (`tenant_id`),
  UNIQUE KEY `id` (`tenant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenants`
--

LOCK TABLES `tenants` WRITE;
/*!40000 ALTER TABLE `tenants` DISABLE KEYS */;
INSERT INTO `tenants` VALUES (4,'Zebun-Nisa w/o Shaikh Abdul Ghani Abdush-Shakoor',NULL,'+91 9987470393','2020-06-30','Female','True',4),(5,'Abdul-Ghani Abdush-Shakoor',NULL,NULL,'2000-12-29','Male','True',5),(6,'Mehrunnisa Mohammed Ishaque Khan','','+91 9768729683',NULL,'Female','True',6),(7,'Basheer Abdul-Kareem',NULL,'+91 8879585067,','2000-01-01','Male','True',9),(8,'Muhammad Miyan Haji Muhammad Farooq',NULL,'+91 9967199395','2000-01-01','Male','True',10),(9,'Ansari Nayab Miyan s/o Muhammad Miyan','','+91 9967199395',NULL,'Male','True',11),(10,'Bismillah Bi wd/o Muhammad Naseer','','','2004-04-11','Female','True',12),(11,'Shaikh Muhammad Khalid Muhammad Iqbal','','+91 9821199959',NULL,'Male','True',13),(12,'Abdul-Jaleel Abdul Hakeem Ansari','','+91 9820020782',NULL,'Male','True',14),(13,'Iqbal Ahmad Abdul-Hameed Shaikh',NULL,'+91 9136428963',NULL,'Male','True',15),(14,'Muhammad Naeem Abdul-Qadir',NULL,'+91 9987133130','2022-12-29','Male','True',16),(15,'Sufiya Abdul-Hamid Khan','','+91 9323168258',NULL,'Female','True',17),(16,'Sagheer Miyan s/o Ansari Babu Abdul-Azeez','','+91 9967077695',NULL,'Male','True',18),(17,'Mateen Miyan s/o Ansari Babu Abdul-Azeez','','+91 7021725912','2021-01-08','Male','True',19),(18,'Muhammad Haneef s/o Ansari Babu Abdul-Azeez','','+91 9867703771',NULL,'Male','True',20),(19,'Wazeer Khan Ramazan Khan','','+91 9322833045','2000-01-01','Male','True',21),(20,'Sagheer Ahmad Hafeezullah','','+91 9820871147','2016-02-13','Male','True',22),(21,'Shareef s/o Ansari Babu Abdul-Azeez','','+919594501984','2012-01-15','Male','True',23),(22,'Laeeq Miyan s/o Ansari Babu Abdul-Azeez','','+91 9975951913','2015-03-07','Male','True',24),(23,'Abdus-Salam Muhammad Ishaque Ansari','','+91 9224681067',NULL,'Male','True',25),(24,'Tahira Bi wd/o Abdur-Rasheed','','+91 9892661102','2000-01-01','Female','True',26),(25,'Ansari Imrana Mehmood Ayaz',NULL,NULL,NULL,'Female','True',27),(26,'Khairun-Nisa w/o Abdur-Rasheed',NULL,NULL,'2000-01-01','Female','True',28),(27,'Mohammed Iqbal Mohammed Ismail Shaikh','','',NULL,'Male','True',29),(28,'Anjuman Ittehadul Muslimeen, Kurla','','',NULL,'Male','True',30),(29,'Safiyah Usman Ansari','','+91 7710926153',NULL,'Female','True',31),(30,'Fahmeedah Iqbal Ahmad Shaikh','','',NULL,'Female','True',32),(31,'Kulsum w/o Mukhtar Ahmad Ansari','','','2023-08-21','Female','True',33),(32,'Sadaf Muhammad Muzzammil Ansari','','',NULL,'Female','True',34),(33,'Muhammad Isa Amjad Ali','','',NULL,'Male','True',35),(34,'Hashimi Bi wd/o Muhammad Islam','','','2014-01-05','Female','True',36),(35,'Maimoona Ismail Memon','','','2023-10-16','Female','True',37),(36,'Mehrun-Nisa Saiyid Nayab Shah','','','2023-04-16','Female','True',38),(37,'Shahjahan Begum w/o Nooruddin Shaikh','','',NULL,'Female','True',39),(38,'Shabana Parveen w/o Shafeel Ahmed Shaikh','','+91 9967542418',NULL,'Female','True',40),(39,'Mohd. Noman Mohd. Usman','','+91 9987245605',NULL,'Male','True',41),(40,'Abdul Hakim Abdul Aziz Fitwalla','','+91 9867600313',NULL,'Male','True',42),(41,'Anwari Bano w/o Muhammed Nabi Shaikh',NULL,'+919892933106',NULL,'Female','True',43),(42,'Sharafat Husain Saadiq Husain','','+91 8691887727','2000-01-01','Male','True',44),(43,'Muhammad Qasim Muhammad Ibrahim','','','2000-01-01','Male','True',45),(44,'Shaikh Javed Akhtar Mohamed Qasim','','',NULL,'Male','True',46),(45,'Hajarah Khatoon w/o Abdur-Rahmaan Shaikh','','','2019-10-29','Female','True',47),(46,'Ishrat Jehan Abdur-Rahmaan Shaikh','','',NULL,'Female','True',48),(47,'Mussarrat Jahan Abdur-Rahmaan Shaikh','','',NULL,'Female','True',49),(48,'Saiyid Qamar Ali Ahmad Ali','','','2000-01-01','Male','True',50),(49,'Qamar Ali Ahmad Ali','','','2000-01-01','Male','True',51),(50,'Raziud-Deen Sirajud-Deen',NULL,'+91 9867735030',NULL,'Male','True',52),(51,'Saeeda Begum w/o Abdul-Karim Yadgri','','+91 8652617827','2018-01-19','Female','True',53),(52,'Hameedah Bi d/o Shareef Khan','Rm. No.1, Gr. Flr., Zuha Apt., Insha Ngr., Amrut Ngr., Mumbra-...., Dist. Thane, Mahrashtra.','',NULL,'Female','True',54),(53,'Hameedah Burhanuddin Chawdhry  & Umanuddin Burhanuddin Chawdhry','','',NULL,'Female','True',55),(54,'Rukhsar Shahrukh Sayyed ','','',NULL,'Female','True',56),(55,'Ghulam Muhammad Khan Ali Muhammad Khan','','','2000-01-01','Male','True',57),(56,'Shaikh Nazir Ahmed s/o Muhyid-Deen','Noor Manzil, 200/13, Opp. \'L\' Ward BMC Office, Behind KNS Bank, S.G. Barve Marg, Kurla(W), Mumbai-400070','+91 9664663616','2000-01-01','Male','True',58),(57,'Mahboob Bi Ahmad Sahib','','','2000-01-01','Female','True',59),(58,'Muhammad Shabbir Ahmad Sahib','','',NULL,'Male','True',60),(59,'Asif s/o Shamsud-deen Shaikh & Aqeela d/o Shamsud-deen Shaikh','','+91 9969431918',NULL,'Male','True',61),(60,'Shaikh Abdur-Rahmaan Ameer',NULL,'+91 9892746181','2000-01-01','Male','True',62),(61,'Noor Jahan Zubair Sakharkar','','+91 9324521632',NULL,'Female','True',63),(62,'Ibrahim Chhota Wawda & Fahmeedah Ibrahim Wawda',NULL,'+91 9324956124',NULL,'Male','True',64),(63,'Fahmeedah Ibrahim Wawda','','',NULL,'Female','True',65),(64,'Nusrat Shaikh Abdur-Rahmaan','','',NULL,'Female','True',66),(65,'Shaikh Abdur-Rahmaan Abdul-Qadir','','','2019-10-14','Male','True',67),(66,'Samun Nizamuddin Khilji & Mussarrat Samun Khilji','','+91 9821716098',NULL,'Male','True',68),(67,'Shaikh Muhammad Tarique Muhammad Yaqub','','+91 9004438484','2015-07-21','Male','True',69),(68,'Haleema Bi d/o Dada Miyan','','+91 8879845747',NULL,'Female','True',70),(69,'Alaud-Deen Khan Chhotey Khan','','','2020-05-31','Male','True',71),(70,'Ansari Farhan Abdul Subhan','','+91 9820936948',NULL,'Male','True',72),(71,'Khaleel Ahmad Abdul-Hameed','','+91 9224158420','2022-11-18','Male','True',73),(72,'Maswud Ahmad Shaikh Khaleel Ahmad','','+91 9224158420',NULL,'Male','True',74),(73,'Fitwalla Ishaque Ibrahim','','',NULL,'Male','True',75),(74,'Kamal Ahmad Ansari','','+91 9137266460',NULL,'Male','True',76),(75,'Raziya Bano w/o Kamal Ahmad Ansari','','+91 9820628396',NULL,'Male','True',77),(76,'Abdul-Kareem Haji Ahmad','','','2001-01-01','Male','True',78),(77,'Zuhrah Abdul-Kareem','','',NULL,'Female','True',79),(78,'Muhammad Husain Rahmatullah','','','2001-01-01','Male','True',80),(79,'Ansari Iqbal Husain s/o Abdur-Rahman',NULL,NULL,'2012-08-30','Male','True',81),(80,'Atiullah Manzoor Shaikh','','+91 9892802772',NULL,'Male','True',82),(81,'Fatima w/o Niyaz Mohd. Khan','','',NULL,'Female','True',83),(82,'Sheereen Bai w/o Muhammad Rafeeq Quraishi','','','2001-01-01','Female','True',84),(83,'Niyaz Mohammad Khan s/o Niyamat Khan',NULL,NULL,NULL,'Male','True',85),(84,'Farida Abdul Razzaque Engineer',NULL,NULL,NULL,'Female','True',86),(85,'Jaffar Niyaz MohammadKhan & Fauziya Niyaz Mohammad Khan','','',NULL,'Male','True',87),(86,'Sabira w/o Madar Bakhsh','','','2001-01-01','Female','True',88),(87,'Shaikh Mahmood Ali Abdur-Rasheed ','','',NULL,'Male','True',89),(88,'Fitwalla Bilquees Abdur Rafe & Mamsa Mariyam Ahmed ','','',NULL,'Female','True',90),(89,'Fitwalla Bilquees Abdur Rafe & Mamsa Haroon Ahmed','','',NULL,'Female','True',91),(90,'Shoeb Ahmed Nazir Ahmed Shaikh','','',NULL,'Male','True',92),(91,'Rais Ahmed Shaikh s/o Nazir Ahmed Shaikh ','','',NULL,'Male','True',93),(92,'Nazeer Ahmad Abdul-Lateef','','','2001-01-01','Male','True',94),(93,'Rais Ahmed Shaikh s/o Nazir Ahmed Shaikh','','',NULL,'Male','True',95),(94,'Khursheed Ali Asad Ali','','+91 9821558495','2001-01-01','Male','True',96),(95,'Amina w/o Sayyed Ibrahim','','',NULL,'Female','True',97),(96,'Tahzeebun-Nisa w/o Shamsud-Deen','','','2001-01-01','Female','True',98);
/*!40000 ALTER TABLE `tenants` ENABLE KEYS */;
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

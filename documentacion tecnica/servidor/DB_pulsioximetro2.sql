-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.5.9-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Volcando estructura para tabla pulsioximetrodb.anomalias
CREATE TABLE IF NOT EXISTS `anomalias` (
  `ID_dispositivo` varchar(12) NOT NULL DEFAULT '',
  `Fecha` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Infarto` binary(1) DEFAULT NULL,
  `Fibrilacion` binary(1) DEFAULT NULL,
  PRIMARY KEY (`ID_dispositivo`,`Fecha`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla pulsioximetrodb.anomalias: ~1 rows (aproximadamente)
DELETE FROM `anomalias`;
/*!40000 ALTER TABLE `anomalias` DISABLE KEYS */;
INSERT INTO `anomalias` (`ID_dispositivo`, `Fecha`, `Infarto`, `Fibrilacion`) VALUES
	('A8032A6A4FAA', '2021-05-30 20:53:55', _binary 0x31, NULL);
/*!40000 ALTER TABLE `anomalias` ENABLE KEYS */;

-- Volcando estructura para tabla pulsioximetrodb.bateria
CREATE TABLE IF NOT EXISTS `bateria` (
  `ID_Dispositivo` varchar(12) NOT NULL DEFAULT '',
  `Bateria` tinyint(4) DEFAULT NULL,
  `Tiempo` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`ID_Dispositivo`,`Tiempo`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla pulsioximetrodb.bateria: ~0 rows (aproximadamente)
DELETE FROM `bateria`;
/*!40000 ALTER TABLE `bateria` DISABLE KEYS */;
/*!40000 ALTER TABLE `bateria` ENABLE KEYS */;

-- Volcando estructura para tabla pulsioximetrodb.pulso
CREATE TABLE IF NOT EXISTS `pulso` (
  `ID_Dispositivo` varchar(12) NOT NULL DEFAULT '',
  `Pulso` float unsigned zerofill NOT NULL DEFAULT 000000000000,
  `O2` tinyint(4) DEFAULT NULL,
  `Tiempo` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`ID_Dispositivo`,`Tiempo`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla pulsioximetrodb.pulso: ~3 rows (aproximadamente)
DELETE FROM `pulso`;
/*!40000 ALTER TABLE `pulso` DISABLE KEYS */;
INSERT INTO `pulso` (`ID_Dispositivo`, `Pulso`, `O2`, `Tiempo`) VALUES
	('A8032A6A4FAA', 000000000000, 0, '2021-05-30 20:53:58'),
	('A8032A6A4FAA', 000000000000, 0, '2021-05-30 20:53:59'),
	('A8032A6A4FAA', 000000000000, 0, '2021-05-30 20:54:00');
/*!40000 ALTER TABLE `pulso` ENABLE KEYS */;

-- Volcando estructura para tabla pulsioximetrodb.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `ID_Usuario` int(11) unsigned zerofill NOT NULL DEFAULT 00000000000,
  `ID_Dispositivo` varchar(12) DEFAULT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellidos` varchar(50) DEFAULT NULL,
  `Edad` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`ID_Usuario`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla pulsioximetrodb.usuarios: ~1 rows (aproximadamente)
DELETE FROM `usuarios`;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` (`ID_Usuario`, `ID_Dispositivo`, `Nombre`, `Apellidos`, `Edad`) VALUES
	(00000000001, 'C05003321F33', 'Eric', 'Garcia', 23);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

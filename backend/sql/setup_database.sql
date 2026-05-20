-- ============================================================
-- BiblioSmart — Full Database Setup
-- Run as root: sudo mysql < setup_database.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS biblioteca
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'proiectbiblioteca26';
GRANT ALL PRIVILEGES ON biblioteca.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;

USE biblioteca;

-- ------------------------------------------------------------
-- 1. carti — book catalog
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS carti (
    carte_id        INT          AUTO_INCREMENT PRIMARY KEY,
    titlu           VARCHAR(50)  NOT NULL,
    autor           VARCHAR(50)  NOT NULL,
    ISBN            VARCHAR(13)  NOT NULL UNIQUE,
    stoc_total      INT          NULL,
    stoc_disponibil INT          NULL,
    imprumutat      TINYINT(1)   NULL,
    gen             VARCHAR(255) NOT NULL,
    pozitie         VARCHAR(100) NULL,
    cod             VARCHAR(50)  NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 2. users — user accounts
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id         INT          AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    email           VARCHAR(50)  NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    rol             ENUM('user', 'bibliotecar') NOT NULL DEFAULT 'user',
    telefon         VARCHAR(50)  NULL UNIQUE,
    description     VARCHAR(255) NULL,
    club            TINYINT(1)   NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 3. carti_citite — read / returned books per user
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS carti_citite (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    user_id  INT NOT NULL,
    carte_id INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 4. recenzii — reviews (rating + comment per book per user)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS recenzii (
    id          INT          AUTO_INCREMENT PRIMARY KEY,
    user_id     INT          NOT NULL,
    carte_id    INT          NOT NULL,
    nota        INT          NOT NULL,
    comentariu  VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 5. anunturi — announcements posted by librarian
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS anunturi (
    anunt_id       INT          AUTO_INCREMENT PRIMARY KEY,
    titlu          VARCHAR(255) NOT NULL,
    anunt          TEXT         NULL,
    data_publicare DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    aprecieri      INT          NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 6. anunturi_aprecieri — likes on announcements
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS anunturi_aprecieri (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    anunt_id INT NOT NULL,
    user_id  INT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 7. cereri_carti — physical book borrow request queue
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cereri_carti (
    cerere_id  INT      AUTO_INCREMENT PRIMARY KEY,
    user_id    INT      NOT NULL,
    carte_id   INT      NOT NULL,
    status           ENUM('pending', 'approved', 'rejected', 'ridicat') NOT NULL DEFAULT 'pending',
    ridicare_de_la   DATETIME NULL,
    ridicare_pana_la DATETIME NULL,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(user_id)  ON DELETE CASCADE,
    FOREIGN KEY (carte_id) REFERENCES carti(carte_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 8. imprumuturi_active — approved and active loans
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS imprumuturi_active (
    imprumut_id   INT      AUTO_INCREMENT PRIMARY KEY,
    user_id       INT      NOT NULL,
    carte_id      INT      NOT NULL,
    data_imprumut DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_scadenta DATETIME NOT NULL,
    FOREIGN KEY (user_id)  REFERENCES users(user_id)  ON DELETE CASCADE,
    FOREIGN KEY (carte_id) REFERENCES carti(carte_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 9. activitati_club — book club activities / posts
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS activitati_club (
    activitate_id INT          AUTO_INCREMENT PRIMARY KEY,
    titlu         VARCHAR(255) NOT NULL,
    continut      TEXT         NULL,
    tip           ENUM('anunt', 'sarcina', 'activitate') NOT NULL DEFAULT 'activitate',
    saptamana     ENUM('anterioara', 'curenta', 'urmatoare') NOT NULL DEFAULT 'curenta',
    creat_de      INT          NOT NULL,
    creat_la      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizat_la DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    nume_imagine  VARCHAR(255) NULL,
    FOREIGN KEY (creat_de) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 10. comentarii_activitati — comments on club activities
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS comentarii_activitati (
    comentariu_id INT      AUTO_INCREMENT PRIMARY KEY,
    activitate_id INT      NOT NULL,
    user_id       INT      NOT NULL,
    continut      TEXT     NOT NULL,
    creat_la      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (activitate_id) REFERENCES activitati_club(activitate_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)       REFERENCES users(user_id)                 ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 11. club_invites — invite tokens for joining the book club
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS club_invites (
    token      VARCHAR(128) PRIMARY KEY,
    created_by INT          NOT NULL,
    expires_at DATETIME     NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

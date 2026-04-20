UPDATE users
SET rol = 'bibliotecar'
WHERE LOWER(TRIM(rol)) IN ('1', 'administrator', 'admin', 'bibliotecar');

UPDATE users
SET rol = 'user'
WHERE rol IS NULL
   OR TRIM(rol) = ''
   OR LOWER(TRIM(rol)) NOT IN ('user', 'bibliotecar');

ALTER TABLE users
MODIFY rol ENUM('user', 'bibliotecar') NOT NULL DEFAULT 'user';
-- Add image filename support for club announcements
ALTER TABLE activitati_club
ADD COLUMN nume_imagine VARCHAR(255) NULL AFTER actualizat_la;

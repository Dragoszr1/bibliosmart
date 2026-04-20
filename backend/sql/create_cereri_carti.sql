-- Book borrow requests table
CREATE TABLE IF NOT EXISTS cereri_carti (
    cerere_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    carte_id    INT NOT NULL,
    status      ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(user_id)  ON DELETE CASCADE,
    FOREIGN KEY (carte_id) REFERENCES carti(carte_id) ON DELETE CASCADE
);

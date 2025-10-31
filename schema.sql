
CREATE DATABASE IF NOT EXISTS virtual_study_groups;
USE virtual_study_groups;

CREATE TABLE IF NOT EXISTS users(
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100), email VARCHAR(150) UNIQUE, password_hash VARCHAR(255),
  role ENUM('student','moderator','admin') DEFAULT 'student',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS study_groups(
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL, description TEXT, owner_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(owner_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS messages(
  id INT AUTO_INCREMENT PRIMARY KEY,
  group_id INT NOT NULL, user_id INT NOT NULL, content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(group_id) REFERENCES study_groups(id),
  FOREIGN KEY(user_id) REFERENCES users(id)
);

INSERT INTO users(name,email) VALUES('Demo User','demo@example.com');
INSERT INTO study_groups(name,description,owner_id) VALUES('Software Engineering','Discuss SRS/SDD',1);

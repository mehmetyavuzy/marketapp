DROP TABLE IF EXISTS recipes;

CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) CHARACTER SET utf8mb4,
    ingredients TEXT CHARACTER SET utf8mb4,
    instructions TEXT CHARACTER SET utf8mb4,
    image_path VARCHAR(255) CHARACTER SET utf8mb4
);

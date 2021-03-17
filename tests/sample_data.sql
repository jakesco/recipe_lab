INSERT INTO ingredient VALUES (1, "Unsalted Crackers", 140, 1.23, 3, "cracker");
INSERT INTO ingredient VALUES (2, "Unsalted Butter", 16, 2.94, 1, "oz");
INSERT INTO ingredient VALUES (3, "Brown Sugar", 32, 2.73, 1, "oz");
INSERT INTO ingredient VALUES (4, "Sea Salt", 4.4, 0.98, 1, "oz");
INSERT INTO ingredient VALUES (5, "Vanilla Extract", 2, 4.98, 2, "fl. oz");
INSERT INTO ingredient VALUES (6, "Semi-Sweet Chocolate Chips", 12, 1.74, 1, "oz");

INSERT INTO recipe VALUES (1, "Chocolate Caramel Toffee", 24, "cracker", 20);

INSERT INTO recipe_ingredient VALUES (1, 1, 40);
INSERT INTO recipe_ingredient VALUES (1, 2, 8);
INSERT INTO recipe_ingredient VALUES (1, 3, 8);
INSERT INTO recipe_ingredient VALUES (1, 4, 0.0425);
INSERT INTO recipe_ingredient VALUES (1, 5, 0.085);
INSERT INTO recipe_ingredient VALUES (1, 6, 12);
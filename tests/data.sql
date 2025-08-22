INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f');

INSERT INTO product (name, stock, price, description, owner_id)
VALUES
  ('Test Product', 10, 100, 'Test Description', 1);

INSERT INTO history (product_id, user_id, price, quantity, action)
VALUES
  (1, 1, 100, 10, 'buy');
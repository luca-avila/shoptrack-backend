INSERT INTO user (username, password)
VALUES
  ('test', 'scrypt:32768:8:1$rgKhpTihDO4zcCCw$0537d1180edf057722094ceba47af4a2dec7ff355d50be5be6a23c5a766d43c08fb413421781b14a8989772b911d61590d584b4168c295bce306712b06907986');

INSERT INTO product (name, stock, price, description, owner_id)
VALUES
  ('Test Product', 10, 100, 'Test Description', 1);

INSERT INTO history (product_id, product_name, user_id, price, quantity, action)
VALUES
  (1, 'Test Product', 1, 100, 10, 'buy');
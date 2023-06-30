INSERT IGNORE INTO campaign (theatre, start)
 VALUES ('Syria', '2021-01-01 00:00:00');

INSERT IGNORE INTO user (discord_id)
  VALUES ('FAKE');

INSERT IGNORE INTO userside (user_id, campaign_id, coalition)
VALUES (
  (SELECT id FROM user LIMIT 1),
  (SELECT id FROM campaign ORDER BY id DESC LIMIT 1),
  'blue'
);

COMMIT;

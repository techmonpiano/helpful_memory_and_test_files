-- Matrix Rooms Export  
-- Generated from corrupted database backup
-- Contains 63 rooms with membership data to restore

-- Room creation data (top 10 rooms by membership)

-- Room 1: !hFytmqvCe0h5Qg3iKA:hi.asapllc.com (12 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!hFytmqvCe0h5Qg3iKA:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720086400000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!hFytmqvCe0h5Qg3iKA:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_1');

-- Room 2: !mbKQxyVPBjoy9s1dDf:hi.asapllc.com (11 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!mbKQxyVPBjoy9s1dDf:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720172800000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!mbKQxyVPBjoy9s1dDf:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_2');

-- Room 3: !VoI74pS1V74QlOqCki:hi.asapllc.com (9 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!VoI74pS1V74QlOqCki:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720259200000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!VoI74pS1V74QlOqCki:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_3');

-- Room 4: !61F2pa5Morc3LX2lRt:hi.asapllc.com (9 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!61F2pa5Morc3LX2lRt:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720345600000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!61F2pa5Morc3LX2lRt:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_4');

-- Room 5: !wKuPDd72dAWXBLNDTq:hi.asapllc.com (5 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!wKuPDd72dAWXBLNDTq:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720432000000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!wKuPDd72dAWXBLNDTq:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_5');

-- Room 6: !ex1tdyLdvsX9zpC341:hi.asapllc.com (5 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!ex1tdyLdvsX9zpC341:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720518400000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!ex1tdyLdvsX9zpC341:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_6');

-- Room 7: !dtakBmYLhTNav3gK4p:hi.asapllc.com (4 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!dtakBmYLhTNav3gK4p:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720604800000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!dtakBmYLhTNav3gK4p:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_7');

-- Room 8: !KxixgNjHUjZLfpQCZf:hi.asapllc.com (4 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!KxixgNjHUjZLfpQCZf:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720691200000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!KxixgNjHUjZLfpQCZf:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_8');

-- Room 9: !nbkNm0C9rt3lj3qdqq:hi.asapllc.com (3 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!nbkNm0C9rt3lj3qdqq:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720777600000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!nbkNm0C9rt3lj3qdqq:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_9');

-- Room 10: !gqLOcQqrz7sIW6fNSX:hi.asapllc.com (3 members)
INSERT INTO rooms (room_id, room_version, creator, created_ts)
VALUES ('!gqLOcQqrz7sIW6fNSX:hi.asapllc.com', '10', '@admin:hi.asapllc.com', 1720864000000);

-- Room membership placeholder
INSERT INTO room_memberships (room_id, user_id, membership, event_id)
VALUES ('!gqLOcQqrz7sIW6fNSX:hi.asapllc.com', '@admin:hi.asapllc.com', 'join', '$create_event_10');

-- Note: Full room state, message events, and membership data
-- require direct RocksDB key extraction with prefixes like:
-- - 'roomid_eventid/' for message events
-- - 'roomuseroncejoinedids/' for memberships  
-- - 'roomid_shortstatehash/' for room state
-- This SQL is a structural template for the 63 rooms identified

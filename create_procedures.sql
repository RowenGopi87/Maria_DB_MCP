-- Create User Management Stored Procedures

DELIMITER //

-- Procedure 1: Create User (username, password) -> returns user_id
DROP PROCEDURE IF EXISTS CreateUser//
CREATE PROCEDURE CreateUser(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255),
    OUT p_user_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Check if user already exists
    SELECT user_id INTO p_user_id FROM users WHERE username = p_username LIMIT 1;
    
    -- If user doesn't exist, create new user
    IF p_user_id IS NULL THEN
        INSERT INTO users (username, password) VALUES (p_username, p_password);
        SET p_user_id = LAST_INSERT_ID();
    END IF;
    
    COMMIT;
END//

-- Procedure 2: Update Balance (calls CreateUser, then updates balance)
DROP PROCEDURE IF EXISTS UpdateBalance//
CREATE PROCEDURE UpdateBalance(
    IN p_username VARCHAR(50),
    IN p_password VARCHAR(255), 
    IN p_balance DECIMAL(10,2)
)
BEGIN
    DECLARE v_user_id INT DEFAULT NULL;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Call CreateUser procedure to get or create user
    CALL CreateUser(p_username, p_password, v_user_id);
    
    -- Insert or update balance
    INSERT INTO balances (user_id, balance) 
    VALUES (v_user_id, p_balance)
    ON DUPLICATE KEY UPDATE 
        balance = p_balance,
        updated_at = CURRENT_TIMESTAMP;
    
    COMMIT;
END//

DELIMITER ;
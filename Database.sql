create schema  Bank_Database;
use Bank_Database;


create table Clients ( 
    client_id int auto_increment primary key, 
    username varchar(50) unique,
    email varchar(100) not null unique, 
    phone_country_code varchar(5) not null,
    phone_number varchar(20) not null, 
    registered_at timestamp default current_timestamp(), 
    city varchar(50) not null,
    street varchar(50) not null,
    postal_code varchar(50) not null,
    password_hash varchar(255) not null,
    passkey_public_key varchar(255),    -- for fido passkey
    passcode_hash varchar(255) not null,
    mfa_secret varchar(255),
    mfa_active boolean default false, 
    is_locked boolean default false,
    lockout_expire timestamp default null,
    is_active boolean default true,
    is_admin boolean default false,
    unique (phone_number, phone_country_code)
);
select * from clients;

create table Clients_ids ( 
    client_id int, 
    id_number varchar(60) not null, 
    given_names varchar(200) not null,
    last_name varchar(50) not null,
    id_type varchar(50) not null,
    birthday date not null, 
    nationality varchar(50) not null,
    emission_country varchar(50) not null,
    issue_date date not null,
    expiration_date date not null,
    is_verified boolean default false,
    primary key (id_number, emission_country),
    foreign key (client_id) references Clients (client_id)
);


create table Accounts ( 
    account_id int auto_increment primary key, 
    iban varchar(50) not null unique,
    bic varchar(50) not null,
    currency char(3) not null default 'MZN',
    balance decimal (15,2) not null default 0.00,
    created_at timestamp not null default current_timestamp(),   
    is_active boolean default true
);

create table TransactionLimits (
    account_id int primary key,
    daily_limit decimal(10,2) default 100000,
    per_transaction_limit decimal (10,2) default 50000,
    foreign key (account_id) references Accounts(account_id)
);


-- junction table between clients and accounts
create table AccountsOwners ( 
    client_id integer not null,
    account_id integer not null,
    ownership_type enum ('primary', 'joint', 'beneficiary') not null,   
    primary key (client_id, account_id),
    foreign key (client_id) references Clients(client_id),
    foreign key (account_id) references Accounts(account_id)
);
   
create table MFA_BackupCodes ( 
    code_id int auto_increment primary key, 
    client_id int not null,
    changed_date timestamp default current_timestamp(), 
    code_hash varchar(255) not null, 
    used boolean default false,
    foreign key (client_id) references Clients (client_id)
);

create table AuthMethodHistory ( 
    history_id int auto_increment primary key, 
    client_id int not null, 
    type enum ('password', 'public_key', 'passcode', 'MFA_backupCode', 'MFA_secretKey'),
    changed_date timestamp default current_timestamp(), 
    authMethod_hash varchar(255) not null, 
    foreign key (client_id) references Clients (client_id)
);


create table PasswordResetTokens ( 
    token_id int auto_increment primary key, 
    client_id int not null,
    expires_at timestamp not null, 
    token_hash varchar(255) not null, 
    used boolean default false,
    foreign key (client_id) references Clients (client_id)
);


create table NotificationLog (
    notification_id int auto_increment primary key, 
    client_id int not null, 
    notification_type enum ('sms', 'email')not null,
    notification_purpose varchar (50) not null,
    status enum ('sent', 'failed', 'pending') not null,
    created_at timestamp default current_timestamp(),
    foreign key (client_id) references Clients (client_id)
);

-- status is updated 
create table Transactions ( 
    transaction_id int auto_increment primary key, 
    from_account int not null, 
    to_account int not null,
    amount decimal(15,2) not null check (amount > 0), 
    transaction_time timestamp default current_timestamp(), 
    status enum ('completed', 'failed', 'pending', 'processing') not null,
    reference text,
    mac_signature varchar(255) not null,
    foreign key (from_account) references Accounts (account_id),
    foreign key (to_account) references Accounts (account_id),
    check (from_account <> to_account)
);


-- permanent, insert whenever a new transaction is innititated by the user
create table TransactionsLog ( 
    transactionLog_id int auto_increment primary key,
    transaction_id int, 
    from_account int not null, 
    to_account int not null,
    amount decimal(15,2) not null check (amount > 0), 
    log_time timestamp default current_timestamp(), 
    status enum ('completed', 'failed', 'pending', 'processing') not null,
    reference text,
    mac_signature varchar(255) not null,
    foreign key (from_account) references Accounts (account_id),
    foreign key (to_account) references Accounts (account_id),
    foreign key (transaction_id) references Transactions (transaction_id)
    check (from_account <> to_account)
);


-- track active user sessions
CREATE TABLE UserSessions (
    session_id varchar(255) primary key,
    client_id int not null,
    session_token varchar(255) not null unique,
    ip_address varchar(45) not null,      
    user_agent text,        
    login_time timestamp default current_timestamp(),
    last_active timestamp default current_timestamp on update current_timestamp(),
    expires_at timestamp not null,
    is_active boolean default true,
    foreign key (client_id) references Clients(client_id)
);

-- in case mfa on, devices that are trusted only need password to login, others need mfa
CREATE TABLE TrustedDevices (
    device_id int auto_increment primary key,
    client_id int not null,
    device_fingerprint varchar(255) not null,
    user_agent text,                  
    ip_address varchar(45) not null,
    last_used timestamp default current_timestamp on update current_timestamp,
    is_trusted boolean default true,
    unique(client_id, device_fingerprint),
    foreign key (client_id) references Clients(client_id)
);

create table LoginAttempts (
    login_attempt_id int auto_increment primary key,
    client_id int not null,
    device_fingerprint varchar(255) not null,
    user_agent text,                  
    ip_address varchar(45) not null,
    location varchar(100),
    attempt_time timestamp  not null default current_timestamp(),
    outcome enum ('success', 'failed password', 'failed mfa', 'failed account locked') not null, 
    risk_score int not null,
    foreign key (client_id) references Clients(client_id)
);

-- before transfer
create table PasscodeAttempts (
    attempt_id int auto_increment primary key,
    client_id int not null,
    account_id int,
    attempt_time timestamp default current_timestamp(),
    outcome enum ('success', 'failed') not null, 
    ip_address varchar(45),
    location varchar(100),
    risk_score int not null,
    foreign key (client_id) references Clients(client_id)
);

create table FraudAlerts (
alert_nr int auto_increment primary key,
client_id int not null, 
cause enum ('login', 'passcode', 'transfer limit', 'suspicious transfer'),
level enum('low', 'medium', 'high', 'urgent'),
details varchar (255),
created_at timestamp default current_timestamp(),
foreign key (client_id) references Clients (client_id)
);

show tables;
-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- indexes for foreign keys
create index clientId_trustedDevices
on TrustedDevices (client_id);

create index accountId_accountOwners
on AccountsOwners (account_id);

create index clientId_accountOwners
on AccountsOwners (client_id);

create index clientId_clientIds
on Clients_ids (client_id);

create index clientId_userSessions
on UserSessions (client_id);

create index fromAccount_id_transactions
on Transactions (from_account);

create index toAccount_id_transactions
on Transactions (to_account);

create index clientId_notificationLog
on NotificationLog (client_id);

create index clientId_pswdResetTokens
on PasswordResetTokens (client_id);

create index clientId_authHistory
on AuthMethodHistory (client_id);

create index clientId_mfaBackupCode 
on MFA_BackupCodes (client_id);

create index idx_transactions_time 
on Transactions(transaction_time);

create index idx_usersessions_expires
on UserSessions(expires_at);

create index idx_transactions_between_accounts 
on Transactions(from_account, to_account);

create index clientid_loginattempts 
on LoginAttempts(client_id);

create index clientid_passcodeattempts 
on PasscodeAttempts(client_id);

create index clientid_fraudalerts
on FraudAlerts(client_id);

create index idx_loginattempts_time
on LoginAttempts(attempt_time);

create index idx_passcodeattempts_time
on PasscodeAttempts(attempt_time);

create index idx_usersessions_token
on UserSessions(session_token);

create index idx_accounts_iban
on Accounts(iban);

create index idx_clients_username
on Clients(username);

create index idx_clients_email 
on Clients(email);

-- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## TRIGGERS

create trigger log_transactions
after update on Transactions
for each row
begin
	if old.status <> new.status then 
	insert into TransactionsLog ( 
    transaction_id, 
    from_account, 
    to_account,
    amount, 
    log_time, 
    status,
    reference,
    mac_signature 
)
values(
    new. transaction_id, 
    new.from_account, 
    new.to_account,
    new.amount, 
    new.transaction_time, 
    new.status,
    new.reference,
    new.mac_signature
);
end if;
end $$
delimiter;


delimiter $$
create trigger no_negative_balance
before insert on Transactions
for each row
begin
	declare cur_balance decimal (15,2);
    select balance into cur_balance from Accounts where account_id = new.from_account;
if new.amount > cur_balance then 
	signal sqlstate '45000' set message_text = 'Insufficient funds';
end if;
end $$
delimiter;


SHOW TRIGGERS;





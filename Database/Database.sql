create schema  Bank_Cyber_Database;
use  Bank_Cyber_Database;


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
    passcode_hash varchar(255) not null,
    mfa_secret varchar(255),
    mfa_active boolean default false, 
    is_locked boolean default false,
    lockout_expire timestamp default null,
    is_active boolean default true,
    is_admin boolean default false,
    unique (phone_number, phone_country_code)
);


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
    auth_type enum ('password', 'MFA_backupCode', 'MFA_secretKey'),
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
    status enum ('completed', 'failed', 'pending') not null,
    reference text,
    mac_signature varchar(255) not null,
    nonce varchar(255) not null unique,
    foreign key (from_account) references Accounts (account_id),
    foreign key (to_account) references Accounts (account_id)
);


-- track active user sessions
create table UserSessions (
    session_id varchar(255) primary key,
    client_id int not null,
    session_token varchar(255) not null unique,
    ip_address varchar(45) not null,      
    -- user_agent text,        if i had developed web
    login_time timestamp default current_timestamp(),
    last_active timestamp default current_timestamp on update current_timestamp(),
    expires_at timestamp not null,
    is_active boolean default true,
    foreign key (client_id) references Clients(client_id)
);

-- in case mfa on, devices that are trusted only need password to login, others need mfa
create table TrustedDevices (
    device_id int auto_increment primary key,
    client_id int not null,
    device_fingerprint varchar(255) not null,
   --  user_agent text if i had developed web,                  
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
    -- user_agent text if i had developed web,                  
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
    foreign key (client_id) references Clients(client_id),
    foreign key (account_id) references Accounts(account_id)
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

------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- speeds up username login lookup
create index idx_clients_username on Clients(username);

-- speeds up email login / recovery lookup
create index idx_clients_email on Clients(email);

-- speeds up lookup of identity documents per client
create index idx_clients_ids_client on Clients_ids(client_id);

-- speeds up filtering expired documents
create index idx_clientsIds_expDate on Clients_ids(expiration_date);

-- speeds up account lookup by IBAN
create index idx_accounts_iban on Accounts(iban);

-- speeds up finding all accounts for a client
create index idx_accountsowners_client on AccountsOwners(client_id);

-- speeds up finding all owners of an account
create index idx_accountsowners_account on AccountsOwners(account_id);

-- speeds up client-account join queries
create index idx_accountsowners_client_account on AccountsOwners(client_id, account_id);

-- speeds up transaction sorting by time
create index idx_transactions_time on Transactions(transaction_time);

-- speeds up lookup of outgoing transfers
create index idx_transactions_from on Transactions(from_account);

-- speeds up lookup of incoming transfers
create index idx_transactions_to on Transactions(to_account);

-- speeds up transaction analytics per time and sender
create index idx_transactions_time_from on Transactions(transaction_time, from_account);

-- speeds up account limit lookup
create index idx_transactionlimits_account on TransactionLimits(account_id);

-- speeds up session lookup by client
create index idx_usersessions_client on UserSessions(client_id);

-- speeds up session validation by token
create index idx_usersessions_token on UserSessions(session_token);

-- speeds up session expiration checks
create index idx_usersessions_expires on UserSessions(expires_at);

-- speeds up login history lookup per user
create index idx_loginattempts_client on LoginAttempts(client_id);

-- speeds up login attempts ordered by time
create index idx_loginattempts_time on LoginAttempts(attempt_time);

-- speeds up fraud detection queries per user and time window
create index idx_loginattempts_client_time on LoginAttempts(client_id, attempt_time);

-- speeds up fraud analysis per user over time window
create index idx_loginattempts_risk_time on LoginAttempts(client_id, risk_score, attempt_time);

-- speeds up passcode attempt lookup per user
create index idx_passcodeattempts_client on PasscodeAttempts(client_id);

-- speeds up passcode attempts ordered by time
create index idx_passcodeattempts_time on PasscodeAttempts(attempt_time);

-- speeds up passcode fraud detection per user and time 
create index idx_passcodeattempts_client_time on PasscodeAttempts(client_id, attempt_time);

-- speeds up fraud alert lookup per user
create index idx_fraudalerts_client on FraudAlerts(client_id);

-- speeds up notification lookup per user
create index idx_notification_client on NotificationLog(client_id);

-- speeds up notification status/time filtering
create index idx_notification_status_time on NotificationLog(status, created_at);

-- speeds up MFA backup code lookup per user
create index idx_mfa_backup_client on MFA_BackupCodes(client_id);

-- speeds up auth history lookup per user
create index idx_authhistory_client on AuthMethodHistory(client_id);

-- speeds up password reset lookup per user
create index idx_passwordresettokens_client on PasswordResetTokens(client_id);

-- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------






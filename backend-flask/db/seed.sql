-- this file was manually created

INSERT INTO
    public.users (
        display_name,
        handle,
        email,
        cognito_user_id
    )
VALUES (
        'Andrew Brown',
        'andrewbrown',
        'andrew@brown.com',
        '5ae290ed-55d1-47a0-bc6d-fe2bc2700399'
    ), (
        'Andrew Bayko',
        'bayko',
        'ohary37.com',
        '5ae290ed-55d1-47a0-bc6d-fe2bc2700389'
    ), (
        'Hillary Ugwu',
        'ohahuru',
        'ohary37.com',
        'MOCK'
    );

INSERT INTO
    public.activities (user_uuid, message, expires_at)
VALUES ( (
            SELECT uuid
            from public.users
            WHERE
                users.handle = 'andrewbrown'
            LIMIT
                1
        ), 'This was imported as seed data!', current_timestamp + interval '10 day'
    )
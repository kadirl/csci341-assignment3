-- Insert sample data for all tables
-- At least 10 instances per table as required

-- Insert USERS (mix of caregivers and members)
INSERT INTO "user" (email, given_name, surname, city, phone_number, profile_description, password) VALUES
('arman.armanov@email.com', 'Arman', 'Armanov', 'Astana', '+77771234567', 'Experienced caregiver', 'password123'),
('amina.aminova@email.com', 'Amina', 'Aminova', 'Almaty', '+77772345678', 'Family member seeking care', 'password123'),
('david.davidov@email.com', 'David', 'Davidov', 'Astana', '+77773456789', 'Professional babysitter', 'password123'),
('elena.elenova@email.com', 'Elena', 'Elenova', 'Astana', '+77774567890', 'Looking for elderly care', 'password123'),
('farid.faridov@email.com', 'Farid', 'Faridov', 'Almaty', '+77775678901', 'Elderly care specialist', 'password123'),
('gulnara.gulnarova@email.com', 'Gulnara', 'Gulnarova', 'Astana', '+77776789012', 'Mother of two children', 'password123'),
('hasan.hasanov@email.com', 'Hasan', 'Hasanov', 'Shymkent', '+77777890123', 'Playmate for children', 'password123'),
('irina.irinova@email.com', 'Irina', 'Irinova', 'Astana', '+77778901234', 'Babysitter with 5 years experience', 'password123'),
('john.johnson@email.com', 'John', 'Johnson', 'Almaty', '+77779012345', 'Father seeking babysitter', 'password123'),
('kate.kateova@email.com', 'Kate', 'Kateova', 'Astana', '+77770123456', 'Elderly care professional', 'password123'),
('lisa.lisova@email.com', 'Lisa', 'Lisova', 'Astana', '+77771234560', 'Mother of 5-year-old son', 'password123'),
('michael.michaelov@email.com', 'Michael', 'Michaelov', 'Almaty', '+77772345601', 'Babysitter', 'password123'),
('nina.ninova@email.com', 'Nina', 'Ninova', 'Shymkent', '+77773456712', 'Family member', 'password123'),
('omar.omarov@email.com', 'Omar', 'Omarov', 'Astana', '+77774567823', 'Playmate specialist', 'password123'),
('paul.paulov@email.com', 'Paul', 'Paulov', 'Astana', '+77775678934', 'Seeking elderly care', 'password123'),
('qasim.qasimov@email.com', 'Qasim', 'Qasimov', 'Almaty', '+77776789045', 'Elderly care expert', 'password123'),
('rosa.rosova@email.com', 'Rosa', 'Rosova', 'Astana', '+77777890156', 'Babysitter', 'password123'),
('sam.samov@email.com', 'Sam', 'Samov', 'Shymkent', '+77778901267', 'Father of three', 'password123'),
('tina.tinova@email.com', 'Tina', 'Tinova', 'Astana', '+77779012378', 'Elderly care professional', 'password123'),
('umar.umarov@email.com', 'Umar', 'Umarov', 'Almaty', '+77770123489', 'Playmate for children', 'password123');

-- Insert CAREGIVERS (users 1, 3, 5, 7, 8, 10, 12, 14, 17, 19, 20)
INSERT INTO caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
(1, 'photo1.jpg', 'Male', 'babysitter', 8.50),
(3, 'photo3.jpg', 'Male', 'babysitter', 9.00),
(5, 'photo5.jpg', 'Male', 'elderly care', 12.00),
(7, 'photo7.jpg', 'Male', 'playmate for children', 7.50),
(8, 'photo8.jpg', 'Female', 'babysitter', 10.00),
(10, 'photo10.jpg', 'Female', 'elderly care', 11.50),
(12, 'photo12.jpg', 'Male', 'babysitter', 9.50),
(14, 'photo14.jpg', 'Male', 'playmate for children', 8.00),
(17, 'photo17.jpg', 'Female', 'babysitter', 10.50),
(19, 'photo19.jpg', 'Female', 'elderly care', 13.00),
(20, 'photo20.jpg', 'Male', 'playmate for children', 7.00);

-- Insert MEMBERS (users 2, 4, 6, 9, 11, 13, 15, 16, 18)
INSERT INTO member (member_user_id, house_rules, dependent_description) VALUES
(2, 'No pets. Please maintain hygiene.', 'Looking for babysitter for 3-year-old daughter'),
(4, 'No pets. Quiet environment required.', 'Elderly mother needs daily care, age 75'),
(6, 'No pets. Clean environment.', 'I have a 5-year-old son who likes painting'),
(9, 'Pets allowed. Respectful behavior.', 'Two children aged 4 and 6 need babysitting'),
(11, 'No pets. Strict hygiene rules.', '5-year-old son who likes painting and drawing'),
(13, 'No pets. Professional care required.', 'Elderly father, age 80, needs assistance'),
(15, 'No pets. Regular schedule.', 'Elderly grandmother, age 70, needs care'),
(16, 'No pets. Soft-spoken caregiver preferred.', 'Elderly parent needs gentle care'),
(18, 'Pets allowed. Flexible schedule.', 'Three children need playmate and supervision');

-- Insert ADDRESSES for all members
INSERT INTO address (member_user_id, house_number, street, town) VALUES
(2, '15', 'Kabanbay Batyr', 'Astana'),
(4, '22', 'Abay Avenue', 'Astana'),
(6, '33', 'Kabanbay Batyr', 'Astana'),
(9, '44', 'Al-Farabi Avenue', 'Almaty'),
(11, '55', 'Kabanbay Batyr', 'Astana'),
(13, '66', 'Tauelsizdik Avenue', 'Shymkent'),
(15, '77', 'Kabanbay Batyr', 'Astana'),
(16, '88', 'Abay Avenue', 'Astana'),
(18, '99', 'Al-Farabi Avenue', 'Almaty');

-- Insert JOBS
INSERT INTO job (member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(2, 'babysitter', 'Must be soft-spoken and patient', '2025-01-15'),
(4, 'elderly care', 'Experience with dementia patients preferred', '2025-01-16'),
(6, 'babysitter', 'Art background preferred, soft-spoken', '2025-01-17'),
(9, 'babysitter', 'Energetic and fun-loving', '2025-01-18'),
(11, 'playmate for children', 'Creative activities required', '2025-01-19'),
(13, 'elderly care', 'Medical training preferred', '2025-01-20'),
(15, 'elderly care', 'Gentle and caring personality', '2025-01-21'),
(16, 'elderly care', 'Soft-spoken caregiver needed', '2025-01-22'),
(18, 'playmate for children', 'Active and engaging', '2025-01-23'),
(2, 'babysitter', 'Weekend availability required', '2025-01-24'),
(4, 'elderly care', 'Morning shifts preferred', '2025-01-25'),
(6, 'babysitter', 'Afternoon availability', '2025-01-26'),
(9, 'playmate for children', 'Outdoor activities preferred', '2025-01-27'),
(11, 'babysitter', 'Educational activities', '2025-01-28'),
(13, 'elderly care', 'Evening care needed', '2025-01-29');

-- Insert JOB_APPLICATIONS
INSERT INTO job_application (caregiver_user_id, job_id, date_applied) VALUES
(1, 1, '2025-01-20'),
(3, 1, '2025-01-21'),
(8, 1, '2025-01-22'),
(1, 2, '2025-01-25'),
(5, 2, '2025-01-26'),
(10, 2, '2025-01-27'),
(19, 2, '2025-01-28'),
(1, 3, '2025-01-30'),
(8, 3, '2025-01-31'),
(12, 3, '2025-02-01'),
(17, 3, '2025-02-02'),
(7, 5, '2025-02-03'),
(14, 5, '2025-02-04'),
(20, 5, '2025-02-05'),
(5, 6, '2025-02-06'),
(10, 6, '2025-02-07'),
(19, 6, '2025-02-08'),
(5, 7, '2025-02-09'),
(10, 7, '2025-02-10'),
(19, 7, '2025-02-11'),
(5, 8, '2025-02-12'),
(10, 8, '2025-02-13'),
(19, 8, '2025-02-14'),
(7, 9, '2025-02-15'),
(14, 9, '2025-02-16'),
(20, 9, '2025-02-17');

-- Insert APPOINTMENTS
INSERT INTO appointment (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(1, 2, '2025-02-10', '09:00:00', 3.0, 'accepted'),
(3, 6, '2025-02-11', '14:00:00', 4.0, 'accepted'),
(5, 4, '2025-02-12', '10:00:00', 5.0, 'accepted'),
(8, 9, '2025-02-13', '15:00:00', 3.5, 'accepted'),
(10, 13, '2025-02-14', '08:00:00', 6.0, 'accepted'),
(12, 11, '2025-02-15', '16:00:00', 2.5, 'accepted'),
(17, 18, '2025-02-16', '11:00:00', 4.0, 'accepted'),
(19, 15, '2025-02-17', '09:30:00', 5.5, 'accepted'),
(1, 6, '2025-02-18', '13:00:00', 3.0, 'accepted'),
(5, 16, '2025-02-19', '10:00:00', 4.0, 'accepted'),
(8, 2, '2025-02-20', '14:00:00', 3.0, 'pending'),
(10, 4, '2025-02-21', '11:00:00', 4.0, 'pending'),
(3, 9, '2025-02-22', '15:00:00', 2.0, 'declined'),
(7, 11, '2025-02-23', '16:00:00', 3.0, 'pending'),
(14, 18, '2025-02-24', '12:00:00', 4.0, 'declined');


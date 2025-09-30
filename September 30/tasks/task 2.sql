CREATE DATABASE HospitalManagement;

USE HospitalManagement;

-- Create Patients table
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    gender CHAR(1),
    city VARCHAR(50)
);

-- Create Doctors table
CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(50),
    specialization VARCHAR(50),
    experience INT
);

-- Create Appointments table
CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

-- Create MedicalRecords table
CREATE TABLE MedicalRecords (
    record_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    diagnosis VARCHAR(100),
    treatment VARCHAR(100),
    date DATE,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
);

-- Create Billing table
CREATE TABLE Billing (
    bill_id INT PRIMARY KEY,
    patient_id INT,
    amount DECIMAL(10,2),
    bill_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);

-- Insert 10 Patients from different Indian cities
INSERT INTO Patients (patient_id, name, age, gender, city) VALUES
(1, 'Amit Sharma', 30, 'M', 'Delhi'),
(2, 'Neha Singh', 25, 'F', 'Mumbai'),
(3, 'Raj Patel', 40, 'M', 'Ahmedabad'),
(4, 'Sonal Gupta', 35, 'F', 'Bangalore'),
(5, 'Vikram Joshi', 28, 'M', 'Chennai'),
(6, 'Pooja Rao', 22, 'F', 'Hyderabad'),
(7, 'Karan Mehta', 50, 'M', 'Kolkata'),
(8, 'Anjali Verma', 45, 'F', 'Pune'),
(9, 'Ravi Kumar', 38, 'M', 'Lucknow'),
(10, 'Suman Das', 33, 'F', 'Jaipur');

-- Insert 5 Doctors with various specializations
INSERT INTO Doctors (doctor_id, name, specialization, experience) VALUES
(1, 'Dr. A. Kumar', 'Cardiology', 15),
(2, 'Dr. B. Singh', 'Orthopedics', 12),
(3, 'Dr. C. Iyer', 'Pediatrics', 10),
(4, 'Dr. D. Das', 'Neurology', 20),
(5, 'Dr. E. Roy', 'General Medicine', 8);

-- Insert Appointments across multiple dates
INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_date, status) VALUES
(1, 1, 1, '2025-10-01', 'Completed'),
(2, 2, 3, '2025-10-05', 'Scheduled'),
(3, 3, 2, '2025-09-28', 'Completed'),
(4, 4, 1, '2025-10-10', 'Cancelled'),
(5, 5, 5, '2025-10-03', 'Completed'),
(6, 6, 4, '2025-09-29', 'Scheduled'),
(7, 7, 1, '2025-10-02', 'Completed'),
(8, 8, 2, '2025-10-07', 'Scheduled'),
(9, 9, 3, '2025-10-01', 'Completed'),
(10, 10, 5, '2025-10-04', 'Completed');

-- Insert Medical Records with diagnosis and treatments
INSERT INTO MedicalRecords (record_id, patient_id, doctor_id, diagnosis, treatment, date) VALUES
(1, 1, 1, 'Hypertension', 'Medication A', '2025-10-01'),
(2, 3, 2, 'Fracture', 'Cast and Rest', '2025-09-28'),
(3, 5, 5, 'Fever', 'Paracetamol', '2025-10-03'),
(4, 7, 1, 'Arrhythmia', 'Medication B', '2025-10-02'),
(5, 9, 3, 'Cold', 'Rest and Fluids', '2025-10-01');

-- Insert Bills with paid/unpaid status
INSERT INTO Billing (bill_id, patient_id, amount, bill_date, status) VALUES
(1, 1, 1500.00, '2025-10-02', 'Paid'),
(2, 3, 5000.00, '2025-09-29', 'Unpaid'),
(3, 5, 700.00, '2025-10-04', 'Paid'),
(4, 7, 2000.00, '2025-10-03', 'Unpaid'),
(5, 9, 300.00, '2025-10-02', 'Paid');

SELECT DISTINCT p.patient_id, p.name, p.age, p.gender, p.city
FROM Patients p
JOIN Appointments a ON p.patient_id = a.patient_id
JOIN Doctors d ON a.doctor_id = d.doctor_id
WHERE d.specialization = 'Cardiology';

SELECT appointment_id, patient_id, appointment_date, status
FROM Appointments
WHERE doctor_id = 1;

-- Show unpaid bills of patients
SELECT b.bill_id, p.name AS patient_name, b.amount, b.bill_date, b.status
FROM Billing b
JOIN Patients p ON b.patient_id = p.patient_id
WHERE b.status = 'Unpaid';

-- GetPatientHistory(patient_id) → returns all visits, diagnoses, and treatments for a patient.
DELIMITER $$
CREATE PROCEDURE GetPatientHistory(IN pid INT)
BEGIN
    SELECT mr.date, d.name AS doctor_name, mr.diagnosis, mr.treatment
    FROM MedicalRecords mr
    JOIN Doctors d ON mr.doctor_id = d.doctor_id
    WHERE mr.patient_id = pid
    ORDER BY mr.date DESC;
END$$
DELIMITER ;

call GetPatientHistory(3);

DELIMITER $$
CREATE PROCEDURE GetDoctorAppointments(IN did INT)
BEGIN
    SELECT appointment_id, patient_id, appointment_date, status
    FROM Appointments
    WHERE doctor_id = did
    ORDER BY appointment_date DESC;
END$$
DELIMITER ;
call GetDoctorAppointments(2);

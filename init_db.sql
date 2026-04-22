-- Table services
CREATE TABLE IF NOT EXISTS services (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    nb_lits INT NOT NULL,
    responsable VARCHAR(100)
);

-- Table medecins
CREATE TABLE IF NOT EXISTS medecins (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    specialite VARCHAR(100),
    service_id INT REFERENCES services(id)
);

-- Table patients
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    date_naissance DATE NOT NULL,
    sexe CHAR(1) CHECK (sexe IN ('M', 'F')),
    adresse TEXT
);

-- Table sejours
CREATE TABLE IF NOT EXISTS sejours (
    id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(id),
    service_id INT REFERENCES services(id),
    medecin_id INT REFERENCES medecins(id),
    date_entree DATE NOT NULL,
    date_sortie DATE,
    cout_sejour NUMERIC(10,2),
    statut VARCHAR(20) DEFAULT 'en_cours' CHECK (statut IN ('en_cours', 'termine', 'urgent'))
);

-- Table diagnostics
CREATE TABLE IF NOT EXISTS diagnostics (
    id SERIAL PRIMARY KEY,
    sejour_id INT REFERENCES sejours(id),
    code_cim VARCHAR(10),
    libelle VARCHAR(200) NOT NULL,
    gravite INT CHECK (gravite BETWEEN 1 AND 5),
    date_pose DATE NOT NULL
);

-- Insertion des services
INSERT INTO services (nom, nb_lits, responsable) VALUES
('Cardiologie', 30, 'Dr. Bernard'),
('Neurologie', 25, 'Dr. Moreau'),
('Urgences', 40, 'Dr. Lefevre'),
('Pediatrie', 20, 'Dr. Simon'),
('Chirurgie', 35, 'Dr. Dupont');

-- Insertion des medecins
INSERT INTO medecins (nom, prenom, specialite, service_id) VALUES
('Bernard', 'Claire', 'Cardiologie', 1),
('Moreau', 'Pierre', 'Neurologie', 2),
('Lefevre', 'Sophie', 'Medecine urgence', 3),
('Simon', 'Marc', 'Pediatrie', 4),
('Dupont', 'Anne', 'Chirurgie', 5),
('Martin', 'Louis', 'Cardiologie', 1),
('Petit', 'Julie', 'Neurologie', 2);

-- Insertion des patients (25 patients attendus)
INSERT INTO patients (nom, prenom, date_naissance, sexe, adresse) VALUES
('Durand', 'Jean', '1955-03-12', 'M', '12 rue de la Paix, Paris'),
('Leroy', 'Marie', '1978-07-25', 'F', '5 avenue Victor Hugo, Lyon'),
('Morel', 'Paul', '1942-11-08', 'M', '8 boulevard Voltaire, Marseille'),
('Garcia', 'Sophie', '1990-01-30', 'F', '3 rue Gambetta, Toulouse'),
('Martinez', 'Antoine', '1965-09-14', 'M', '21 rue du Commerce, Bordeaux'),
('Robert', 'Helene', '1983-05-22', 'F', '14 impasse des Lilas, Nantes'),
('Bernard', 'Pierre', '1950-12-03', 'M', '7 chemin des Roses, Strasbourg'),
('Thomas', 'Julie', '2001-08-18', 'F', '2 rue Nationale, Lille'),
('Petit', 'Michel', '1938-04-27', 'M', '33 avenue de la Republique, Nice'),
('Roux', 'Isabelle', '1972-10-15', 'F', '9 place du Marche, Rennes'),
('Simon', 'Francois', '1988-02-09', 'M', '18 rue de la Gare, Reims'),
('Laurent', 'Claire', '1960-06-30', 'F', '6 rue Saint-Pierre, Grenoble'),
('Michel', 'Eric', '1995-11-21', 'M', '11 rue des Fleurs, Toulon'),
('Lefevre', 'Nathalie', '1947-08-05', 'F', '25 avenue du General, Angers'),
('Adam', 'Thomas', '2010-03-17', 'M', '4 rue de l Eglise, Le Mans'),
('Bonnet', 'Valerie', '1975-07-11', 'F', '16 rue du Moulin, Aix-en-Provence'),
('Fontaine', 'Jacques', '1932-09-28', 'M', '30 boulevard du Temple, Brest'),
('Chevalier', 'Sandrine', '1992-04-04', 'F', '13 place de la Mairie, Perpignan'),
('Rousseau', 'Luc', '1968-12-19', 'M', '22 rue Victor Hugo, Amiens'),
('Vincent', 'Patricia', '1980-01-07', 'F', '8 impasse du Chateau, Limoges'),
('Fournier', 'Remi', '2005-06-23', 'M', '1 rue de la Fontaine, Clermont-Ferrand'),
('Girard', 'Christine', '1955-10-31', 'F', '19 avenue de la Victoire, Metz'),
('Mercier', 'Alain', '1943-03-08', 'M', '27 rue du Faubourg, Nancy'),
('Dupuis', 'Laure', '1998-09-16', 'F', '5 chemin des Vignes, Tours'),
('Blanc', 'Georges', '1970-02-14', 'M', '10 rue de la Republique, Dijon');

-- Insertion des sejours
INSERT INTO sejours (patient_id, service_id, medecin_id, date_entree, date_sortie, cout_sejour, statut) VALUES
(1, 1, 1, '2024-10-01', '2024-10-08', 3200.00, 'termine'),
(2, 2, 2, '2024-10-03', '2024-10-10', 2800.00, 'termine'),
(3, 1, 6, '2024-10-05', NULL, 4100.00, 'en_cours'),
(4, 3, 3, '2024-10-07', '2024-10-08', 950.00, 'termine'),
(5, 5, 5, '2024-10-08', '2024-10-15', 5600.00, 'termine'),
(6, 4, 4, '2024-10-09', '2024-10-14', 1800.00, 'termine'),
(7, 1, 1, '2024-10-10', NULL, 2900.00, 'urgent'),
(8, 4, 4, '2024-10-11', '2024-10-15', 1600.00, 'termine'),
(9, 2, 7, '2024-10-12', NULL, 3700.00, 'en_cours'),
(10, 5, 5, '2024-10-13', '2024-10-20', 6200.00, 'termine'),
(11, 3, 3, '2024-10-14', '2024-10-15', 880.00, 'termine'),
(12, 1, 6, '2024-10-15', NULL, 4500.00, 'urgent'),
(13, 3, 3, '2024-10-16', '2024-10-17', 1100.00, 'termine'),
(14, 2, 2, '2024-10-17', '2024-10-24', 3100.00, 'termine'),
(15, 4, 4, '2024-10-18', '2024-10-21', 1400.00, 'termine'),
(16, 5, 5, '2024-10-19', NULL, 5900.00, 'en_cours'),
(17, 1, 1, '2024-10-20', '2024-10-27', 3600.00, 'termine'),
(18, 3, 3, '2024-10-21', '2024-10-22', 790.00, 'termine'),
(19, 2, 7, '2024-10-22', NULL, 2600.00, 'en_cours'),
(20, 5, 5, '2024-10-23', '2024-10-30', 7100.00, 'termine'),
(21, 4, 4, '2024-10-24', '2024-10-28', 1700.00, 'termine'),
(22, 1, 6, '2024-10-25', NULL, 3300.00, 'urgent'),
(23, 2, 2, '2024-10-26', '2024-11-02', 2900.00, 'termine'),
(24, 3, 3, '2024-10-27', '2024-10-28', 830.00, 'termine'),
(25, 5, 5, '2024-10-28', NULL, 6800.00, 'en_cours');

-- Insertion des diagnostics
INSERT INTO diagnostics (sejour_id, code_cim, libelle, gravite, date_pose) VALUES
(1, 'I21.0', 'Infarctus aigu du myocarde', 5, '2024-10-01'),
(2, 'G35', 'Sclerose en plaques', 3, '2024-10-03'),
(3, 'I50.0', 'Insuffisance cardiaque congestive', 4, '2024-10-05'),
(4, 'S06.0', 'Commotion cerebrale', 2, '2024-10-07'),
(5, 'K40.0', 'Hernie inguinale bilaterale', 2, '2024-10-08'),
(6, 'J18.9', 'Pneumonie non precisee', 3, '2024-10-09'),
(7, 'I63.5', 'Infarctus cerebral par occlusion', 5, '2024-10-10'),
(8, 'A09', 'Gastroenterite infectieuse', 1, '2024-10-11'),
(9, 'G40.0', 'Epilepsie partielle idiopathique', 3, '2024-10-12'),
(10, 'M16.0', 'Coxarthrose primitive bilateral', 2, '2024-10-13'),
(11, 'R07.4', 'Douleur thoracique non specifique', 2, '2024-10-14'),
(12, 'I48', 'Fibrillation et flutter auriculaire', 4, '2024-10-15'),
(13, 'T14.1', 'Plaie de region du corps non precisee', 1, '2024-10-16'),
(14, 'G43.0', 'Migraine sans aura', 2, '2024-10-17'),
(15, 'J06.9', 'Infection aigue des voies respiratoires', 1, '2024-10-18'),
(16, 'C34.1', 'Neoplasme malin du lobe superieur', 5, '2024-10-19'),
(17, 'I10', 'Hypertension essentielle primaire', 3, '2024-10-20'),
(18, 'S52.0', 'Fracture de l olecraner', 2, '2024-10-21'),
(19, 'G61.0', 'Syndrome de Guillain-Barre', 4, '2024-10-22'),
(20, 'K57.3', 'Diverticulose du colon sans peritonite', 3, '2024-10-23'),
(21, 'L03.0', 'Cellulite des doigts et des orteils', 1, '2024-10-24'),
(22, 'I21.4', 'Infarctus du myocarde sous-endocardique', 5, '2024-10-25'),
(23, 'G20', 'Maladie de Parkinson', 3, '2024-10-26'),
(24, 'R55', 'Syncope et collapsus', 2, '2024-10-27'),
(25, 'K80.0', 'Calculs de la vesicule biliaire', 3, '2024-10-28');

-- Desactivation du Row Level Security
ALTER TABLE services DISABLE ROW LEVEL SECURITY;
ALTER TABLE medecins DISABLE ROW LEVEL SECURITY;
ALTER TABLE patients DISABLE ROW LEVEL SECURITY;
ALTER TABLE sejours DISABLE ROW LEVEL SECURITY;
ALTER TABLE diagnostics DISABLE ROW LEVEL SECURITY;

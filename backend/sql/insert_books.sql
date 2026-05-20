-- ============================================================
-- BiblioSmart — Book catalog seed (60 books)
-- Run: mysql -u admin -pproiectbiblioteca26 biblioteca < insert_books.sql
-- ============================================================

USE biblioteca;

INSERT INTO carti (titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen, pozitie, cod) VALUES

-- ── BIOLOGIE ────────────────────────────────────────────────
('Biologie - Manual clasa a IX-a',    'Gheorghe Mohan, Aurel Ardelean',      '9786060010011', 3, 3, 0, 'Manual Biologie',   'Raft A1', 'BIO-09'),
('Biologie - Manual clasa a X-a',     'Silvia Olteanu, Tatiana Coprean',     '9786060010028', 3, 3, 0, 'Manual Biologie',   'Raft A1', 'BIO-10'),
('Biologie - Manual clasa a XI-a',    'Gheorghe Mohan, Aurel Ardelean',      '9786060010035', 3, 3, 0, 'Manual Biologie',   'Raft A1', 'BIO-11'),
('Biologie - Manual clasa a XII-a',   'Gheorghe Mohan, Aurel Ardelean',      '9786060010042', 3, 3, 0, 'Manual Biologie',   'Raft A1', 'BIO-12'),

-- ── CHIMIE ──────────────────────────────────────────────────
('Chimie - Manual clasa a IX-a',      'Luminița Vlădescu, Irinel Badea',     '9786060010059', 3, 3, 0, 'Manual Chimie',     'Raft A2', 'CHI-09'),
('Chimie - Manual clasa a X-a',       'Luminița Vlădescu, C. Tăbărașc',     '9786060010066', 3, 3, 0, 'Manual Chimie',     'Raft A2', 'CHI-10'),
('Chimie - Manual clasa a XI-a',      'Luminița Vlădescu, Irinel Badea',     '9786060010073', 3, 3, 0, 'Manual Chimie',     'Raft A2', 'CHI-11'),
('Chimie - Manual clasa a XII-a',     'Luminița Vlădescu, C. Tăbărașc',     '9786060010080', 3, 3, 0, 'Manual Chimie',     'Raft A2', 'CHI-12'),

-- ── FIZICĂ ──────────────────────────────────────────────────
('Fizică - Manual clasa a IX-a',      'Mihai Popescu, Delia Davidescu',      '9786060010097', 3, 3, 0, 'Manual Fizică',     'Raft A3', 'FIZ-09'),
('Fizică - Manual clasa a X-a',       'Mihai Popescu, Delia Davidescu',      '9786060010103', 3, 3, 0, 'Manual Fizică',     'Raft A3', 'FIZ-10'),
('Fizică - Manual clasa a XI-a',      'Rodica Ionescu, Florin Macesanu',     '9786060010110', 3, 3, 0, 'Manual Fizică',     'Raft A3', 'FIZ-11'),
('Fizică - Manual clasa a XII-a',     'Rodica Ionescu, Florin Macesanu',     '9786060010127', 3, 3, 0, 'Manual Fizică',     'Raft A3', 'FIZ-12'),

-- ── MATEMATICĂ ──────────────────────────────────────────────
('Matematică - Manual clasa a IX-a',  'Marius Burtea, Georgeta Burtea',      '9786060010134', 3, 3, 0, 'Manual Matematică', 'Raft A4', 'MAT-09'),
('Matematică - Manual clasa a X-a',   'Marius Burtea, Georgeta Burtea',      '9786060010141', 3, 3, 0, 'Manual Matematică', 'Raft A4', 'MAT-10'),
('Matematică - Manual clasa a XI-a',  'Marius Burtea, Georgeta Burtea',      '9786060010158', 3, 3, 0, 'Manual Matematică', 'Raft A4', 'MAT-11'),
('Matematică - Manual clasa a XII-a', 'Marius Burtea, Georgeta Burtea',      '9786060010165', 3, 3, 0, 'Manual Matematică', 'Raft A4', 'MAT-12'),

-- ── MARII CLASICI ───────────────────────────────────────────
('Poezii',                            'Mihai Eminescu',                      '9786060020011', 4, 4, 0, 'Poezie',            'Raft B1', 'LIT-001'),
('Luceafărul și alte poezii',         'Mihai Eminescu',                      '9786060020028', 3, 3, 0, 'Poezie',            'Raft B1', 'LIT-002'),
('Amintiri din copilărie',            'Ion Creangă',                         '9786060020035', 4, 4, 0, 'Proză',             'Raft B1', 'LIT-003'),
('Povești',                           'Ion Creangă',                         '9786060020042', 3, 3, 0, 'Proză',             'Raft B1', 'LIT-004'),
('Harap-Alb',                         'Ion Creangă',                         '9786060020059', 3, 3, 0, 'Proză',             'Raft B1', 'LIT-005'),
('Moara cu noroc',                    'Ioan Slavici',                        '9786060020066', 4, 4, 0, 'Nuvele',            'Raft B1', 'LIT-006'),
('Mara',                              'Ioan Slavici',                        '9786060020073', 3, 3, 0, 'Roman',             'Raft B1', 'LIT-007'),
('Nuvele',                            'Ioan Slavici',                        '9786060020080', 3, 3, 0, 'Nuvele',            'Raft B1', 'LIT-008'),
('O scrisoare pierdută',              'Ion Luca Caragiale',                  '9786060020097', 4, 4, 0, 'Dramaturgie',       'Raft B2', 'LIT-009'),
('Momente și schițe',                 'Ion Luca Caragiale',                  '9786060020103', 4, 4, 0, 'Proză',             'Raft B2', 'LIT-010'),
('O noapte furtunoasă',               'Ion Luca Caragiale',                  '9786060020110', 3, 3, 0, 'Dramaturgie',       'Raft B2', 'LIT-011'),
('Poezii populare ale românilor',     'Vasile Alecsandri',                   '9786060020127', 3, 3, 0, 'Poezie',            'Raft B2', 'LIT-012'),
('Alexandru Lăpușneanul',             'Costache Negruzzi',                   '9786060020134', 3, 3, 0, 'Nuvele',            'Raft B2', 'LIT-013'),
('Ciocoii vechi și noi',              'Nicolae Filimon',                     '9786060020141', 3, 3, 0, 'Roman',             'Raft B2', 'LIT-014'),
('Pseudokinegetikos',                 'Alexandru Odobescu',                  '9786060020158', 2, 2, 0, 'Proză',             'Raft B2', 'LIT-015'),

-- ── INTERBELIC ──────────────────────────────────────────────
('Ion',                               'Liviu Rebreanu',                      '9786060030011', 4, 4, 0, 'Roman',             'Raft B3', 'LIT-016'),
('Pădurea spânzuraților',             'Liviu Rebreanu',                      '9786060030028', 3, 3, 0, 'Roman',             'Raft B3', 'LIT-017'),
('Ciuleandra',                        'Liviu Rebreanu',                      '9786060030035', 3, 3, 0, 'Roman',             'Raft B3', 'LIT-018'),
('Răscoala',                          'Liviu Rebreanu',                      '9786060030042', 3, 3, 0, 'Roman',             'Raft B3', 'LIT-019'),
('Baltagul',                          'Mihail Sadoveanu',                    '9786060030059', 4, 4, 0, 'Roman',             'Raft B3', 'LIT-020'),
('Hanu Ancuței',                      'Mihail Sadoveanu',                    '9786060030066', 3, 3, 0, 'Proză',             'Raft B3', 'LIT-021'),
('Neamul Șoimăreștilor',              'Mihail Sadoveanu',                    '9786060030073', 3, 3, 0, 'Roman',             'Raft B3', 'LIT-022'),
('Frații Jderi',                      'Mihail Sadoveanu',                    '9786060030080', 2, 2, 0, 'Roman',             'Raft B3', 'LIT-023'),
('Ultima noapte de dragoste',         'Camil Petrescu',                      '9786060030097', 4, 4, 0, 'Roman',             'Raft B4', 'LIT-024'),
('Patul lui Procust',                 'Camil Petrescu',                      '9786060030103', 3, 3, 0, 'Roman',             'Raft B4', 'LIT-025'),
('Enigma Otiliei',                    'George Călinescu',                    '9786060030110', 4, 4, 0, 'Roman',             'Raft B4', 'LIT-026'),
('Bietul Ioanide',                    'George Călinescu',                    '9786060030127', 2, 2, 0, 'Roman',             'Raft B4', 'LIT-027'),
('Cuvinte potrivite',                 'Tudor Arghezi',                       '9786060030134', 3, 3, 0, 'Poezie',            'Raft B4', 'LIT-028'),
('Flori de mucigai',                  'Tudor Arghezi',                       '9786060030141', 3, 3, 0, 'Poezie',            'Raft B4', 'LIT-029'),
('Poemele luminii',                   'Lucian Blaga',                        '9786060030158', 3, 3, 0, 'Poezie',            'Raft C1', 'LIT-030'),
('Meșterul Manole',                   'Lucian Blaga',                        '9786060030165', 2, 2, 0, 'Dramaturgie',       'Raft C1', 'LIT-031'),
('Joc secund',                        'Ion Barbu',                           '9786060030172', 2, 2, 0, 'Poezie',            'Raft C1', 'LIT-032'),
('Concert din muzică de Bach',        'Hortensia Papadat-Bengescu',          '9786060030189', 2, 2, 0, 'Roman',             'Raft C1', 'LIT-033'),
('La Medeleni',                       'Ionel Teodoreanu',                    '9786060030196', 3, 3, 0, 'Roman',             'Raft C1', 'LIT-034'),
('Craii de Curtea-Veche',             'Mateiu Caragiale',                    '9786060030202', 2, 2, 0, 'Roman',             'Raft C1', 'LIT-035'),
('Rusoaica',                          'Gib Mihăescu',                        '9786060030219', 2, 2, 0, 'Roman',             'Raft C1', 'LIT-036'),
('Adela',                             'Garabet Ibrăileanu',                  '9786060030226', 2, 2, 0, 'Roman',             'Raft C2', 'LIT-037'),
('Plumb',                             'George Bacovia',                      '9786060030233', 3, 3, 0, 'Poezie',            'Raft C2', 'LIT-038'),
('Scântei galbene',                   'George Bacovia',                      '9786060030240', 2, 2, 0, 'Poezie',            'Raft C2', 'LIT-039'),
('Romanțe pentru mai târziu',         'Ion Minulescu',                       '9786060030257', 2, 2, 0, 'Poezie',            'Raft C2', 'LIT-040'),

-- ── POSTBELIC / PROGRAM ȘCOLAR ──────────────────────────────
('Moromeții',                         'Marin Preda',                         '9786060040011', 4, 4, 0, 'Roman',             'Raft C2', 'LIT-041'),
('Cel mai iubit dintre pământeni',    'Marin Preda',                         '9786060040028', 3, 3, 0, 'Roman',             'Raft C2', 'LIT-042'),
('Iona',                              'Marin Sorescu',                       '9786060040035', 2, 2, 0, 'Dramaturgie',       'Raft C3', 'LIT-043'),
('Liliecii',                          'Marin Sorescu',                       '9786060040042', 2, 2, 0, 'Poezie',            'Raft C3', 'LIT-044'),
('Necuvintele',                       'Nichita Stănescu',                    '9786060040059', 3, 3, 0, 'Poezie',            'Raft C3', 'LIT-045'),
('Laus Ptolemaei',                    'Nichita Stănescu',                    '9786060040066', 2, 2, 0, 'Poezie',            'Raft C3', 'LIT-046'),
('Groapa',                            'Eugen Barbu',                         '9786060040073', 2, 2, 0, 'Roman',             'Raft C3', 'LIT-047'),
('Nuntă în cer',                      'Mircea Eliade',                       '9786060040080', 2, 2, 0, 'Roman',             'Raft C3', 'LIT-048'),
('Maitreyi',                          'Mircea Eliade',                       '9786060040097', 3, 3, 0, 'Roman',             'Raft C3', 'LIT-049'),
('Orbitor',                           'Mircea Cărtărescu',                   '9786060040103', 2, 2, 0, 'Roman',             'Raft C3', 'LIT-050');

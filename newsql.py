import os

db_name = 'EmployeesFromGithub.db'
if not os.path.exists(db_name):
    open(db_name, 'w').close()

import sqlite3

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create the tables
cursor.execute("""
CREATE TABLE dept (
   DEPTNO INTEGER NOT NULL PRIMARY KEY,
   DNAME VARCHAR(20) NOT NULL,
   LOC VARCHAR(20) NOT NULL
);
""")

# Insert data into the 'dept' table
cursor.executemany("""
INSERT INTO dept (DEPTNO, DNAME, LOC) VALUES (?, ?, ?);
""", [
    (10, 'ACCOUNTING', 'NEW YORK'),
    (20, 'RESEARCH', 'DALLAS'),
    (30, 'SALES', 'CHICAGO'),
    (40, 'OPERATIONS', 'BOSTON')
])

# Create the 'emp' table
cursor.execute("""
CREATE TABLE emp (
   EMPNO INTEGER NOT NULL PRIMARY KEY,
   ENAME VARCHAR(20) NOT NULL,
   JOB VARCHAR(20) NOT NULL,
   MGR INTEGER,
   HIREDATE DATE NOT NULL,
   SAL INTEGER NOT NULL,
   COMM INTEGER,
   DEPTNO INTEGER NOT NULL,
   FOREIGN KEY (MGR) REFERENCES emp (EMPNO) ON DELETE SET NULL ON UPDATE CASCADE,
   FOREIGN KEY (DEPTNO) REFERENCES dept (DEPTNO) ON DELETE RESTRICT
);
""")

# Insert data into the 'emp' table
cursor.executemany("""
INSERT INTO emp (EMPNO, ENAME, JOB, MGR, HIREDATE, SAL, COMM, DEPTNO) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", [
        (7839, 'KING', 'PRESIDENT', None, '1981-11-17', 5000, None, 10),
        (7698, 'BLAKE', 'MANAGER', 7839, '1981-05-01', 2850, None, 30),
        (7654, 'MARTIN', 'SALESMAN', 7698, '1981-09-28', 1250, 1400, 30),
        (7782, 'CLARK', 'MANAGER', 7839, '1981-06-09', 2450, None, 10),
        (7566, 'JONES', 'MANAGER', 7839, '1981-04-02', 2975, None, 20),
        (7788, 'SCOTT', 'ANALYST', 7566, '1982-12-09', 3000, None, 20),
        (7902, 'FORD', 'ANALYST', 7566, '1981-12-03', 3000, None, 20),
        (7499, 'ALLEN', 'SALESMAN', 7698, '1981-02-20', 1600, 300, 30),
        (7521, 'WARD', 'SALESMAN', 7698, '1981-02-22', 1250, 500, 30),
        (7844, 'TURNER', 'SALESMAN', 7698, '1981-09-08', 1500, 0, 30),
        (7876, 'ADAMS', 'CLERK', 7788, '1983-01-12', 1100, None, 20),
        (7900, 'JAMES', 'CLERK', 7698, '1981-12-03', 950, None, 30),
        (7934, 'MILLER', 'CLERK', 7782, '1982-01-23', 1300, None, 10)
    ])

# Create the 'proj' table
cursor.execute("""
CREATE TABLE proj (
   PROJID INTEGER NOT NULL PRIMARY KEY,
   EMPNO INTEGER NOT NULL,
   STARTDATE DATE NOT NULL,
   ENDDATE DATE NOT NULL,
   FOREIGN KEY (EMPNO) REFERENCES emp (EMPNO) ON DELETE NO ACTION ON UPDATE CASCADE
);
""")

# Insert data into the 'proj' table
cursor.executemany("""
INSERT INTO proj (PROJID, EMPNO, STARTDATE, ENDDATE) VALUES (?, ?, ?, ?);
""", [
    (1, 7782, '2005-06-16', '2005-06-18'),
    (4, 7782, '2005-06-19', '2005-06-24'),
    (2, 7698, '2005-07-01', '2005-07-15'),
    (3, 7788, '2005-08-01', '2005-08-15'),
    (5, 7844, '2005-09-01', '2005-09-15')
    # Add other project records
])

conn.commit()
conn.close()
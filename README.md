# MethodsDBCH
Automation of the selection of methods for solving mathematical problems, problems of cryptography, cosmology, digital signal processing.

The MethodsDBCH software package can be used by specialists interested in selecting a modular arithmetic method for data processing in large computational ranges. When selecting, the conditions of the theoretical or practical problem being solved are taken into account. Users-specialists in the field of large computational ranges can add to or change information about the methods included in the registry.
## Functionality
- Сollection and processing of information about methods of computation in large computer ranges, namely:
  - algorithm class;
  - computational complexity class;
  - area of tasks to be solved (mathematical problems);
  - area of practical application (practical tasks);
  - related theorems;
  - work restrictions;
  - number of execution stages;
  - the amount of occupied internal and external memory;
  - computational complexity value (O- and L-notations).
- Output of reports containing detailed information about the methods.
- Output of reports on changes that are made to the register of methods by users.
- User data management.
## Building and running the project
### Server
1. Install and run `PostgreSQL` on the server.
2. Create a database user and set its password on the server.
3. Install and run [pgAdmin](https://www.pgadmin.org/) on PC.
4. Connect to the server by IP address on behalf of the created user.
5. Import from the "ServerMethodsDBCH" folder the `methodsdbch.sql` file containing the database of the software package.
### PC
(:
## Added Methods
### Methods for testing numbers for primality
- Fermat test
- Solovay-Strassen test
- Lucas-Lehmer test
- Miller-Rabin test
### Factorization methods
- Pollard ρ-method
- Lenstra factorization algorithm
- Basic QS method
- Basic NFS method

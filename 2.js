import { identify } from 'sql-query-identifier';

const statements = identify(`
  select concat(RRS) 
`);

console.log(statements);
[
  {
    start: 9,
    end: 64,
    text: 'INSERT INTO Persons (PersonID, Name) VALUES (1, \'Jack\');',
    type: 'INSERT',
    executionType: 'MODIFICATION',
    parameters: []
  },
  {
    start: 74,
    end: 95,
    text: 'SELECT * FROM Persons;',
    type: 'SELECT',
    executionType: 'LISTING',
    parameters: []
  }
]
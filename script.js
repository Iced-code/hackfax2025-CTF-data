
// Step 2: Function to create the table
function createTableFromJson(jsonData) {
  // Get the container element
  const container = document.getElementById('table-container');

  // Create the main table element
  const table = document.createElement('table');
  
  // Get the keys from the first object to use as table headers
  // const columns = Object.keys(jsonData[0]);
  columns = ["Challenge_Name","Category","Difficulty","Points","Attempts_Fail","Attempts_Successful"]
  // console.log(columns)

  // Create table header row
  const headerRow = document.createElement('tr');
  columns.forEach(col => {
    const th = document.createElement('th');
    th.innerHTML = col;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);

  // Create table body rows
  jsonData.forEach(item => {
    const dataRow = document.createElement('tr');
    columns.forEach(col => {
      const td = document.createElement('td');
      td.innerHTML = item[col];
      dataRow.appendChild(td);
    });
    table.appendChild(dataRow);
  });

  // Append the created table to the container
  container.appendChild(table);
}

async function loadChallenges() {
    const res = await fetch("http://127.0.0.1:5000/query/challenges");
    const data = await res.json();
    createTableFromJson(data);
}

loadChallenges();

// Call the function to generate the table
// createTableFromJson(d);

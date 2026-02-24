
function createTableFromJson(jsonData) {
  // Get the container element
  const container = document.getElementById('table-container');

  // Create the main table element
  const table = document.createElement('table');
  
  // Get the keys from the first object to use as table headers
  //const columns = Object.keys(jsonData[0]);
  const columns = ["ID", "Challenge_Name","Category","Difficulty","Points","Attempts","Attempts_Successful","Attempts_Fail", "Success_Rate"]

  // Create table header row
  const headerRow = document.createElement('tr');
  columns.forEach(col => {
    const th = document.createElement('th');
    th.innerHTML = col;
    headerRow.appendChild(th);
  });

  table.appendChild(headerRow);


  let id = 1;
  // Create table body rows
  jsonData.forEach(item => {
    const dataRow = document.createElement('tr');
    columns.forEach(col => {
      const td = document.createElement('td');
      td.innerHTML = item[col];

      if(col == "ID"){
        td.innerHTML = id;
        id+=1;
      }

      if((col === "Attempts_Successful") && item[col] === 0){
        dataRow.style.color = "red";
        td.style.fontWeight = "bold";
      }

      if(col === "Success_Rate"){
        td.innerHTML += "%";

        let r = parseInt(item[col]) / 100;
        // td.style.backgroundColor = `rgb(${r * 255}, 255, ${r * 255})`;
        td.style.backgroundColor = `rgb(${r * 245}, 255, ${r * 245})`;
      }

      if(item[col] == "Easy"){
        td.classList.add("difficulty-easy");
      }
      else if(item[col] == "Medium"){
        td.classList.add("difficulty-medium");
      }
      else if(item[col] == "Hard"){
        td.classList.add("difficulty-hard");
      }

      if(col !== "Challenge_Name" || col !== "Category" ){
        td.style.textAlign = "center"
      }

      dataRow.appendChild(td);
    });
    table.appendChild(dataRow);
  });
  /* jsonData.forEach(item => {
    const dataRow = document.createElement('tr');
    
    for (const col in item) {
      const td = document.createElement('td');
      td.innerHTML = item[col];

      if(item[col] == "Easy"){
        td.classList.add("difficulty-easy");
      }
      else if(item[col] == "Medium"){
        td.classList.add("difficulty-medium");
      }
      else if(item[col] == "Hard"){
        td.classList.add("difficulty-hard");
      }

      dataRow.appendChild(td);
    }
    
    table.appendChild(dataRow);
  }); */

  // Append the created table to the container
  container.appendChild(table);
}

function getQueryParams(){
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const isAscending = urlParams.get('isAscending');

  return isAscending;
}

async function loadChallenges() {
  const res = await fetch("http://127.0.0.1:5000/query/challenges");
  const data = await res.json();
  createTableFromJson(data);
}

loadChallenges();

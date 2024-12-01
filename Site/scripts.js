let table = `
  <div class="table_box">
    <p class="table_name"> Nome Tabela </p>
    <table>
      <tr> <!-- nomes das colunas -->
        <th>Company</th>
        <th>Contact</th>
        <th>Country</th>
      </tr>
      <tr> <!-- começo da tupla1 -->
        <td>Alfreds Futterkiste</td>
        <td>Maria Anders</td>
        <td>Germany</td>
      </tr>
      <tr><!-- começo da tupla2 -->
        <td>Centro comercial Moctezuma</td>
        <td>Francisco Chang</td>
        <td>Mexico</td>
      </tr>
    </table>
  </div>
`

async function filterCheck() {
  const filter1 = document.querySelector('#filter1')
  const filter2 = document.querySelector('#filter2')
  const filter3 = document.querySelector('#filter3')
  const tables = document.querySelector('#tables')
  tables.innerHTML += await makeTableFromFile('tabelateste')
}

// reads a line and returns an array with the values separated by comma splited */ 
function splitValuesOfLine(line) {
  return line.split(',')
}

// split a text file with multiple lines in an array where each position corresponds to a line*/
function splitLines(lines) {
  return lines.split('\n')
}

// reads a table name and then reads a text file with the same name from online repository and returns all text in that file
async function readTextFile(tableName) {
  let link = 'https://raw.githubusercontent.com/yuriralb/bancodedados/refs/heads/main/tables/'
  link = link + tableName //+ '.csv'
  const response = await fetch(link)
  const text = await response.text()
  lines = splitLines(text)
  return lines //outputs the content of the text file
}

// TODO: CHECK IF LAST ELEMENT OF lines ARRAY IS A SINGLE '\n' (if it is, then lines.length - 1. else, lines.length
// reads a table name and returns a HTML table based on a text file with same name in online repository
async function makeTableFromFile(tableName) {
  lines = await readTextFile(tableName)
  new_table = 
  `
  <div class="table_box">
    <p class="table_name"> ${tableName} </p>
    <table>
  `
  console.log(lines)
  for (let i = 0; i < lines.length - 1; i++) {
    lineValues = splitValuesOfLine(lines[i])
    new_table += '<tr>'
    if (i == 0) { // first line is always the name of the columns
      for (let j = 0; j < lineValues.length; j++) {
        new_table += `<th>${lineValues[j]}</th>`
      }
    } else { // remaining lines are always data
      for (let j = 0; j < lineValues.length; j++) {
        new_table += `<td>${lineValues[j]}</td>`
      }
    }
    new_table += '</tr>'
  }
  new_table += 
  `
    </table>
  </div>
  `
  console.log(new_table)
  return new_table
}
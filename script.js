const baseURL = "/grades";

function updateTable(data) {

    const tableBody = document.querySelector("#gradesTable tbody");
    tableBody.innerHTML = "";

    for (const name in data) {

        const row = `
            <tr>
                <td>${name}</td>
                <td>${data[name]}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    }
}

function getAllGrades() {
    
    fetch(baseURL)
    .then(response => response.json())
    .then(data => updateTable(data));
}

function getGrade() {

    const name = document.getElementById("name").value;
    const encodedName = name.replaceAll(" ", "%20");

    fetch(`${baseURL}/${encodeURIComponent(name)}`)
    .then(response => response.json())
    .then(data => updateTable(data));
}

function addGrade() {

    const name = document.getElementById("name").value;
    const grade = parseFloat(document.getElementById("grade").value);

    fetch(baseURL, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name: name,
            grade: grade
        })

    })
    .then(response => response.json())
    .then(() => getAllGrades());
}

function editGrade() {

    const name = document.getElementById("name").value;
    const grade = parseFloat(document.getElementById("grade").value);
    const encodedName = name.replaceAll(" ", "%20");

    fetch(`${baseURL}/${encodeURIComponent(name)}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            grade: grade
        })

    })
    .then(response => response.json())
    .then(() => getAllGrades());
}

function deleteGrade() {

    const name = document.getElementById("name").value;
    const encodedName = name.replaceAll(" ", "%20");

    fetch(`${baseURL}/${encodeURIComponent(name)}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(() => getAllGrades());
}
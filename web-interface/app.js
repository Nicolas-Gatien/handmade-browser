const searchButton = document.querySelector('button')
const searchInput = document.querySelector('input')
const searchResultsList = document.querySelector('#search-results')

searchButton.addEventListener('click', async (e) => {
    const params = new URLSearchParams();
    params.append("query", searchInput.value);
    const response = await fetch(`http://127.0.0.1:5555/search?${params}`, {
        method: "GET"
    });

    const data = await response.json()
    const results = data['results']

    searchResultsList.innerHTML = "<ol></ol>"

    for (const element of results) {
        searchResultsList.innerHTML += `<li><a href="${element[0]}">${element[0]}</a></li>`
    }

    console.log(data['results'])
})
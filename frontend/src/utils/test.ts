let response = await fetch('http://localhost:3000/api/auth/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(['admin', '123456'])
})
let data = await response.json()
console.log(data)

    // .then(response => response.json())
    // .then(data => console.log(data))
    // .catch(error => console.error('Error:', error));
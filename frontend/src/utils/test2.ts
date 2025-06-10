import baseApiUrl from "../api/baseUrl";

// const res = await fetch(new URL("auth/login", baseApiUrl),{
//     method: "POST",
//     body: JSON.stringify(["admin", "admin"])
// });
const res = await fetch('http://localhost:3000/api/auth/login?username=admin&password=123456')
console.log(await res.json());
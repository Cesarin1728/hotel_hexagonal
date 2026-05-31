export class AuthApiAdapter {
    constructor(baseUrl) { this.baseUrl = baseUrl; }
    async login(username, password) {
        const formData = new URLSearchParams();
        formData.append('username', username); formData.append('password', password);
        const res = await fetch(`${this.baseUrl}/api/auth/login`, {
            method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData.toString()
        });
        if (!res.ok) throw new Error("Credenciales inválidas");
        return await res.json();
    }
}
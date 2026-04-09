<template>
    <div>
        <div class="navbar">
            <router-link to="/admin/dashboard">Home</router-link>
            <router-link to="/admin/students">Students</router-link>
            <router-link to="/admin/search">Search</router-link>
            <router-link to="/admin/summary">Summary</router-link>
            <router-link to="/admin/profile">Profile</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <div class="container">
            <div class="card">
                <div class="header" style="justify-content: center;">
                    <h3 style="margin-left: 480px;">Registered Companies</h3>
                    <button class="btn-comp">Total Companies : {{companies.length}}</button>
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Company Id</th>
                                <th>Name</th>
                                <th>HR Contact</th>
                                <th>Drive Count</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="com in companies" :key="com.id">
                                <td>{{com.id}}</td>
                                <td>{{com.name}}</td>
                                <td>{{com.hr_contact}}</td>
                                <td>{{com.drive_count}}</td> 
                                <td>
                                    <button class="btn btn-black" @click="Blacklist(com.id)" v-show="com.status !== 'PENDING' && !com.is_blacklisted">Blacklist</button>
                                    <button class="btn btn-unblack" @click="Unblacklist(com.id)" v-show="com.status !== 'PENDING' && com.is_blacklisted">UnBlacklist</button>
                                    <button class="btn btn-success" @click="status(com.id, 'approve')" v-show="com.status === 'PENDING'" style="margin-left: 10px;">Approve✅</button>
                                    <button class="btn btn-danger" @click="status(com.id, 'reject')" v-show="com.status === 'PENDING'" style="margin-left: 10px;">Reject❌</button>
                                </td> 
                            </tr>
                            <tr v-show="companies.length === 0">
                                <td colspan="5" class="text-center"> ----No Companies Have Regiatered So Far----</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
           </div>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            companies: [],
            IsStatus: true
        }
    },
    methods: {
        async Blacklist(id) {
            try {
                const token = localStorage.getItem('token') 
                const response = await fetch('/api/admin/blacklist_company',{
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ id: id})
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    this.fetchCompanies()
                }
                else {
                    alert(data.message);
                }
            }
            catch (error) {
                console.error('Error:', error);
                alert('An error occurred while blacklisting the company!!')
            } 
        },
        async Unblacklist(id) {
            try {
                const token = localStorage.getItem('token') 
                const response = await fetch('/api/admin/blacklist_company',{
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`

                    },
                    body: JSON.stringify({ id: id})
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    this.fetchCompanies()
                }
                else {
                    alert(data.message);
                }
            }
            catch (error) {
                console.error('Error:', error);
                alert('An error occurred while Unblacklisting the company!!')
            }
        },
        async status(id, action) {
            try {
                const token = localStorage.getItem('token') 
                const response = await fetch('/api/admin/approve_reject_company', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ id: id, action: action})
                })
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    this.fetchCompanies()
                }
                else {
                    alert(data.message);
                }
            }
            catch (error) {
                console.error('Error:', error);
                alert('An error occurred while updating the company status!!')
            }
        },
        async fetchCompanies() {
            try {
                const token = localStorage.getItem('token') 
                const response = await fetch('/api/admin/companies', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    this.companies = data['Companies'];
                }
                else {
                    alert(data.message);
                }
            }
            catch (error) {
                console.error('Error:', error);
                alert('An error occurred while fetching companies!!')
            }
        }
    },
    mounted() {
        const role = localStorage.getItem('role')
        if (role !== 'admin') {
            alert('Unauthorized Access!! Admin access required.')
            this.$router.push('/')
        }
        this.fetchCompanies()
    }
}
</script>

<style scoped>
.navbar {
    display: flex;
    justify-content: space-around;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.75);
    padding: 16px 3px;
    margin: 28px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

.navbar a {
    text-decoration: none;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 25px;
    font-weight: bold;
    color: rgb(241, 111, 63);
    padding: 12px 30px;
    border-radius: 10px;
    transition: all 0.3s ease;
    display: inline-block;
}

.navbar a:hover {
    background-color: rgb(241, 111, 63);
    color: white;
    transform: scale(1.15);
}

.container{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
}
.card{
    width: 90%;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border: 2px solid chocolate;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(173, 216, 230, 0.8);
    text-align: center;
    position: relative;

}

.card .content{
    max-height: 400px;
    overflow: auto;
    padding: 8px 0;
}
.card .header{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: lightcoral ;
    width: 100%;
    padding: 15px;
    box-sizing: border-box;
    border-radius: 10px;

}
.card h3{
    margin: 0;
    font-size: 30px;
    font-weight: bold;
}

table{
    border-radius: 10px;
    border-collapse: collapse;
    width: 100%;
    margin: 29px auto;
    background: whitesmoke;
    text-align: center;
    box-shadow: 0 4px 8px rgba(173, 216, 230, 0.8);
    overflow: hidden;
}
th{
    background-color: rgb(232, 186, 169);
    color: black;
    padding: 20px;
    margin: 0;
    font-size: 22px;
    font-weight: bold;
    text-align: center;

}
td{
    padding: 10px;
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    border-bottom: 1px solid whitesmoke;
}
tr:nth-child(even){
    background-color: rgb(177, 128, 177);
}
tr:hover{
    background: rgb(241, 183, 241);
}

.card .btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}

button {
    background-color: lightblue;
    font-weight: bold;
} 

.card .btn-black {
    color: red;
}

.card .btn-unblack {
    color: green;
}
.card .btn-success {
    color: green;
}

.card .btn-danger {
    color: red;
}
.card .btn-black:hover {
    background-color: red;
    color: white;
    transform: scale(1.15);
}
.card .btn-unblack:hover {
    background-color: green;
    color: white;
    transform: scale(1.15);
}
.card .btn-success:hover {
    background-color: green;
    color: white;
    transform: scale(1.15);
}
.card .btn-danger:hover {
    background-color: rgb(185, 57, 57);
    color: white;
    transform: scale(1.15);
}

.header .btn-comp {
    padding: 13px;
    background-color: goldenrod;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-left: 250px;
}
.btn-comp:hover {
    transform: scale(1.05);
}
</style>
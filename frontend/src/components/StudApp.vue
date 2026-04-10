<template>
    <div>
        <div class="navbar">
            <router-link to="/student/dashboard">Home</router-link>
            <router-link to="/student/profile">Profile</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <div class="container">
            <div class="card">
                <div class="header">
                    <h3 style="margin-left: 500px;">Student Applications</h3>
                    <button class="btn btn-download" @click="downloadApplications"><i class="fa-solid fa-download"></i> - Download CSV</button>
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Drive ID</th>
                                <th>Company Name</th>
                                <th>Job Title</th>
                                <th>Applied Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="app in applications" :key="app.application_id">
                                <td>{{app.drive_id}}</td>
                                <td>{{ app.company_name }}</td>
                                <td>{{ app.job_title }}</td>
                                <td>{{ app.applied_date }}</td>
                                <td :class="app.status === 'SELECTED' ? 'selected' : app.status==='REJECTED' ? 'rejected' : 'pending'">{{ app.status }}</td>
                            </tr>
                            <tr v-if="Array.isArray(applications) && applications.length === 0">
                                <td colspan="6" class="text-center">----No Applications are filled so far----</td>
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
            applications : [],
        }
    },
    methods: {
        async fetchApplications() {
            try {
                const token = localStorage.getItem('token')
                const response = await fetch('/api/student/application_history', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json()
                this.applications = data['Application_History']
                if (!response.ok) {
                    alert(data.message)
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while fetching student applications!!')
            };
        },
        async downloadApplications() {
            try {
                const token = localStorage.getItem('token')
                const response = await fetch('/api/student/export_csv', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                })
                const data = await response.json()
                if (!response.ok) {
                    alert(data.message)
                } else {
                    alert('Application History Sent Successfully!! Check your mail.')
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while triggering the export task!!')
            };
        }

    },
    mounted() {
        const role = localStorage.getItem('role')
        if (role !== 'student') {
            alert('Unauthorized Access!! Student access required.')
            this.$router.push('/')
        }
        this.fetchApplications()
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
    max-height: 300px;
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

.selected {
    color: white;
    background-color: green;
    font-weight: bold;
}
.rejected {
    color: white;
    background-color: red;
    font-weight: bold;
}
.pending {
    color: white;
    background-color: orange;
    font-weight: bold;
}

.btn-download {
    padding: 12px 25px;
    background-color: goldenrod;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-download:hover {
    background-color: gold;
    transform: scale(1.05);
}

</style>

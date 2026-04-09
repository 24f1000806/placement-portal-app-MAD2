<template>
    <div>
        <div class="navbar" v-show="!ifdetails">
            <router-link to="/admin/students">Students</router-link>
            <router-link to="/admin/companies">Companies</router-link>
            <router-link to="/admin/search">Search</router-link>
            <router-link to="/admin/summary">Summary</router-link>
            <router-link to="/admin/profile">Profile</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <div class="container" v-show="!ifdetails">
            <div class="card">
                <div class="header" style="justify-content: center;">
                    <h3 style="margin-left: 550px;">Drives</h3>
                    <button class="btn-drive">Total Drives : {{drives.length}}</button>
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Drive Id</th>
                                <th>Job title</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="drive in drives" :key="drive.drive_id">
                                <td>{{drive.drive_id}}</td>
                                <td>{{drive.job_title}}</td>
                                <td>
                                    <button class="btn btn-primary" @click="detail(drive.drive_id)">View Detailsℹ️</button>
                                    <button class="btn btn-success" @click="status(drive.drive_id, 'approve')" v-show="drive.status === 'PENDING'" style="margin-left: 10px;">Approve✅</button>
                                    <button class="btn btn-danger" @click="status(drive.drive_id, 'reject')" v-show="drive.status === 'PENDING'" style="margin-left: 10px;">Reject❌</button>
                                </td>
                            </tr>
                            <tr v-if="drives.length === 0">
                                <td colspan="3" class="text-center"> ----No Drives created So Far----</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
           </div>
        </div>
        <br><br>
        <div class="container" v-show="!ifdetails">
            <div class="card">
                <div class="header" style="justify-content: center;">
                    <h3 style="margin-left: 480px;">Student Applications</h3>
                    <button class="btn-app">Total Applications : {{applications.length}}</button>
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Application Id</th>
                                <th>Drive Id</th>
                                <th>Company Id</th>
                                <th>Student Id</th>
                                <th>Applied Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="app in applications" :key="app.application_id">
                                <td>{{app.application_id}}</td>
                                <td>{{app.drive_id}}</td>
                                <td>{{ app.company_id }}</td>
                                <td>{{ app.student_id }}</td>
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
        <div class="details" v-show="ifdetails">
            <form>
                <h2>Drive Details!!</h2>
                <div class="details-grid">
                    <div class="field">
                        <label>ID:</label>
                        <input :value="details.drive_id" readonly>
                    </div>

                    <div class="field">
                        <label>Company Name:</label>
                        <input :value="details.company_name" readonly>
                    </div>

                    <div class="field">
                        <label>Job Title:</label>
                        <input :value="details.job_title" readonly>
                    </div>

                    <div class="field">
                        <label>Job Description:</label>
                        <textarea :value="details.job_desc" readonly></textarea>
                    </div>

                    <div class="field">
                        <label>Eligible Branch:</label>
                        <input :value="details.eligible_branch" readonly>
                    </div>

                    <div class="field">
                        <label>Eligible CGPA:</label>
                        <input :value="details.eligible_cgpa" readonly>
                    </div>

                    <div class="field">
                        <label>Eligible Year:</label>
                        <input :value="details.eligible_year" readonly>
                    </div>

                    <div class="field">
                        <label>Total Applications:</label>
                        <input :value="details.total_applications" readonly>
                    </div>

                    <div class="field">
                        <label>Deadline:</label>
                        <input :value="details.deadline" readonly>
                    </div>

                    <div class="field">
                        <label>Status:</label>
                        <input :value="details.status" readonly>
                    </div>
                </div>
                <button @click.prevent="ifdetails=false">Back</button>
            </form>
        </div>
    </div>  
</template>

<script>
export default {
    data() {
        return {
            drives: [],
            details: {},
            applications: [],
            ifdetails: false
        }
    },
    methods: {
        async detail(id) {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch(`/api/admin/drive_detail/${id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                const data = await response.json()
                if (!response.ok) {
                    alert(data.message)
                }
                else {
                    this.details = data['details']
                    this.ifdetails = true
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while fetching drives!!')
            };
        },

        async status(id, action) {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch('/api/admin/approve_reject_drive', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        id: id,
                        action: action
                    })
                })
                const data = await response.json()
                if (response.ok) {
                    alert(data.message)
                    this.fetchDrives()
                }
                else {
                    alert(data.message)
                }
            }
            catch (error) {
                console.error('Error:', error)
                alert('An error occurred while updating the drive status!!')
            }
        },

        async fetchDrives() {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch('/api/admin/placement_drives', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                const data = await response.json()
                this.drives = data['All_Placement_Drives']
                if (!response.ok) {
                    alert(data.message)
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while fetching drives!!')
            };
        },

        async fetchstudentApplications() {
            try {
                const token = localStorage.getItem('token')
                const response = await fetch('/api/admin/student_applications', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                const data = await response.json()
                this.applications = data['Applications']
                if (!response.ok) {
                    alert(data.message)
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while fetching student applications!!')
            };
        }

    },
    mounted() {
        const role = localStorage.getItem('role')
        if (role !== 'admin') {
            alert('Unauthorized Access!! Admin access required.')
            this.$router.push('/')
        }
        this.fetchDrives()
        this.fetchstudentApplications()
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

.card .btn-primary {
    color: dodgerblue;
}

.card .btn-success {
    color: green;
}

.card .btn-danger {
    color: red;
}
.card .btn-primary:hover {
    background-color: deepskyblue;
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
.details {
    width: 1000px;
    border: 2px solid chocolate;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(10px);
    padding: 50px;
    margin: 20px auto;
}

.details h2 {
    text-align: center;
    font-size: 40px;
    margin-bottom: 45px;
}

.details-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px 50px;
}

.field {
    display: flex;
    flex-direction: column;
}

.details label {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 8px;
    color: #222;
}

.details input {
    width: 100%;
    font-size: 15px;
    color: #333;
    border: 2px solid goldenrod;
    border-radius: 10px;
    padding: 15px;
    background: rgba(255, 255, 255, 0.8);
}
.details textarea {
    resize: none;
    height: 80px;
    border-radius: 10px;
    padding: 10px;
    border: 2px solid goldenrod;
}

.details button {
    margin-top: 40px;
    width: 150px;
    background: white;
    border: 2px solid goldenrod;
    padding: 15px;
    border-radius: 10px;
    font-size: 20px;
    font-weight: bold;
    display: block;
    margin-left: auto;
    margin-right: auto;
    transition: 0.3s ease;
}

.details button:hover {
    background: gold;
    transform: scale(1.2);
}
.header .btn-drive {
    padding: 13px;
    background-color: goldenrod;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 17px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-left: 400px;
}

.btn-drive:hover {
    transform: scale(1.05);
}
.header .btn-app {
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
.btn-app:hover {
    transform: scale(1.05);
}
</style>
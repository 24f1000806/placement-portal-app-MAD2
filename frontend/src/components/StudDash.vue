<template>
    <div>
        <div class="navbar" v-show="!ifdetails">
            <router-link to="/student/history">Placement History</router-link>
            <router-link to="/student/profile">Profile</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <div class="container" v-show="!ifdetails">
            <div class="card">
                <div class="header" style="justify-content: center;">
                    <button :class="{active: activebtn==='all'}" @click="activebtn ='all'">All Drives</button>
                    <button :class="{active: activebtn==='ele'}" @click="activebtn ='ele'">Eligible Drives</button>
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Drive Id</th>
                                <th>Company Name</th>
                                <th>Job title</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody v-show="activebtn==='all'">
                            <tr v-for="drive in alldrives" :key="drive.drive_id">
                                <td>{{drive.drive_id}}</td>
                                <td>{{drive.company_name}}</td>
                                <td>{{drive.job_title}}</td>
                                <td>
                                    <button class="btn btn-primary" @click="detail(drive.drive_id)">View Detailsℹ️</button>
                                    <button class="btn btn-success" @click="apply(drive.drive_id)" v-show="!drive.applied" style="margin-left: 10px;">Apply✅</button>
                                    <button class="btn btn-applied" v-show="drive.applied" style="margin-left: 10px;">Already Applied⚠️</button>
                                </td>
                            </tr>
                            <tr v-if="alldrives.length === 0">
                                <td colspan="30"> ------No Drives to Apply------ </td>
                            </tr>
                        </tbody>
                        <tbody v-show="activebtn==='ele'">
                            <tr v-for="drive in eledrives" :key="drive.drive_id">
                                <td>{{drive.drive_id}}</td>
                                <td>{{drive.company_name}}</td>
                                <td>{{drive.job_title}}</td>
                                <td>
                                    <button class="btn btn-primary" @click="detail(drive.drive_id)">View Detailsℹ️</button>
                                    <button class="btn btn-success" @click="apply(drive.drive_id)" v-show="!drive.applied" style="margin-left: 10px;">Apply✅</button>
                                    <button class="btn btn-applied" v-show="drive.applied" style="margin-left: 10px;">Already Applied⚠️</button>
                                </td>
                            </tr>
                            <tr v-if="eledrives.length === 0">
                                <td colspan="30"> ------You are not Eligible for any Drive------ </td>
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
                        <label>Deadline:</label>
                        <input :value="details.deadline" readonly>
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
            alldrives: [],
            eledrives: [],
            details: {},
            activebtn: 'all',
            ifdetails:false,
        }
    },
    methods: {
        async detail(id) {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch(`/api/student/drive_detail/${id}`, {
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
                alert('An error occurred while getting drive details!!')
            };
        },

        async fetchAllDrives() {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch('/api/student/all_drives', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                const data = await response.json()
                this.alldrives = data['All_Placement_Drives']
                if (!response.ok) {
                    alert(data.message)
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while fetching drives!!')
            };
        },
        async fetchEleDrives() {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch('/api/student/eligible_drives', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                const data = await response.json()
                this.eledrives = data['eligible_drives']
                if (!response.ok) {
                    alert(data.message)
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while fetching drives!!')
            };
        },

        async apply(id) {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch('/api/student/apply_drive', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        id: id
                    })
                })
                const data = await response.json()
                if (!response.ok) {
                    alert(data.message)
                }
                else{
                    alert('Applied Successfully!!')
                    this.fetchAllDrives()
                    this.fetchEleDrives()
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('Applying Failed!! Try again later')
            };
            
        }
    },
    mounted() {
        const role = localStorage.getItem('role')
        if (role !== 'student') {
            alert('Unauthorized Access!! Student access required.')
            this.$router.push('/')
        }
        this.fetchAllDrives()
        this.fetchEleDrives()
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
.card .header button {
    width: 500px;
    padding: 20px;
    background-color: lightcoral;
    border: 0px solid lightcoral;
    border-radius: 10px;
    margin: auto;
    font-size: larger;
    transition: all 0.2s ease;
}
.card .header button:hover {
    background-color: goldenrod;
    transform: scale(1.1);
}
.card .header button.active {
    background-color: goldenrod;
    transform: scale(1.25);
    transition: all 0.3 ease;
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
    transition: background-color 0.3s ease;
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

.card .btn-applied {
    color: goldenrod;
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
.card .btn-applied:hover {
    background-color: rgb(185, 57, 57);
    color: white;
    transform: scale(1.10);
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

.details .field {
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
</style>
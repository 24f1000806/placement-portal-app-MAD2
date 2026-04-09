<template>
    <div>
        <div class="navbar" v-show="ifnavbar">
            <router-link to="/company/dashboard">Home</router-link>
            <router-link to="/company/profile">Profile</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <div class="container" v-show="ifapps">
            <div class="card">
                <div class="header" style="justify-content: center;">
                    <h3>Applications</h3>
                </div>
                <div class="content">
                    <table>
                        <thead>
                            <tr>
                                <th>Application Id</th>
                                <th>Job title</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="app in applications" :key="app.application_id">
                                <td>{{app.application_id}}</td>
                                <td>{{app.job_title}}</td>
                                <td>
                                    <button class="btn btn-primary" @click="detail(app.application_id)">View Applicationℹ️</button>
                                    <button class="btn btn-success" @click.prevent="status(app.application_id, 'select')" v-show="app.status === 'APPLIED'" style="margin-left: 10px;">Select✅</button>
                                    <button class="btn btn-danger" @click.prevent="status(app.application_id, 'reject')" v-show="app.status === 'APPLIED'" style="margin-left: 10px;">Reject❌</button>
                                </td>
                            </tr>
                            <tr v-if="applications.length === 0">
                                <td colspan="3" class="text-center"> ----No Applications applied So Far----</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
           </div>
        </div>
        <div class="details" v-show="ifdetails">
            <form>
                <h2>Application Details!!</h2>
                <div class="details-grid">
                    <div class="field">
                        <label>Application ID:</label>
                        <input :value="details.application_id" readonly>
                    </div>

                    <div class="field">
                        <label>Drive ID:</label>
                        <input :value="details.drive_id" readonly>
                    </div>

                    <div class="field">
                        <label>Job Title:</label>
                        <input :value="details.job_title" readonly>
                    </div>

                    <div class="field">
                        <label>Student Name:</label>
                        <input :value="details.student_name" readonly>
                    </div>

                    <div class="field">
                        <label>Branch:</label>
                        <input :value="details.branch" readonly>
                    </div>

                    <div class="field">
                        <label>CGPA:</label>
                        <input :value="details.cgpa" readonly>
                    </div>
                    
                    <div class="field">
                        <label>Year:</label>
                        <input :value="details.year" readonly>
                    </div>

                    <div class="field">
                        <label>Resume Path:</label>
                        <a :href="details.resume" target="_blank" class="resume-link">
                            {{ details.resume }}
                        </a>
                    </div>

                    <div class="field">
                        <label>Applied Date:</label>
                        <input :value="details.applied_date" readonly>
                    </div>

                    <div class="field">
                        <label>Status:</label>
                        <input :value="details.status" readonly>
                    </div>
                </div>
                <button @click.prevent="ifnavbar=true; ifdetails=false; ifapps=true;">Back</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            applications : [],
            details: {},
            ifapps:true,
            ifdetails:false,
            ifnavbar:true
        }
    },
    methods: {
        async detail(id) {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch(`/api/company/application_detail/${id}`, {
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
                    this.ifapps=false;
                    this.ifnavbar=false;
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while getting drive details!!')
            };
        },

        async status(id, action) {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch('/api/company/update_application_status', {
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
                    this.fetchapplications()
                }
                else {
                    alert(data.message)
                }
            }
            catch (error) {
                console.error('Error:', error)
                alert('An error occurred while updating the application status!!')
            }
        },

        async fetchapplications() {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch('/api/company/student_applications', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                })
                const data = await response.json()
                this.applications = data['Applications']
                if (!response.ok) {
                    alert(data.message)
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while fetching applications!!')
            };
        },
    },
    mounted() {
        const role = localStorage.getItem('role')
        if (role !== 'company') {
            alert('Unauthorized Access!! Company access required.')
            this.$router.push('/')
        }
       this.fetchapplications()
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
    transition: all 0.3s ease;
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
    transform: scale(1.11);
}
.card .btn-success:hover {
    background-color: green;
    color: white;
    transform: scale(1.12);
}
.card .btn-danger:hover {
    background-color: rgb(185, 57, 57);
    color: white;
    transform: scale(1.12);
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

.resume-link {
    display: block;
    width: 100%;
    font-size: 15px;
    color: #333;
    border: 2px solid goldenrod;
    border-radius: 10px;
    padding: 15px;
    background: rgba(255, 255, 255, 0.8);
    text-decoration: none;
}

</style>
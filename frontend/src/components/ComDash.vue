<template>
    <div>
        <div class="navbar" v-show="ifnavbar">
            <router-link to="/company/applications">Applications</router-link>
            <router-link to="/company/profile">Profile</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <div class="container" v-show="ifdrives">
            <div class="card">
                <div class="header" style="justify-content: center;">
                    <h3>Drives</h3>
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
                                <td>{{drive.id}}</td>
                                <td>{{drive.job_title}}</td>
                                <td>
                                    <button class="btn btn-primary" @click.prevent="detail(drive.id)">View Detailsℹ️</button>
                                    <button class="btn btn-success" @click.prevent="close(drive.id)" v-show="drive.status === 'APPROVED'" style="margin-left: 10px;">Close✅</button>
                                    <button class="btn btn-danger" v-show="drive.status === 'CLOSED'" style="margin-left: 10px;">Closed❌</button>
                                </td>
                            </tr>
                            <tr v-if="drives.length === 0">
                                <td colspan="3" class="text-center"> ----No Drives created So Far----</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
           </div>
            <div class="add">
                <button @click.prevent="ifnavbar=false; ifdetails=false; ifdrives=false; ifcreate=true">+ Create Drive</button>
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
                <button @click.prevent="ifnavbar=true; ifdetails=false; ifdrives=true; ifcreate=false">Back</button>
            </form>
        </div>
        <div v-if="ifcreate" class="main">
            <div class="create">
                <form @submit.prevent="createdrive">
                    <i class="fa-solid fa-plus"></i>
                    <br><br>
                    <div class="input-box"> 
                        <input type="text" v-model='job_title' placeholder="Job Title" required="true">
                    </div>
                    <div class="input-box">
                        <textarea v-model="job_desc" placeholder="Job Description" required></textarea>
                    </div>
                    <div class="input-box">
                        <select v-model="branch" required>
                            <option disabled value="">Eligible Branch</option>
                            <option value="cse">CSE</option>
                            <option value="it">IT</option>
                            <option value="ece">ECE</option>
                            <option value="eee">EEE</option>
                            <option value="me">ME</option>
                            <option value="ce">CE</option>
                        </select>
                    </div>
                    <div class="input-box">
                        <select v-model="year" required>
                            <option disabled value="">Eligible Year</option>
                            <option value="1">1st Year</option>
                            <option value="2">2nd Year</option>
                            <option value="3">3rd Year</option>
                            <option value="4">4th Year</option>
                        </select>
                    </div>
                    <div class="input-box">
                        <input type="number" min="1" max="10" step="0.1" v-model='cgpa'  placeholder="Eligible CGPA" required="true">
                    </div>
                    <div class="input-box">
                        <input type="date" v-model='app_deadline'  placeholder="Deadline" required="true">
                    </div>
                    <button @click.prevent="ifnavbar=true; ifdetails=false; ifdrives=true; ifcreate=false"><strong>Back</strong></button>
                    <button type="submit" style="margin-left: 15px;"><strong>Create+</strong></button>
                </form>
            </div>         
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return{
            drives: [],
            ifdrives: true,
            ifcreate: false,
            ifnavbar: true,
            ifdetails: false,
            details: [],
            job_title: '',
            job_desc: '',
            branch: '',
            year: '',
            cgpa: '',
            app_deadline: ''
        }

    },
    methods: {
        async detail(id) {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch(`/api/company/drive_detail/${id}`, {
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
                    this.ifcreate=false;
                    this.ifdrives=false;
                    this.ifnavbar=false;
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while getting drive details!!')
            };
        },

        async close(id) {
            const token = localStorage.getItem('token')
            try {
                const response = await fetch('/api/company/close_drive', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({id: id})
                })
                const data = await response.json()
                if (!response.ok) {
                    alert(data.message)
                }
                else {
                    alert(data.message)
                    this.fetchdrives()
                }
            }
            catch(error) {
                console.error('Error:', error)
                alert('An error occurred while closiing drive !!')
            };
        },

        async createdrive(){
            try{
                const token = localStorage.getItem('token')
                const response = await fetch('/api/company/create_drive', {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        job_title: this.job_title,
                        job_description: this.job_desc,
                        eligible_branch: this.branch,
                        eligible_year: this.year,
                        eligible_cgpa: this.cgpa,
                        application_deadline: this.app_deadline
                    })
                });
                const data =  await response.json()
                console.log(data)
                if (!response.ok){
                    alert(data.message)
                    this.ifcreate=false;
                    this.ifdetails=false;
                    this.ifdrives=true;
                    this.ifnavbar=true;
                    this.clearDriveForm();
                }
                else {
                    alert(data.message)
                    this.clearDriveForm();
                    this.fetchdrives();
                    this.ifcreate=false;
                    this.ifdetails=false;
                    this.ifdrives=true;
                    this.ifnavbar=true;
                }
            }
            catch(error){
                console.error('Error:', error);
                alert('An error occured while creating Drive!! Please try again later.')
            }
        },
        async fetchdrives(){
            try{
                const token = localStorage.getItem('token')
                const response = await fetch('/api/company/drives', {
                    headers: {
                    'Authorization': `Bearer ${token}`
                    },
                });
                const data =  await response.json()
                if (!response.ok){
                    alert(data.message)
                }
                else {
                    this.drives = data['Drives']
                }
            }
            catch(error){
                console.error('Error:', error);
                alert('An error occured while creating Drive!! Please try again later.')
            }
        },
        clearDriveForm() {
            this.job_title = '';
            this.job_desc = '';
            this.branch = '';
            this.year = '';
            this.cgpa = '';
            this.app_deadline = '';
        }
    },
    mounted() {
        const role = localStorage.getItem('role')
        if (role !== 'company') {
            alert('Unauthorized Access!! Company access required.')
            this.$router.push('/')
        }
        this.fetchdrives()
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

.card .btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
    background-color: lightblue;
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
    transform: scale(1.13);
}
.card .btn-success:hover {
    background-color: green;
    color: white;
    transform: scale(1.13);
}
.card .btn-danger:hover {
    background-color: rgb(185, 57, 57);
    color: white;
    transform: scale(1.13);
}
.create {
    width: 350px;
    height: 520px;
    margin-top: 50px;
    margin-left: 550px;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border: 2px solid chocolate;
    border-radius: 20px;
    text-align: center;
}

.create input {
    width: 300px;
    height: 40px;
    border-radius: 10px;
    margin-bottom: 15px;
    padding-left: 15px;
    font-weight: bold;
    font-size: 15px;
    border: 2px solid goldenrod;
}

.create textarea {
    width: 300px;
    height: 80px;
    border-radius: 10px;
    margin-bottom: 15px;
    padding: 10px 15px;
    font-weight: bold;
    font-size: 15px;
    border: 2px solid goldenrod;
    resize: none;
    font-family: inherit;
}

.create select {
    width: 300px;
    height: 40px;
    border: 2px solid goldenrod;
    border-radius: 10px;
    margin-bottom: 15px;
    padding-left: 10px;
    font-weight: bold;
    font-size: 15px;
    font-family: cursive;
}

select:invalid {
  color: gray;
}

.create option {
    font-weight: bold;
    font-size: 15px;
    color: goldenrod;
}

.create button {
    width: 117px;
    height: 40px;
    border-radius: 10px;
    margin-top: 10px;
    font-size: 16px;
    border: 2px solid goldenrod;
    transition: all 0.3s ease;
}

.create button:hover {
    background-color: gold;
    transform: scale(1.1);

}

.create i {
    font-size: 40px;
    color: black;
    margin-top: 20px;
}

.add button{
    width: 150px;
    background: #fff;
    border: none;
    padding: 15px;
    border-radius: 10px;
    border: 2px solid goldenrod;
    font-size: 17px;
    font-weight: bold;
    margin: 20px auto;
    transition: all 0.3s ease;
}
.add button:hover{
    transform: scale(1.2);
    background: gold;
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
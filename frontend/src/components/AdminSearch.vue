<template>
    <div>
        <div class="navbar" v-show="ifnavbar">
            <router-link to="/admin/dashboard">Home</router-link>
            <router-link to="/admin/students">Students</router-link>
            <router-link to="/admin/companies">Companies</router-link>
            <router-link to="/admin/summary">Summary</router-link>
            <router-link to="/admin/profile">Profile</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
       <div class="search" style="padding: 50px;" v-show="ifsearch">
            <form @submit.prevent="search">
                <select v-model="searchfor" required>
                    <option value="company">Company</option>
                    <option value="student">Student</option>
                </select>
                <input style="width: 450px;" type="number" v-model.number="id" placeholder="Search Companies/Students by ID" min="1" required>
                <button type="submit">Search</button>
            </form>
       </div>
       <div class="details" v-show="ifcompany">
        <form>
            <h2>Company Details!!</h2>
            <br><br>
            <div class="input-box"> 
              <label>ID:</label>  
              <input :value="company.id" readonly>
            </div>
            <div class="input-box">
              <label>Name:</label>
              <input :value="company.name" readonly>      
            </div>
            <div class="input-box">
              <label >HR Contact:</label>
              <input :value="company.hr_contact" readonly>
            </div>
            <div class="input-box"> 
              <label for>Drive Count:</label>
              <input :value="company.drive_count" readonly>
            </div>
            <div class="input-box"> 
              <label for>Status:</label>
              <input :value="company.status" readonly>
            </div>
            <div class="input-box"> 
              <label for>Is Blacklisted?:</label>
              <input :value="company.is_blacklisted" readonly>
            </div>
            <button @click.prevent="ifcompany=false; ifsearch=true; ifnavbar=true">Back</button>
        </form>
       </div>
       <div class="details" v-show="ifstudent">
        <form>
            <h2>Student Details!!</h2>
            <br><br>
            <div class="input-box"> 
              <label>ID:</label>  
              <input :value="student.id" readonly>
            </div>
            <div class="input-box">
              <label>Name:</label>
              <input :value="student.name" readonly>      
            </div>
            <div class="input-box">
              <label >Branch:</label>
              <input :value="student.branch" readonly>
            </div>
            <div class="input-box"> 
              <label for>Year:</label>
              <input :value="student.year" readonly>
            </div>
            <div class="input-box"> 
              <label for>CGPA:</label>
              <input :value="student.cgpa" readonly>
            </div>
            <div class="input-box"> 
              <label for>Is Blacklisted?:</label>
              <input :value="student.is_blacklisted" readonly>
            </div>
            <button @click.prevent="ifstudent=false; ifsearch=true; ifnavbar=true">Back</button>
        </form>
       </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            searchfor: 'company',
            id: null,
            company: {},
            student: {},
            ifnavbar: true,
            ifsearch: true,
            ifcompany: false,
            ifstudent: false,
        }
    },
    methods: {
        async search() {
            const searchfor = this.searchfor
            const id = this.id
            if (searchfor === 'company') {
                try {
                    const token = localStorage.getItem('token')
                    const response = await fetch(`/api/admin/search_company/${id}`, {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    const data = await response.json()
                    this.company = data['Company_Info']
                    if (!response.ok) {
                        alert(data.message)
                        this.ifsearch = true
                        this.ifcompany = false
                        this.ifnavbar = true
                    }
                    else {
                        this.ifsearch = false
                        this.ifcompany = true
                        this.ifnavbar = false
                    }
                }
                catch(error) {
                    console.error('Error:', error)
                    alert('An error occurred while fetching student applications!!')
                };
            }
                
            else {
                try {
                    const token = localStorage.getItem('token')
                    const response = await fetch(`/api/admin/search_student/${id}`, {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    const data = await response.json()
                    this.student = data['Student_Info']
                    if (!response.ok) {
                        alert(data.message)
                        this.ifsearch = true
                        this.ifstudent = false
                        this.ifnavbar = true
                    }
                    else {
                        this.ifsearch = false
                        this.ifstudent = true
                        this.ifnavbar = false
                    }
                }
                catch(error) {
                    console.error('Error:', error)
                    alert('An error occurred while fetching student applications!!')
                };
            }
        }
    },
    mounted() {
        const role = localStorage.getItem('role')
        if (role !== 'admin') {
            alert('Unauthorized Access!! Admin access required.')
            this.$router.push('/')
        }
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
.search{
    display: flex;
    align-items: center;
    justify-content: center;
}
.search form{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 30px;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border-radius: 10px;
    border: 2px solid chocolate;
    padding: 20px;
}
.search select, input {
    padding: 15px;
    width: 200px;
    border-radius: 10px;
    font-size: 16px;
    background: #fff;
    border: 2px solid goldenrod;

}

.search button{
    width: 100px;
    background: #fff;
    border: none;
    padding: 15px;
    border-radius: 10px;
    border: 2px solid goldenrod;
    font-size: 15px;
    font-weight: bold;
    margin: 20px auto;
    transition: 0.3s ease;
}
button:hover{
    background: gold;
    transform: scale(1.2);
}
.details {
    width: 400px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.5);
    padding: 20px;
    position: relative;
    box-sizing: border-box;
    margin: auto;
    margin-top: 10px;
}
.details h2{
    text-align: center;
    font-size: 35px;
}
.details .input-box{
    position: relative;
    width: 100%;
    margin-bottom: 20px ;
}
.details .input-box input{
    width: 100%;
    font-size: 15px;
    color: #333;
    letter-spacing: 1px;
    outline: none;
    border: solid 2px rgba(255, 255, 255, 0.5);
    border-radius: 10px;
    padding: 10px;
    padding-right: 40px;
    box-sizing: border-box;
}
.input-box i{
    position: absolute;
    right: 20px;
    top: 50%;
    font-size: 20px;
    transform: translateY(-50%);
    pointer-events: none;
}

button{
    width: 100px;
    background: #fff;
    border: none;
    padding: 9px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: bold;
    display: block;
    transition: background 0.3s ease;
    margin: auto;
}
label{
    font-size: 19px;
    font-weight: bold;
    color: #333;
}    
</style>
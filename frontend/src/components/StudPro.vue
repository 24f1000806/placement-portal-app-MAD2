<template>
   <div>
        <div class="navbar">
            <router-link to="/student/dashboard">Home</router-link>
            <router-link to="/student/history">Placement History</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <div class="profile">
            <form @submit.prevent="updateprofile">
                <i class="fa-solid fa-id-card"></i>
                <br><br>
                <div class="input-box"> 
                    <label for="name">Name:</label>  
                    <input type="text" id="name" v-model="username" value="{{username}}" required>
                </div>
                <div class="input-box">
                    <label for="email">Email:</label>
                    <input type="email" id="email" v-model="email" value="{{email}}" required>
                </div>
                <div class="input-box">
                    <label for="branch">Branch:</label>
                    <input type="text" id="branch" v-model="branch" value="{{branch}}" readonly>
                </div>
                <div class="input-box">
                    <label for="year">Year:</label>
                    <input type="number" min="1" max="4" id="year" v-model="year" value="{{year}}" required>
                </div>
                <div class="input-box">
                    <label for="cgpa">CGPA:</label>
                    <input type="number" min="1" max="10" step="0.1" id="cgpa" v-model="cgpa" value="{{cgpa}}" required>
                </div>
                <div class="input-box">
                    <label for="resume">Resume Path:</label>
                    <input type="url" id="resume" v-model="resume" value="{{resume}}" required>
                </div>
                <!-- <br><br> -->
                <button type="submit">Update</button>
            </form>
        </div>
   </div>

</template>

<script>
    export default {
        data() {
            return {
                username: '',
                email: '',
                branch: '',
                year: null,
                cgpa: null,
                resume: ''
            }
        },
        methods: {
            async updateprofile() {
                try {
                    const token = localStorage.getItem('token');
                    const response = await fetch('/api/student/profile', {
                        method: 'PUT',
                        headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            name: this.username,
                            email: this.email,
                            branch: this.branch,
                            year: this.year,
                            cgpa: this.cgpa,
                            resume: this.resume,
                        })
                    });
                    const data = await response.json();
                    if (response.ok) {
                        alert(data.message);
                    }
                    else {
                        alert(data.message);
                    }
                }
                catch (error) {
                    console.error('Error:',error);
                    alert('An error occured while updating profile!!');
                }
            },
            async fetchprofile(){
                try {
                    const token = localStorage.getItem('token');
                    const response = await fetch('/api/student/profile', {
                        headers: {
                        'Authorization': `Bearer ${token}`
                        }
                    });
                    const data = await response.json();
                    if (response.ok) {
                        this.username = data.name;
                        this.email = data.email;
                        this.branch = data.branch;
                        this.year = data.year;
                        this.cgpa = data.cgpa;
                        this.resume = data.resume;
                    }
                    else {
                        alert(data.message);
                    }
                }
                catch (error) {
                    console.error('Error:',error);
                    alert('An error occured while fetching profile!!');
                }  
            }
        },
        mounted() {
            const role = localStorage.getItem('role')
            if (role !== 'student') {
                alert('Unauthorized Access!! Student access required.')
                this.$router.push('/')
            }
            this.fetchprofile();        
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
.profile {
    width: 380px;
    height: 650px;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border: 2px solid chocolate;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.5);
    padding: 40px;
    position: relative;
    box-sizing: border-box;
    margin: auto;
    margin-top: 15px;

}.profile .input-box{
    position: relative;
    width: 100%;
    margin-bottom: 20px ;

}.profile .input-box input{
    width: 100%;
    font-size: 15px;
    color: #333;
    letter-spacing: 1px;
    outline: none;
    border: solid 2px goldenrod;
    border-radius: 10px;
    padding: 10px;
    padding-right: 40px;
    box-sizing: border-box;
}

.profile i{
    position: absolute;
    right: 168px;
    top: 5%;
    font-size: 50px;
    transform: translateY(-50%);
    pointer-events: none;
}

button{
    width: 120px;
    background: #fff;
    border: 2px solid goldenrod;
    padding: 12px;
    border-radius: 10px;
    font-size: 17px;
    font-weight: bold;
    display: block;
    transition: all 0.3s ease;
    margin: auto;
}
button:hover{
    background-color: gold;
    transform: scale(1.1);
}
label{
    font-size: 19px;
    font-weight: bold;
    color: #333;
}   
</style>
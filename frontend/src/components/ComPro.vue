<template>
   <div>
        <div class="navbar">
            <router-link to="/company/dashboard">Home</router-link>
            <router-link to="/company/applications">Applications</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
        <div class="profile">
            <form @submit.prevent="updateprofile">
                <i class="fa-solid fa-user-tie"></i>
                <br><br>
                <br><br>
                <div class="input-box"> 
                    <label for="name">Name:</label>  
                    <input type="text" id="name" name="name" v-model="username" value="username" required>
                </div>
                <div class="input-box">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" v-model="email" value="email" required>
                </div>
                <div class="input-box">
                    <label for="hremail">HR Contact:</label>
                    <input type="email" id="hremail" name="email" v-model="hr_contact" value="hr_contact" required>
                </div>
                <br><br>
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
                hr_contact: ''
            }
        },
        methods: {
            async updateprofile() {
                try {
                    const token = localStorage.getItem('token');
                    const response = await fetch('/api/company/profile', {
                        method: 'PUT',
                        headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            name: this.username,
                            email: this.email,
                            hr_contact: this.hr_contact
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
                    const response = await fetch('/api/company/profile', {
                        headers: {
                        'Authorization': `Bearer ${token}`
                        }
                    });
                    const data = await response.json();
                    if (response.ok) {
                        this.username = data.name;
                        this.email = data.email;
                        this.hr_contact = data.hr_contact
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
            if (role !== 'company') {
                alert('Unauthorized Access!! Company access required.')
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
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border: 2px solid chocolate;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.5);
    padding: 40px;
    position: relative;
    box-sizing: border-box;
    margin: auto;
    margin-top: 50px;

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
    right: 170px;
    top: 13%;
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
    transform: scale(1.2);
}
label{
    font-size: 19px;
    font-weight: bold;
    color: #333;
}   
</style>
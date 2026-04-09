<template>
   <div v-if="isLogin" class="main">
        <form class="container" @submit.prevent="login">
            <i class="fa-solid fa-building-columns"></i>
            <br><br>
            <div class="input-icon">
              <input type="email" v-model='email' placeholder="Email" required>
            </div>
            <div class="input-icon">
                <input type="password" v-model='password' placeholder="Password" required>
            </div>
            <div>
                <button type="submit"><strong>Login</strong></button>
            </div>
            <span>
                <button type="button" @click="isLogin=false; StudentRegister=true; clearform()" style="margin-right: 20px;"><strong>Register as Student</strong></button>
                <button type="button" @click="isLogin=false; CompanyRegister=true; clearform()"><strong>Register as Company</strong></button>
            </span>              
        </form>
    </div>
    <div v-if="StudentRegister" class="main">
        <form class="student-reg" @submit.prevent="streg">
            <i class="fa-solid fa-user-graduate"></i>
            <br><br>
            <div>
              <input type="email" v-model='email' placeholder="Email" required>
            </div>
            <div>
                <input type="password" v-model='password'placeholder="Password" required>
            </div>
            <div>
                <input type="text" v-model='name' placeholder="Name" required>
            </div>
            <div>
                <select v-model="branch" required>
                    <option disabled value="">Select Branch</option>
                    <option value="cse">CSE</option>
                    <option value="it">IT</option>
                    <option value="ece">ECE</option>
                    <option value="eee">EEE</option>
                    <option value="me">ME</option>
                    <option value="ce">CE</option>
                </select>
            </div>
            <div>
                <select v-model="current_year" required>
                    <option disabled value="">Current Year</option>
                    <option value="1">1st Year</option>
                    <option value="2">2nd Year</option>
                    <option value="3">3rd Year</option>
                    <option value="4">4th Year</option>
                </select>
            </div>
            <div>
                <input type="number" min="1" max="10" step="0.1" v-model='cgpa'  placeholder="CGPA" required>
            </div>
            <div>
               <input type="url" v-model='resume_link' placeholder="Resume Link" required>
            </div> 
            <div>
                <button type="submit"><strong>Register</strong></button>
            </div>
            <div>-</div>
            <a href="" @click.prevent="isLogin=true; StudentRegister=false">Already Registered? Login</a>              
        </form>
        
    </div>
    <div v-if="CompanyRegister" class="main">
        <form class="company-reg" @submit.prevent="coreg">
            <i class="fa-solid fa-briefcase"></i>
            <br><br>
            <div>
              <input type="email" v-model='email' placeholder="Email" required>
            </div>
            <div>
                <input type="password" v-model='password' placeholder="Password" required>
            </div>
            <div>
                <input type="text" v-model='name' placeholder="Company Name" required>
            </div>
            <div>
                <input type="text" v-model='hr_contact' placeholder="HR Contact" required>
            </div>
            <div>
                <button type="submit"><strong>Register</strong></button>
            </div>  
            <div>-</div> 
            <a href="" @click.prevent="isLogin=true; CompanyRegister=false">Already Registered? Login</a>
        </form>
    </div>
</template>

<script>
export default {
    
    data() {
        return {
            isLogin: true,
            StudentRegister: false,
            CompanyRegister: false,
            email: '',
            password: '',
            name: '',
            branch: '',
            current_year: '',
            cgpa: '',
            resume_link: '',
            hr_contact: ''
        }
    },

    methods: {
        async login() {
            try {
                const response = await fetch('/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password
                    })
                })
                const data = await response.json()

                if (!response.ok) {
                    alert(data.message)
                    return;
                }
                                
                localStorage.setItem('token', data.auth_token);
                localStorage.setItem('role', data.role);

                if (data.role === 'student') {
                    this.clearform();
                    this.$router.push('/student/dashboard');
                }
                else if (data.role === 'company') {
                    this.clearform();
                    this.$router.push('/company/dashboard');
                }
                else {
                    this.clearform();
                    this.$router.push('/admin/dashboard');
                }
            } 
            catch(error){
                console.error('Error:', error);
                alert('An error occurred during login!! Please try again later');
            }
        },

        async streg() {
            try {
                const response = await fetch('/api/student/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                        student_name: this.name,
                        branch: this.branch,
                        year: this.current_year,
                        cgpa: this.cgpa,
                        resume_path: this.resume_link
                    })
                })

                const data = await response.json()

                if (!response.ok){
                    alert(data.message);
                    return;
                } 
                else {
                    alert('Registration successful!! Please Login');
                    this.clearform();
                    this.StudentRegister = false;
                    this.isLogin = true;
                }
            }
            catch(error) {
                console.log('Error:', error);
                alert('An error occurred during registration!! Please try again later');
            }
        },

        async coreg() {
            try{
                const response = await fetch('/api/company/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                        company_name: this.name,
                        hr_contact: this.hr_contact
                    })
                })

                const data = await response.json()

                if (!response.ok){
                    alert(data.message);
                    return;
                } 
                else {
                    alert('Registration successful!! Please Login');
                    this.clearform();
                    this.CompanyRegister = false;
                    this.isLogin = true;
                }
            }
            catch(error){
                console.log('Error:', error);
                alert('An error occurred during registration!! Please try again later');
            }
        },
        clearform() {
            this.email = '';
            this.password = '';
            this.name = '';
            this.branch = '',
            this.current_year = '',
            this.cgpa = '',
            this.resume_link = '',
            this.hr_contact = ''
        }
    }
}
</script>

<style scoped>

.main {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding-top: 0px;
}
.container {
    width: 320px;
    height: 400px;
    padding-top: 0px;
    border: 2px solid chocolate;
    border-radius: 20px;
    text-align: center;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
}

.container input {
    width: 280px;
    height: 43px;
    border: 2px solid goldenrod;
    border-radius: 12px;
    margin-bottom: 15px;
    margin-top: 20px;
    padding-left: 15px;
    font-weight: bold;
    font-size: 15px;
    font-family: cursive;
}

.container button {
    width: 117px;
    height: 40px;
    border: 2px solid goldenrod;
    border-radius: 10px;
    margin-bottom: 5px;
    display: inline-block;
    margin-top: 18px;
    transition: transform 0.3s ease, background-color 0.3s ease;
}

.container button:hover {
    background-color: gold;
    transform: scale(1.2);
}

.container i {
    font-size: 40px;
    color: black;
    margin-top: 20px;
}

.student-reg {
    width: 350px;
    height: 570px;
    padding-top: 15px;
    border: 2px solid chocolate;
    border-radius: 20px;
    text-align: center;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
}

.student-reg input {
    width: 300px;
    height: 40px;
    border: 2px solid goldenrod;
    border-radius: 10px;
    margin-bottom: 15px;
    padding-left: 15px;
    font-weight: bold;
    font-size: 15px;
    font-family: cursive;
}

.student-reg select {
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

.student-reg option {
    font-weight: bold;
    font-size: 15px;
    color: goldenrod;
}

.student-reg button {
    width: 117px;
    height: 40px;
    border: 2px solid goldenrod;
    border-radius: 10px;
    margin-top: 10px;
    transition: transform 0.3s ease, background-color 0.3s ease;
}

.student-reg button:hover {
    background-color: gold;
    transform: scale(1.2);
}

.student-reg i {
    font-size: 40px;
    color: black;
    margin-top: 20px;
}


.company-reg {
    width: 350px;
    height: 400px;
    padding-top: 0px;
    border: 2px solid chocolate;
    border-radius: 20px;
    text-align: center;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
}

.company-reg input {
    width: 300px;
    height: 40px;
    border: 2px solid goldenrod;
    border-radius: 10px;
    margin-bottom: 15px;
    padding-left: 15px;
    font-weight: bold;
    font-size: 15px;
    font-family: cursive;
}

.company-reg button {
    width: 117px;
    height: 40px;
    border: 2px solid goldenrod;
    border-radius: 10px;
    transition: transform 0.3s ease, background-color 0.3s ease;
}

.company-reg button:hover {
    background-color: gold;
    transform: scale(1.2);
}

.company-reg i {
    font-size: 40px;
    color: black;
    margin-top: 20px;
}

.main a {
    margin-top: 10px;
    color: black;
    transition: color 0.3s ease;
}
.main a:hover {
    color: blue;
}
</style>
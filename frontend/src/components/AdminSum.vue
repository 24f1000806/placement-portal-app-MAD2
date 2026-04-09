<template>
    <div>
        <div class="navbar" v-show="ifnavbar">
            <router-link to="/admin/dashboard">Home</router-link>
            <router-link to="/admin/students">Students</router-link>
            <router-link to="/admin/companies">Companies</router-link>
            <router-link to="/admin/search">Search</router-link>
            <router-link to="/admin/profile">Profile</router-link>
            <router-link to="/logout">Logout</router-link>
        </div>
       <div class="summ" style="padding: 50px;" v-show="ifchart">
            <form @submit.prevent="show">
                <h2 style="font-size: 35px;">Choose Chart!!</h2>
                <select v-model="showchartfor" required>
                    <option value="placement">Placement Summary</option>
                    <option value="drives">Drives per Company</option>
                </select>
                <button type="submit">Show Chart</button>
            </form>
       </div>
        <div class="chart" v-show="ifplacement">
            <img :src="chartURL" alt="Placement Summary Chart">
            <button @click="ifchart=true; ifnavbar=true; ifplacement=false;">Back</button>
        </div>
        <div class="chart" v-show="ifdrives">
            <img :src="chartURL" alt="Drives per Company Chart">
            <button @click="ifchart=true; ifnavbar=true; ifdrives=false;">Back</button>
        </div>
    </div>

</template>

<script>
export default {
    data() {
        return {
            ifchart: true,
            ifnavbar: true,
            ifplacement: false,
            ifdrives: false,
            showchartfor: 'placement',
            chartURL: ''
        }
    },
    methods: {
        async show() {
            try{
                const token = localStorage.getItem('token');
                const chart = this.showchartfor;
                const response = await fetch(`/api/admin/summary/${chart}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.ok) {
                    if (chart === 'placement') {
                        this.chartURL = '/static/charts/placement_summary.png'
                        this.ifchart = false;
                        this.ifplacement = true;
                        this.ifnavbar = false;
                        this.ifdrives = false;
                    }
                    else{
                        this.chartURL = '/static/charts/drive_summary.png'
                        this.ifchart = false;
                        this.ifplacement = false;
                        this.ifnavbar = false;
                        this.ifdrives = true;     
                    }
                }
                else{
                    alert('Failed to fetch chart. Please try again later.')
                }
            }
            catch(error) {
                console.error('Error:', error);
                alert('An error occurred while fetching the chart!!')
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
.summ{
    display: flex;
    align-items: center;
    justify-content: center;
}
.summ form{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 30px;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border-color: chocolate;
    border: 2px solid chocolate;
    border-radius: 10px;
    padding: 10px;
    width: 500px;
}
.summ select {
    padding: 15px;
    width: 350px;
    border-radius: 10px;
    font-size: 16px;
    background: #fff;
    border: 2px solid goldenrod;
}

.summ button{
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
.chart{
    width: 900px;
    height: 80vh;
    margin: 50px auto;
    background: rgba(255,255,255,0.85);
    border-radius: 15px;
    padding: 30px;
    text-align: center;

}
.chart img{
    width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 15px;
}
.chart a {
    display: inline-block;
    text-decoration: none;
    color: black;
    width: 90px;
    background: #fff;
    border: none;
    padding: 14px;
    border-radius: 10px;
    font-size: 17px;
    font-weight: bold;
    margin: 20px auto;
    transition: background 0.3s ease;
}
.chart a:hover{
    background: lightcoral;
}
.chart button{
    width: 100px;
    background: #fff;
    padding: 9px;
    border-radius: 10px;
    border: 2px solid goldenrod;
    font-size: 15px;
    font-weight: bold;
    display: block;
    transition: background 0.3s ease;
    margin: auto;
}
.chart button:hover{
    background-color: gold;
}
</style>
<script lang="ts" setup>
import { ref } from 'vue'
const username = ref('')
const password = ref('')
const message  = ref('')

const selected = ref<'student'|'teacher'>('student')

function handleLogin() {
    console.log(username, password)
}
</script>

<template>
    <div id="login-bg">
        <div class="login-container">
            <div class="login-title" :class="selected">
                <p class="teacher-title" @click="selected='teacher'">教师登录</p>
                <p class="student-title" @click="selected='student'">学生登录</p>
            </div>
            <form @submit.prevent="handleLogin">
                <input v-model="username" placeholder="用户名" />
                <input v-model="password" type="password" placeholder="密码" />
                <button type="submit">登录</button>
                <p v-if="message">{{ message }}</p>
            </form>
        </div>
    </div>
</template>

<style lang="css" scoped>
.login-title>p{
    cursor: pointer;
}

.login-title.student>.student-title,
.login-title.teacher>.teacher-title{
    color: rgb(26, 128, 130);
}

form>input,
form>button{
    height: 30px;
    border-radius: 4px;
}

.login-container{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 30px;
}

form{
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.login-title{
    display: flex;
    gap: 40px;
    font-size: larger;
}

.login-title>p.selected{
    color: #209359;
    font-weight: bold;
}

#login-bg {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

}

.login-container {
    width: 360px;
    height: 480px;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
    background-color: var(--color-background);
    border-radius: 14px;
    padding: 30px;
}
</style>
<script lang="ts" setup>
import { ref } from 'vue'
import WoocButton from '@/components/WoocButton.vue'
import { InputText } from 'primevue'
import { Form } from '@primevue/forms'
import WoocLogo from '@/assets/pic/wooc-logo.png'
import baseApiUrl from '@/api/baseUrl'
import SelectButton from 'primevue/selectbutton';


const username = ref('')
const password = ref('')
const email = ref('')
const message = ref('')

const selected = ref<'student' | 'teacher'>('student')
const states = ref<('注册'|'登录')[]>(['注册','登录'])
const state = ref(states.value[0])

function onFormSubmit() {
    console.log(username.value, password.value)
    fetch(new URL('login', baseApiUrl),{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value,
            role: selected.value,
            email: email.value
        })
    }).then(res => res.json()).then(data => { 
        message.value = data.message
        console.log(data)
    })
}

</script>

<template>
    <div id="login-bg">
        <div class="login-container">
            <img :src="WoocLogo" alt="Wooc Logo">
            <div class="login-title" :class="selected">
                <p class="teacher-title" @click="selected = 'teacher'">教师</p>
                <p class="student-title" @click="selected = 'student'">学生</p>
            </div>
            <Form @submit="onFormSubmit">
                <InputText v-model:model-value="username" name="username" type="text" placeholder="用户名" fluid />
                <InputText v-model:model-value="password" name="password" type="password" placeholder="密码" fluid />
                <InputText v-if="state=='注册'" v-model:model-value="email" name="email" type="email" placeholder="邮箱" fluid />
                <WoocButton type="submit">点击{{ state }}</WoocButton>
            </Form>
            <SelectButton v-model="state" :options="states"></SelectButton>
        </div>
    </div>
</template>


<style lang="css" scoped>
.login-title>p {
    cursor: pointer;
}

.login-title.student>.student-title,
.login-title.teacher>.teacher-title {
    color: var(--color-tint);
}

.login-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 30px;
}

form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.login-title {
    display: flex;
    gap: 40px;
    font-size: larger;
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
    height: 520px;
    box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
    background-color: var(--color-background);
    border-radius: var(--card-border-radius);
    padding: 30px;
}
</style>
<script lang="ts" setup>
import { ref } from 'vue'
import Button from 'primevue/button'
import { InputText } from 'primevue'
import { Form } from '@primevue/forms'
import WoocLogo from '@/assets/pic/wooc-logo.png'
import baseApiUrl from '@/api/baseUrl'
import SelectButton from 'primevue/selectbutton';
import FloatLabel from 'primevue/floatlabel'
import Password from 'primevue/password'
import { useToast } from 'primevue/usetoast'
import Toast from 'primevue/toast'
import { accountState } from '@/global/account'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const email = ref('')
// const message = ref('')

const selected = ref<'student' | 'teacher'>('student')
const states = ['注册', '登录']
const state = ref(states[0])
const router = useRouter()

const toast = useToast()

function onFormSubmit() {
  switch (state.value) {
    case '登录':
      fetch(new URL('login', baseApiUrl), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: username.value,
          password: password.value,
          role: selected.value
        })
      }).then(res => res.json()).then(data => {
        console.log(data)
        if (data.result == true) {
          accountState.isLoggedIn = true
          accountState.role = data.user.role
          accountState.userid = data.user.id
          accountState.username = username.value
          router.push('/')
        }
        toast.add({
          severity: data.result ? 'success' : 'warn',
          summary: '登录结果',
          detail: data.message,
          life: 3000
        })
      })
      break;
    case '注册':
      fetch(new URL('register', baseApiUrl), {
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
        console.log(data)
        toast.add({
          severity: 'info',
          summary: '注册结果',
          detail: data.message,
          life: 3000
        })
      })
      break;
  }
}

</script>

<template>
  <div id="login-bg">
    <div class="login-container">
      <img :src="WoocLogo" alt="Wooc Logo">
      <div class="login-title" :class="selected">
        <p class="teacher-title" @click="selected = 'teacher'">我是教师</p>
        <p class="student-title" @click="selected = 'student'">我是学生</p>
      </div>
      <Form @submit="onFormSubmit">
        <FloatLabel variant="on">
          <InputText id="username" v-model="username" type="text" fluid />
          <label for="username">用户名</label>
        </FloatLabel>
        <FloatLabel variant="on" v-if="state === '注册'">
          <InputText id="email" v-model="email" type="email" fluid />
          <label for="email">邮箱</label>
        </FloatLabel>
        <FloatLabel variant="on">
          <Password id="password" :toggle-mask="true" v-model="password" type="password" :feedback="false" fluid />
          <label for="password">密码</label>
        </FloatLabel>
        <Button type="submit" :label="state" />
        <Toast />
      </Form>
      <SelectButton v-model="state" :options="states"></SelectButton>
    </div>
  </div>
</template>


<style lang="css" scoped>
.login-title>p {
  cursor: pointer;
  transition: color 0.2s;
}

.login-title>p:hover {
  color: gray;
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
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.1);
  background-color: var(--color-background);
  border-radius: var(--card-border-radius);
  padding: 60px;
}
</style>
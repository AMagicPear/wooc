import { reactive } from "vue";

export type UserRole = 'none' | 'student' | 'teacher'

export const accountState = reactive({
    isLoggedIn: false,
    userid : 0,
    role: 'none' as UserRole,
    username: undefined as string | undefined
})

// 调试时默认处于已登录
accountState.isLoggedIn = true
accountState.userid = 1
accountState.role = 'student'
accountState.username = "perry"

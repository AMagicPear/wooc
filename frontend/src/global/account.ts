import { reactive } from "vue";

export type UserRole = 'none' | 'student' | 'teacher'

export const accountState = reactive({
    isLoggedIn: false,
    userid : 0,
    role: 'none' as UserRole,
    username: undefined as string | undefined
})

import baseApiUrl from "@/api/baseUrl";
import type { Course } from "@/api/lessonApi";
import { reactive } from "vue";

export type UserRole = 'none' | 'student' | 'teacher'

export const accountState = reactive({
    isLoggedIn: false,
    userid: 0,
    role: 'none' as UserRole,
    username: undefined as string | undefined,
    enrolled: [] as number[]
})

export const getEnrolled = async () => {
    let coursesResult: { courses: Course[] } = await (
        await fetch(new URL(`/students/${accountState.userid}/courses`, baseApiUrl))
    ).json();
    accountState.enrolled = coursesResult.courses.map(course => course.id)
    return coursesResult.courses
}

// 调试时默认处于已登录
// accountState.isLoggedIn = true
// accountState.userid = 1
// accountState.role = 'student'
// accountState.username = "perry"
// getEnrolled()
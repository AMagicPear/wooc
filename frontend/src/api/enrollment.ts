export interface Enrollment {
    id: number,
    student_id: number,
    course_id: number,
    enrolled_at: string,
    completed_at: string,
    progress: number,
    username: string,
    email: string
}
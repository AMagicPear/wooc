export interface Course {
    cover_image: string,
    created_at: string,
    description: string,
    enrollment_count: number,
    id: number,
    teacher_id: number,
    teacher_name: string,
    title: string,
    updated_at: string,
}

export interface CoursePost {
    title: string,
    description: string,
    teacher_id: number,
    cover_image?: string,
}

export interface CourseResourceItem {
    "course_id": number,
    "created_at": string,
    "description": string,
    "duration": number,
    "file_path": string,
    "file_size": number,
    "id": number,
    "resource_type": "video" | "audio" | "document" | "image" | "link",
    "title": string
}

export interface Exam {
    "course_id": number,
    "created_at": string,
    "description": string,
    "duration": number,
    "id": number,
    "passing_score": number,
    "question_count": number,
    "title": string
}

export interface Question {
    correct_answer: string,
    id: number,
    options?: string[],
    question_text: string,
    question_type: 'multiple_choice' | 'true_false' | 'short_answer' | 'essay',
    score: number,
    test_id: number
}

export interface Assignment {
    course_id: number,
    created_at: string,
    deadline: string,
    description: string,
    id: number,
    max_score: number,
    title: string
}

export interface AssignmentSubmissionPost {
    assignment_id: number;
    text: string;
    file_paths: Record<string, string>;
    student_id: number;
}
export interface AssignmentSubmission {
    assignment_id: number;
    content: string;
    email: string;
    feedback?: string;
    file_path: Record<string, string>;
    graded_at?: string;
    grader_id?: number;
    id: number;
    score?: number;
    student_id: number;
    submitted_at: string;
    username: string;
}

// 作业的批改
export interface Grade{
    id: number,
    feedback: string,
    email: string,
    graded_at: string,
    grader_id: number,
    score: number
    student_id: number,
    username: string,
    assignment_id: number
}
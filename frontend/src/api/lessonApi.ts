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
    teacher_id: string,
    cover_image: string,
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

export interface AssignmentSubmission {
    assignment_id: number;
    text: string;
    file_paths: Record<string, string>;
    student_id: number;
}
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
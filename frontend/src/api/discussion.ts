export interface DiscussionPost {
    course_id: number,
    title: string,
    content: string,
    author_id: number
}

export interface Discussion {
    author_id: number,
    author_name: string,
    content: string,
    course_id: 1,
    id: number,
    reply_count: number,
    title: string,
    created_at: string,
    updated_at: string
}
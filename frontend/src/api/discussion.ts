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
    course_id: number,
    id: number,
    reply_count: number,
    title: string,
    created_at: string,
    updated_at: string
}

export interface Reply {
    author_id: number,
    author_name: string,
    content: string,
    created_at: string,
    discussion_id: number,
    id: number
}
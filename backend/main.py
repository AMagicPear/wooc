from util.db_connection import init_database
import util.user_functions as user
import util.course_functions as course
import util.resource_functions as resource
import util.enrollment_functions as enrollment
import util.progress_functions as progress
import util.discussion_functions as discussion
import util.assignment_functions as assignment
import util.test_functions as test


def main():
    # 初始化数据库
    init_database()
    
    # 示例：创建一个教师用户
    teacher_id = user.register_user("teacher1", "password123", "teacher@example.com", "teacher")
    if teacher_id:
        print(f"教师用户创建成功，ID: {teacher_id}")
    else:
        print("教师用户创建失败，用户名或邮箱已存在")
    
    # 示例：创建一个学生用户
    student_id = user.register_user("student1", "password123", "student@example.com", "student")
    if student_id:
        print(f"学生用户创建成功，ID: {student_id}")
    else:
        print("学生用户创建失败，用户名或邮箱已存在")
    
    # 示例：创建一门课程
    course_id = course.create_course("Python编程基础", "学习Python编程语言的基础知识", teacher_id, "course_cover.jpg")
    if course_id:
        print(f"课程创建成功，ID: {course_id}")
    else:
        print("课程创建失败")
    
    # 示例：添加课程资源
    video_id = resource.add_course_resource(course_id, "第1课：Python介绍", "Python语言概述", "video", "videos/lesson1.mp4", 10240000, 3600)
    ppt_id = resource.add_course_resource(course_id, "第1课：Python介绍PPT", "课程PPT", "document", "documents/lesson1.pptx", 5120000)
    
    # 示例：学生选课
    enrollment_id = enrollment.enroll_student(student_id, course_id)
    if enrollment_id:
        print(f"学生选课成功，ID: {enrollment_id}")
    else:
        print("学生选课失败，可能已选过该课程")
    
    # 示例：更新学习进度
    progress.update_learning_progress(student_id, video_id, 1800, False)  # 观看了30分钟
    progress.update_learning_progress(student_id, ppt_id, 600, True)    # 已完成文档学习
    
    # 示例：创建讨论主题
    discussion_id = discussion.create_discussion(course_id, "Python编程问题", "关于Python列表的疑问", student_id)
    if discussion_id:
        print(f"讨论主题创建成功，ID: {discussion_id}")
    else:
        print("讨论主题创建失败")
    
    # 示例：回复讨论
    reply_id = discussion.add_discussion_reply(discussion_id, "我认为应该使用列表推导式来解决这个问题", teacher_id)
    if reply_id:
        print(f"讨论回复成功，ID: {reply_id}")
    else:
        print("讨论回复失败")
    
    # 示例：创建作业
    assignment_id = assignment.create_assignment(course_id, "Python基础作业", "完成Python基础练习", "2023-12-31 23:59:59", 100)
    if assignment_id:
        print(f"作业创建成功，ID: {assignment_id}")
    else:
        print("作业创建失败")
    
    # 示例：提交作业
    submission_id = assignment.submit_assignment(assignment_id, student_id, "这是我的作业内容", "assignments/student1_work.pdf")
    if submission_id:
        print(f"作业提交成功，ID: {submission_id}")
    else:
        print("作业提交失败")
    
    # 示例：批改作业
    graded = assignment.grade_assignment(submission_id, 85, "做得很好，有些细节需要改进", teacher_id)
    if graded:
        print("作业批改成功")
    else:
        print("作业批改失败")
    
    # 示例：创建测试
    test_id = test.create_test(course_id, "Python基础知识测试", "测试Python基础知识掌握情况", 60, 60)
    if test_id:
        print(f"测试创建成功，ID: {test_id}")
    else:
        print("测试创建失败")
    
    # 示例：添加测试题目
    question_id1 = test.add_test_question(test_id, "Python中如何定义一个函数？", "short_answer", None, "def 函数名(参数):")
    question_id2 = test.add_test_question(test_id, "以下哪个是Python的内置数据类型？", "multiple_choice", ["int", "float", "list", "all"], "all")
    
    # 示例：开始测试
    attempt_id = test.start_test(test_id, student_id)
    if attempt_id:
        print(f"测试开始，ID: {attempt_id}")
    else:
        print("测试开始失败")
    
    # 示例：提交测试答案
    test.submit_test_answer(attempt_id, question_id1, "def function():")
    test.submit_test_answer(attempt_id, question_id2, "all")
    
    # 示例：完成测试
    completed = test.complete_test(attempt_id)
    if completed:
        print("测试完成")
    else:
        print("测试完成失败")

if __name__ == "__main__":

    main()
    
<script setup lang="ts">
import { Card } from "primevue";
</script>

<template>
  <div class="about">
    <Card>
      <template #title>→砖大学MOOC</template>
      <template #content>
        <section>
          <h2>背景</h2>
          <p>
            在数字化教育时代，开发一个在线数字媒体教学平台，为教师和学生提供一个便捷的教学和学习环境，支持多种数字媒体形式的教学内容展示和互动。
          </p>
        </section>
        <section>
          <h2>功能要求</h2>
          <ul>
            <li>
              <strong>课程管理：</strong
              >教师可以创建课程，上传课程大纲、教学视频、音频、PPT等教学资源；学生可以浏览和选择课程进行学习。
            </li>
            <li>
              <strong>教学互动：</strong
              >提供在线讨论区、作业提交与批改、在线测试等功能，促进师生之间的互动和交流。
            </li>
            <li>
              <strong>多媒体播放：</strong
              >支持高清视频、音频的流畅播放，提供播放控制功能（如暂停、快进、快退等）。
            </li>
            <li>
              <strong>学习进度跟踪：</strong
              >记录学生的学习进度，包括已完成的课程、观看的视频时长、作业完成情况等。
            </li>
            <li>
              <strong>用户管理：</strong
              >实现教师和学生的注册、登录、权限管理等功能。
            </li>
          </ul>
        </section>
        <section>
          <h2>技术要求</h2>
          <ul>
            <li>
              <strong>前端：</strong
              >使用Vue等现代前端框架构建用户界面，提供良好的用户体验。
            </li>
            <li>
              <strong>后端：</strong>采用Node.js、Spring
              Boot等技术进行后端开发，使用数据库存储课程信息、用户数据等。
            </li>
            <li>
              <strong>多媒体播放：</strong
              >利用HTML5的多媒体播放功能，结合相关的播放器插件（如video.js等）实现多媒体内容的播放。
            </li>
          </ul>
        </section>
      </template>
    </Card>
    <Card>
      <template #title>作者信息</template>
      <template #content>
        <p>B22170323沈立</p>
        <p>B22170322杨徐</p>
        <p>B22170321张俊泽</p>
      </template>
    </Card>
  </div>
</template>

<style lang="css" scoped>
.about {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

h2 {
  color: #29b965;
  margin-top: 25px;
}
ul {
  padding-left: 20px;
}
li {
  margin-bottom: 8px;
}
.section {
  padding: 15px;
  margin-bottom: 20px;
}
</style>
